# Key Flows — Six End-to-End Traces

These six flows are the spine of the curriculum. Other modules rotate among them; none of them reuses the same flow twice as its main example.

1. [Browse catalog](#flow-1-browse-the-catalog) — UI → REST → Postgres (read path, pagination)
2. [Add to basket](#flow-2-add-item-to-basket) — UI → gRPC → Redis (auth boundary, cache-style state)
3. [Checkout / create order](#flow-3-checkout) — UI → REST → CQRS → outbox → RabbitMQ (the big one)
4. [Order state machine](#flow-4-order-lifecycle-grace-period--stock--payment) — background workers + integration events
5. [Login](#flow-5-login-oidc) — cookie + OIDC + JWT auth boundary
6. [Price change](#flow-6-admin-price-change) — write path with conditional event publication

---

## Flow 1: Browse the catalog

Why this flow matters: it is the simplest full-stack path in the repo and the template for every read endpoint you will ever write: filter → count → page → return typed result.

Open these files first:
- `src/WebApp/Components/Pages/Catalog/Catalog.razor` — the page component
- `src/WebApp/Extensions/Extensions.cs:L34-L36` — the typed `HttpClient` for `CatalogService`, with API version 2.0 and auth token handler
- `src/Catalog.API/Apis/CatalogApi.cs:L26-L30` — route registration; `:L124-L159` — the handler

Trace:

| Step | Owner | File | What happens | Data shape | Risk |
| --- | --- | --- | --- | --- | --- |
| 1 | WebApp (Blazor Server) | `Catalog.razor` | Component renders on the server, calls `CatalogService` | route/query params | UI coupled to service availability |
| 2 | WebApp | `Extensions.cs:L34-L36` | `HttpClient` with base address `https+http://catalog-api` (service discovery), `.AddApiVersion(2.0)`, `.AddAuthToken()` | HTTP GET | version pinning lives here, not in call sites |
| 3 | Catalog.API | `CatalogApi.cs:L16-L18` | Versioned route group `api/catalog`, v1 + v2 registered side by side | route match | two versions of `/items` differ in signature |
| 4 | Catalog.API | `CatalogApi.cs:L134-L147` | Builds an `IQueryable`, composes optional `name`/`type`/`brand` filters | `IQueryable<CatalogItem>` | deferred execution — nothing hits the DB yet |
| 5 | Catalog.API | `CatalogApi.cs:L149-L156` | `LongCountAsync()` then `OrderBy(Name).Skip().Take().ToListAsync()` | 2 SQL queries | count+page is 2 round trips; fine here, worth knowing |
| 6 | Catalog.API | `CatalogApi.cs:L158` | Wraps in `PaginatedItems<CatalogItem>` | JSON | returns the **EF entity** directly — no DTO. Contract = schema. |
| 7 | WebApp | `MapForwarder` `src/WebApp/Program.cs:L32` | Product images proxied to `/api/catalog/items/{id}/pic` | binary | image bytes never pass through Blazor code |

Validation and authorization: route constraints (`{id:int}`, `{name:minlength(1)}` at `CatalogApi.cs:L36-L46`); explicit guard `id <= 0` → ProblemDetails 400 at `:L176-L181`. **No authorization on catalog reads — it's a public catalog, and that's a deliberate choice worth saying out loud in an interview.**

Persistence and side effects: read-only; EF Core over Postgres. `GetItemById` uses `.Include(ci => ci.CatalogBrand)` at `:L183` — eager loading to avoid a lazy N+1.

Tests that cover it: `tests/Catalog.FunctionalTests/CatalogApiTests.cs` runs against a real Aspire-hosted Postgres container (`CatalogApiFixture.cs:L17-L25`). e2e: `e2e/BrowseItemTest.spec.ts`.

What juniors usually miss: `IQueryable` composition means the `if (name is not null)` blocks build SQL, not filter in memory. Deleting the `.Skip/.Take` would return the whole table.

What seniors notice: the API returns EF entities as the wire contract (`PaginatedItems<CatalogItem>`). Cheap now; any schema change is silently a **public contract change**. Also: `LongCountAsync` runs on the *filtered* query here, but in the semantic-search variant (`:L259-L260`) the count is over **all** items while the page is filtered by `Embedding != null` — *possible inconsistency between total and page contents; investigate*.

Interview angle: "How do you implement pagination correctly?" — answer with this exact file: compose filters on `IQueryable`, count then page in SQL, return page index/size/total in the payload. Mention offset pagination's weakness (late pages scan) and the keyset alternative.

Drill: add (on paper) a `maxPrice` filter to `GetAllItems`. Which lines change? What's the SQL effect?
Self-grade — Basic: new `Where` clause after L147. Solid: also updates route metadata/OpenAPI description and mentions the v1/v2 split (which version gets it?). Strong: notes that filtering by price on a decimal column is index-friendly, that adding it to v2 only is a non-breaking contract change, and that a test belongs in `CatalogApiTests`.

---

## Flow 2: Add item to basket

Why this flow matters: it crosses the repo's only gRPC boundary, shows Redis used as a keyed document store, and demonstrates a *client-computes, server-stores* design with real concurrency implications.

Open these files first:
- `src/WebApp/Services/BasketState.cs:L33-L56` — `AddAsync`
- `src/WebApp/Extensions/Extensions.cs:L31-L32` — gRPC client registration with `.AddAuthToken()`
- `src/Basket.API/Grpc/BasketService.cs:L36-L57` — `UpdateBasket`
- `src/Basket.API/Repositories/RedisBasketRepository.cs:L34-L48` — persistence

Trace:

| Step | Owner | File | What happens | Data shape | Risk |
| --- | --- | --- | --- | --- | --- |
| 1 | WebApp | `BasketState.cs:L35` | Reads current basket (cached `Task` in `_cachedBasket`) | `List<BasketQuantity>` | read-modify-write starts here |
| 2 | WebApp | `BasketState.cs:L37-L51` | Increments quantity or appends new item **in UI memory** | mutated list | lost-update window: two tabs/circuits can interleave |
| 3 | WebApp | `BasketState.cs:L53-L54` | Invalidates cache, sends **whole basket** via gRPC | `UpdateBasketRequest` | full replace, not delta |
| 4 | Basket.API | `BasketService.cs:L38-L41` | `context.GetUserIdentity()`; unauthenticated → `RpcException(Unauthenticated)` | userId from JWT `sub` | the basket key is the caller's identity — users can't touch others' baskets |
| 5 | Basket.API | `BasketService.cs:L49-L50` | Maps proto → `CustomerBasket` (ProductId + Quantity only) | model | server stores no prices — prices re-resolved at read time |
| 6 | Basket.API | `RedisBasketRepository.cs:L36-L37` | JSON (source-generated serializer) → `StringSetAsync("/basket/{sub}")` | UTF-8 bytes | last-writer-wins; no TTL — *possible risk: baskets live forever* |
| 7 | Basket.API | `RedisBasketRepository.cs:L47` | Reads it back and returns it | `CustomerBasket` | extra round trip per update |

Validation and authorization: authN enforced in the service method itself (`BasketService.cs:L38-L41`, `:L61-L65`); `GetBasket` is `[AllowAnonymous]` and returns an **empty basket** for anonymous callers rather than 401 (`:L12-L19`). JWT validation configured in `src/eShop.ServiceDefaults/AuthenticationExtensions.cs:L33-L50` (note `ValidateAudience = false` at L49 — *possible risk, see security checklist*).

Persistence and side effects: Redis only. No events published. Basket contents get authoritative prices later, from Catalog, in `BasketState.FetchBasketItemsAsync` (`BasketState.cs:L117-L149`) — the client never supplies a price the server trusts (compare Flow 3).

Tests that cover it: `tests/Basket.UnitTests/BasketServiceTests.cs` (gRPC service with fake repo). e2e: `e2e/AddItemTest.spec.ts`, `RemoveItemTest.spec.ts`.

What juniors usually miss: the quantity increment happens in the **WebApp**, not the Basket service. The server can't enforce "quantity only goes up by 1" — it stores whatever the client sends.

What seniors notice: read-modify-write over gRPC with last-writer-wins storage = **lost updates** under concurrency (two browser tabs on the same account). Acceptable for a basket; unacceptable for money. Also `BasketState` caches a `Task` (`_cachedBasket`), a neat idiom that dedupes concurrent fetches per circuit.

Interview angle: "Where would you put a shopping basket — DB or cache — and what consistency do you give up?" Mid-level answer names last-writer-wins, per-user keying by JWT `sub` (an isolation boundary), and price re-resolution to keep the client untrusted.

Drill: write the exact sequence of two interleaved `AddAsync` calls (tabs A and B) that loses an item.
Self-grade — Basic: produces the interleaving. Solid: names it "lost update / read-modify-write race" and points at `BasketState.cs:L35-L54`. Strong: proposes fixes (server-side delta op `AddItem(productId, qty)`, Redis `WATCH`/Lua, or version field) and says why the repo's choice is fine for baskets.

---

## Flow 3: Checkout

Why this flow matters: this is the interview flow. It touches idempotency, CQRS, a DDD aggregate, a transactional outbox, and event-driven fan-out — five senior vocabulary words in one click.

Open these files first:
- `src/WebApp/Components/Pages/Checkout/Checkout.razor:L101-L116` — submit handler (`[Authorize]` at L6)
- `src/WebApp/Services/BasketState.cs:L78-L109` — `CheckoutAsync`
- `src/Ordering.API/Apis/OrdersApi.cs:L118-L168` — `CreateOrderAsync`
- `src/Ordering.API/Application/Behaviors/` — the MediatR pipeline
- `src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs:L52-L65` — aggregate ctor
- `src/Ordering.Infrastructure/OrderingContext.cs:L47-L62` — `SaveEntitiesAsync`

Trace:

| Step | Owner | File | What happens | Data shape | Risk |
| --- | --- | --- | --- | --- | --- |
| 1 | WebApp | `Checkout.razor:L101-L109` | Form submit; DataAnnotations validate; custom check "cart not empty" (L118-L126) | `BasketCheckoutInfo` | RequestId generated at page init (L94) — same ID on retry, by design |
| 2 | WebApp | `BasketState.cs:L80-L86` | Ensures RequestId; resolves buyerId (`sub` claim) + username | GUID, strings | buyer identity from auth state, never from form |
| 3 | WebApp | `BasketState.cs:L89-L106` | Fetches basket items **with catalog prices**, builds `CreateOrderRequest` with hardcoded test card `1111...4444` | request record | demo shortcut: fake card data (L100-L103) |
| 4 | Ordering.API | `OrdersApi.cs:L119-L136` | Reads `x-requestid` header; empty GUID → 400. Logs *without* the request body ("don't log the request as it has CC number", L130) | header GUID | idempotency key is client-supplied |
| 5 | Ordering.API | `OrdersApi.cs:L140-L146` | Masks card number, wraps command: `IdentifiedCommand<CreateOrderCommand,bool>` | command | masking before it ever reaches a handler/log |
| 6 | Ordering.API | `ValidatorBehavior.cs:L20-L34` | FluentValidation validators run; failures throw `OrderingDomainException` | — | `CreateOrderCommandValidator.cs:L6-L16`: card length 12–19, CVV length 3, items non-empty |
| 7 | Ordering.API | `IdentifiedCommandHandler.cs:L41-L48` | `requestManager.ExistAsync(id)` — duplicate? return `true` and do nothing. Else record the request id | DB row (`ClientRequest`) | **idempotency**: retries are absorbed here |
| 8 | Ordering.API | `TransactionBehavior.cs:L32-L52` | Opens EF transaction (execution strategy), runs inner handler, commits, **then** publishes outbox events | transaction scope | events publish only after commit — the outbox contract |
| 9 | Ordering.API | `CreateOrderCommandHandler.cs:L32-L33` | Saves `OrderStartedIntegrationEvent` to the **integration event log** (same DB) | outbox row | not sent yet, just recorded |
| 10 | Domain | `Order.cs:L52-L65`, `:L71-L91` | Aggregate ctor sets `Submitted`, raises `OrderStartedDomainEvent`; `AddOrderItem` merges duplicate products, applies best discount | aggregate | invariants enforced in one place |
| 11 | Ordering.Infra | `OrderingContext.cs:L47-L62` + `MediatorExtension.cs:L5-L20` | `SaveEntitiesAsync`: dispatch domain events **before** `SaveChangesAsync`, so handler side effects join the same transaction | — | in-process handlers create the Buyer, verify payment method (in `Application/DomainEventHandlers/` — *inferred*) |
| 12 | Ordering.API | `TransactionBehavior.cs:L52` | After commit: `PublishEventsThroughEventBusAsync(transactionId)` reads pending outbox rows and publishes | RabbitMQ msg | crash between commit and publish → event stays `NotPublished` (*no retry dispatcher — see critique*) |
| 13 | Basket.API | `OrderStartedIntegrationEventHandler.cs:L10-L15` | Deletes the user's basket | — | at-least-once consumer; delete is naturally idempotent |

Validation and authorization: `[Authorize]` on the page (`Checkout.razor:L6`); JWT bearer on Ordering.API (`AuthenticationExtensions.cs:L33-L50`); form validation (DataAnnotations); command validation (FluentValidation); aggregate invariants (`OrderItem` throws on negative units — see `tests/Ordering.UnitTests/Domain/OrderAggregateTest.cs:L31-L43`). Four validation layers, each with a different job.

Persistence and side effects: one Postgres transaction containing: order row(s), buyer/payment rows (via domain event handlers), the `ClientRequest` idempotency row, and the outbox row. Side effects after commit: RabbitMQ publish → basket deletion.

Tests that cover it: `tests/Ordering.UnitTests/Application/` (command handler tests), `tests/Ordering.FunctionalTests/` (API level). No e2e checkout spec found in `e2e/` — *gap worth noting*.

What juniors usually miss: `TypedResults.Ok()` is returned at `OrdersApi.cs:L166` **even when `result` is false** (failed command). The HTTP contract says 200; the log says failure. Look at L157-L164 and confirm.

What seniors notice: (1) the idempotency check (`ExistAsync`) runs *inside* the transaction behavior's scope, so the request record and the order commit atomically — a crash can't record the request without the order; (2) `IdentifiedCommandHandler.cs:L99-L102` swallows **all** exceptions and returns `default` — a validation failure becomes HTTP 200 with a warning log; (3) the WebApp deletes the basket directly (`BasketState.cs:L108`) *and* the event handler deletes it — belt and suspenders because the event path is at-least-once and the direct path is best-effort.

Interview angle: this flow *is* the answer to "design a checkout that survives retries and crashes." Rehearse it: idempotency key → validate → transaction → aggregate → outbox → publish-after-commit → idempotent consumers.

Drill: the user double-clicks "Place order" and the browser sends two identical POSTs. Write down what happens at each of steps 4, 7, and 13 for the second request.
Self-grade — Basic: second request returns 200 without creating a second order. Solid: cites `CreateResultForDuplicateRequest()` returning `true` (`CreateOrderCommandHandler.cs:L67-L70`) and that the RequestId is created at page-init, not per click. Strong: explains what breaks if the client generated a *new* GUID per click, and where you'd add a server-side uniqueness net (e.g., unique index on (buyer, basket-hash, window) — with its false-positive tradeoff).

---

## Flow 4: Order lifecycle (grace period → stock → payment)

Why this flow matters: it's a distributed state machine driven entirely by asynchronous events across four services — the repo's best material for reliability questions (retries, ordering, at-least-once).

Open these files first:
- `src/OrderProcessor/Services/GracePeriodManagerService.cs:L26-L36`, `:L63-L93`
- `src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs:L99-L168` — the state transitions
- `src/Catalog.API/IntegrationEvents/EventHandling/OrderStatusChangedToAwaitingValidationIntegrationEventHandler.cs`
- `src/PaymentProcessor/IntegrationEvents/EventHandling/OrderStatusChangedToStockConfirmedIntegrationEventHandler.cs`

State machine (from `Order.cs`): `Submitted → AwaitingValidation → StockConfirmed → Paid → Shipped`, with `Cancelled` reachable until Paid (`SetCancelledStatus` throws if Paid/Shipped, `Order.cs:L142-L153`).

Trace:

| Step | Owner | File | What happens | Data shape | Risk |
| --- | --- | --- | --- | --- | --- |
| 1 | OrderProcessor | `GracePeriodManagerService.cs:L26-L36` | `BackgroundService` loop every `CheckUpdateTime` seconds | timer | polling, not scheduling — fine at this scale |
| 2 | OrderProcessor | `:L69-L74` | **Raw SQL** against `ordering.orders`: submitted orders older than grace period | `List<int>` | a second service reads Ordering's DB — boundary leak, deliberate tradeoff |
| 3 | OrderProcessor | `:L53-L60` | Publishes `GracePeriodConfirmedIntegrationEvent` per order | event | re-published every poll until status changes — consumers must be idempotent |
| 4 | Ordering.API | `Application/IntegrationEvents/EventHandling/GracePeriodConfirmedIntegrationEventHandler.cs` | Sends `SetAwaitingValidationOrderStatusCommand` (*inferred from names*) → `Order.SetAwaitingValidationStatus` (`Order.cs:L99-L106`) — **guarded**: only transitions from Submitted | command | the status guard is what makes duplicate events harmless |
| 5 | Catalog.API | `OrderStatusChangedToAwaitingValidation...Handler.cs:L15-L29` | Checks `AvailableStock >= Units` per item; publishes StockConfirmed or StockRejected via **its own outbox** (L31-L32) | event | check only — stock is *decremented* later, on Paid |
| 6 | PaymentProcessor | `OrderStatusChangedToStockConfirmed...Handler.cs:L21-L28` | Simulated payment: config flag `PaymentSucceeded` decides success/failure | event | payment is a stub — by design |
| 7 | Ordering.API | payment succeeded/failed handlers | `SetPaidStatus` (`Order.cs:L119-L128`, guarded on StockConfirmed) or cancellation path | DB update | each transition publishes the next `OrderStatusChangedTo*` event |
| 8 | WebApp | `Extensions.cs:L43-L51` | WebApp itself subscribes to all six status events → `OrderStatusNotificationService` pushes live updates to the user's open page | UI notification | a *frontend* consuming the bus — unusual and worth discussing |

Validation and authorization: none per event — RabbitMQ messages are trusted intra-system traffic. The *state guards* in `Order.cs` are the real protection.

Persistence and side effects: every transition is a DB write in Ordering + an outbox event. Catalog decrements real stock in `OrderStatusChangedToPaidIntegrationEventHandler.cs` (same folder).

Tests that cover it: `tests/Ordering.UnitTests/Domain/OrderAggregateTest.cs` covers transitions; no cross-service integration test exists — the seams are tested only implicitly. *Gap.*

What juniors usually miss: events can arrive **twice or out of order**. The system survives because transitions are guarded by current status (`if (OrderStatus == ...)`) — idempotency by state check, not by deduplication.

What seniors notice: `RabbitMQEventBus.OnMessageReceived` **acks even on handler exception** (`RabbitMQEventBus.cs:L177-L180`, with an explicit comment recommending DLX for real systems). A failed stock check handler = event lost forever = order stuck in AwaitingValidation. This is the single best "what would you harden first?" answer in the repo.

Interview angle: "How do services coordinate without distributed transactions?" — choreographed saga: each service reacts to events, state guards give idempotency, compensation = cancellation path (`SetCancelledStatusWhenStockIsRejected`, `Order.cs:L155-L168`).

Drill: build the timeline for an order where stock is rejected. Which services write to their DBs, in what sequence, and what does the user see?
Self-grade — Basic: correct event sequence ending in Cancelled. Solid: notes the description text listing rejected product names and the WebApp live notification. Strong: identifies what happens if `OrderStockRejected` is lost (order stuck; grace-period manager will *not* rescue it because status ≠ Submitted) and proposes a reconciliation job.

---

## Flow 5: Login (OIDC)

Why this flow matters: it's a textbook *federated identity* setup: one identity provider, cookie session for the web UI, JWT bearer for APIs. Every multi-service system you'll work on has some version of this.

Open these files first:
- `src/WebApp/Extensions/Extensions.cs:L53-L92` — cookie + OIDC client config
- `src/eShop.ServiceDefaults/AuthenticationExtensions.cs:L33-L50` — JWT validation on APIs
- `src/Identity.API/Configuration/Config.cs:L18-L24` — API scopes; client registrations at L44+
- `src/eShop.AppHost/Program.cs:L96-L101` — the callback-URL cyclic wiring

Trace:

| Step | Owner | File | What happens | Risk |
| --- | --- | --- | --- | --- |
| 1 | WebApp | `Extensions.cs:L66-L70` | Default scheme = cookie; challenge = OIDC | — |
| 2 | WebApp → Identity | `Extensions.cs:L72-L87` | Authorization-code flow, `ClientId "webapp"`, scopes `openid profile orders basket`, `SaveTokens = true` | `ClientSecret = "secret"` hardcoded — sample-only |
| 3 | Identity.API | Duende IdentityServer (`Config.cs`) | Authenticates seeded user, issues code → tokens | mostly vendored quickstart UI — don't imitate blindly |
| 4 | WebApp | cookie | Session established; tokens stored in the auth cookie (`SaveTokens`) | cookie size; lifetime 60 min default (L62) |
| 5 | WebApp → APIs | `Extensions.cs:L32,L36,L40` | `.AddAuthToken()` forwards the access token on gRPC/HTTP calls | token relay — WebApp acts on user's behalf |
| 6 | APIs | `AuthenticationExtensions.cs:L33-L50` | JWT bearer validates issuer; **`ValidateAudience = false` (L49)** despite setting an audience | *possible risk: a token minted for basket also passes at ordering* |
| 7 | Any API | e.g. `BasketService.cs:L15` | Identity = `sub` claim (`DefaultInboundClaimTypeMap.Remove("sub")` at `AuthenticationExtensions.cs:L31` keeps the raw claim name) | resource isolation is *by construction*: basket key = sub |

What juniors usually miss: there are two different auth artifacts alive at once — the **cookie** (WebApp session) and the **JWT** (API calls). Losing this distinction is the #1 junior auth confusion.

What seniors notice: authorization here is coarse (authenticated or not). There are no roles/policies on ordering endpoints; `GetOrdersByUserAsync` scopes by identity (`OrdersApi.cs:L93-L98`) but `GetOrderAsync(orderId)` — check it — fetches by id with **no ownership check** (`OrdersApi.cs:L80-L91`). *Investigate: can an authenticated user read another user's order by guessing an int id? Classic IDOR shape — see the security checklist.*

Interview angle: "Cookie vs token auth — when each?" and "What's an IDOR and where have you seen one?" You now have a concrete anchor for both.

Drill: list every claim the WebApp reads (grep `FindFirst` in `src/WebApp`), and for each, say what breaks if it's absent.

---

## Flow 6: Admin price change

Why this flow matters: it's the cleanest example of *conditional* event publication and the outbox pattern outside Ordering — and the repo's best "why do we need atomicity between DB write and message publish?" exhibit.

Open these files first:
- `src/Catalog.API/Apis/CatalogApi.cs:L324-L363` — `UpdateItem`
- `src/IntegrationEventLogEF/Services/IntegrationEventLogService.cs:L34-L44` — outbox save
- `src/Catalog.API/IntegrationEvents/` — `CatalogIntegrationEventService`

Trace:

| Step | Owner | File | What happens | Risk |
| --- | --- | --- | --- | --- |
| 1 | Catalog.API | `CatalogApi.cs:L330-L337` | Load item; 404 with ProblemDetails if absent | — |
| 2 | Catalog.API | `CatalogApi.cs:L340-L343` | `SetValues(productToUpdate)` — full overwrite from request body; embedding recomputed | mass-assignment shape: client controls every column |
| 3 | Catalog.API | `CatalogApi.cs:L345-L347` | EF change tracker asks: did `Price` change? | change detection drives business logic |
| 4a | (price changed) | `CatalogApi.cs:L350-L356` | Build `ProductPriceChangedIntegrationEvent` (with old price), save event + item **in one local transaction**, then publish | crash after commit, before publish → pending outbox row |
| 4b | (price same) | `CatalogApi.cs:L360` | Plain `SaveChangesAsync()` | no event noise |

Validation and authorization: *none* — no `[Authorize]`, no `RequireAuthorization()` on catalog writes. Anyone who can reach catalog-api can create/update/delete products. In this sample only the internal network can; still, this is the repo's most glaring **missing authorization boundary** and a first-class ticket (see `06-contribution-practice/01-good-first-tickets.md`).

What juniors usually miss: why bother with the event log table at all? Because `SaveChangesAsync` + `PublishAsync` as two separate steps can half-fail: price updated but no event (WebApp shows stale price warnings never fire), or event without update (consumers act on a price that never changed).

What seniors notice: who consumes `ProductPriceChangedIntegrationEvent`? Grep it. (Historically the basket price-update path; in this codebase check whether any subscription exists — if none, it's a *published-but-unconsumed* event, which is legal in pub/sub but worth flagging.)

Interview angle: "Explain the transactional outbox pattern" — answer with L350-L356 in front of you: event row + business row in one transaction, publish after commit, mark published, sweep failures.

Drill: write the failure matrix for UpdateItem: crash before commit / after commit before publish / after publish before mark-published. What state is each, and who fixes it?
Self-grade — Basic: three rows correct. Solid: notes the missing background dispatcher for `NotPublished` rows (`IntegrationEventLogService.cs:L19-L32` is only called with a transaction id, by the current request). Strong: designs the sweeper (poll `NotPublished`/`PublishedFailed`, exponential backoff, idempotent consumers make re-publish safe).
