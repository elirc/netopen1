# Pattern Catalog — 14 Cards

Recognition training: each card = problem → shape → real anchors → failure modes → when to use/avoid → interview angle → drill. Learn to *spot* these in any repo; name-dropping without recognition is how candidates fail deep-dives.

---

## Pattern 1: Transactional Outbox

Problem it solves: "save to my DB" and "publish an event" are two systems; either alone can fail, leaving them inconsistent.
General shape: write the event into a table **in the same DB transaction** as the business change; publish after commit; mark published; sweep failures.
Real example: `src/Catalog.API/Apis/CatalogApi.cs:L350-L356` (price change) with `src/IntegrationEventLogEF/Services/IntegrationEventLogService.cs:L34-L44`.
Second example: `src/Ordering.API/Application/Behaviors/TransactionBehavior.cs:L38-L52` (publish strictly after commit).
Why this implementation works: `UseTransaction` (`IntegrationEventLogService.cs:L40`) enlists the log write in the caller's transaction — atomicity by construction.
Failure modes: crash after commit before publish → row stuck `NotPublished`; **this repo has no background sweeper**, so stuck rows stay stuck (possible risk). Publish twice if crash after publish before mark → consumers must be idempotent.
Use it when: any DB-write-plus-message operation. Avoid it when: you have no DB in the operation (then use broker transactions or accept loss).
Interview angle: "How do you keep DB and queue consistent?" — the #1 distributed-systems screener. Answer with this card.
Drill: find the third user of the outbox (grep `IIntegrationEventLogService`) and diagram its states from `EventStateEnum.cs`.

## Pattern 2: Idempotent Command (request-id dedup)

Problem it solves: clients retry; networks duplicate; "create order" must not run twice.
General shape: client sends a stable request id; server records it transactionally; duplicates short-circuit to a canned response.
Real example: `src/Ordering.API/Application/Commands/IdentifiedCommandHandler.cs:L41-L48`; header intake at `OrdersApi.cs:L119-L136`; id minted once per checkout page load (`Checkout.razor:L94`).
Second example: `CreateOrderIdentifiedCommandHandler.CreateResultForDuplicateRequest` returns `true` (`CreateOrderCommandHandler.cs:L67-L70`) — duplicates look like success.
Why this implementation works: the request record commits in the same transaction as the order (TransactionBehavior wraps both), so there's no window where the id is recorded but the order isn't.
Failure modes: id generated per *click* instead of per *intent* defeats the whole thing; the catch block at `IdentifiedCommandHandler.cs:L99-L102` swallows failures — a failed command still leaves the request id recorded, so a *legitimate* retry is treated as duplicate. That's a real design wart to discuss.
Use when: any non-idempotent POST. Avoid when: operation is naturally idempotent (PUT-by-key) — then it's overhead.
Interview angle: "How do you make an API idempotent?" Junior says "check if it exists." Mid says "client-supplied key, stored atomically with the write." Senior adds the failed-attempt-then-retry wart above.
Drill: trace what a retry sees if the first attempt failed validation. (Hint: request id recorded at L48 *before* mediator send… but is that inside the transaction? Verify.)

## Pattern 3: Aggregate Root (DDD)

Problem it solves: invariants that span multiple objects (order + items) get violated when anyone can mutate any object.
General shape: one root entity owns the object graph; all mutations go through root methods; collections exposed read-only.
Real example: `src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs:L31-L33` (private list, `AsReadOnly`), `:L71-L91` (`AddOrderItem` merges duplicates, keeps best discount).
Second example: Buyer aggregate, `AggregatesModel/BuyerAggregate/Buyer.cs` (payment-method verification).
Why it works: EF Core maps the private field, so persistence doesn't force public setters; invariants live in exactly one place.
Failure modes: anemic drift (logic leaking into handlers), aggregates too big (whole catalog as one aggregate = lock contention), cross-aggregate transactions (the rule: reference other aggregates by id — see `BuyerId int?` at `Order.cs:L14`).
Use when: real invariants exist. Avoid when: CRUD with no rules — Catalog.API correctly does *not* use aggregates.
Interview angle: "What's an aggregate and how big should it be?" — answer: consistency boundary = transaction boundary, with `Order.cs` as your example.
Drill: try to add an `OrderItem` from outside the aggregate. Write down every compiler error; each one is the pattern working.

## Pattern 4: Domain Events (dispatch-before-save)

Problem it solves: "when an order is created, also create/verify the buyer" without the command handler knowing about buyers.
General shape: entities queue events; the unit-of-work dispatches them; handlers mutate state in the *same* transaction.
Real example: `Order.cs:L61-L64` queues `OrderStartedDomainEvent`; `OrderingContext.SaveEntitiesAsync` (`OrderingContext.cs:L47-L62`) dispatches via `MediatorExtension.cs:L5-L20` **before** `SaveChangesAsync` — the file's own comment explains choice A vs B.
Second example: each status setter queues its event (`Order.cs:L103, L112, L123`).
Failure modes: handlers that do I/O (email!) inside the transaction stretch it; event handlers raising events → dispatch loops (this impl dispatches once — events raised *during* dispatch may be missed; *investigate*).
Use when: side effects must be atomic with the trigger. Avoid when: side effect can/should be eventually consistent → integration event instead.
Interview angle: "domain event vs integration event" — same-transaction/in-process vs after-commit/cross-service. eShop is the canonical citation.
Drill: list every `AddDomainEvent` call in Order.cs and match each to its handler in `Ordering.API/Application/DomainEventHandlers/`.

## Pattern 5: CQRS-lite (commands via MediatR, queries direct)

Problem it solves: write paths need invariants and transactions; read paths need shaped DTOs, fast.
General shape: commands → mediator pipeline → aggregate → repository; queries → thin query class → DB → DTOs, bypassing the domain.
Real example: commands in `Ordering.API/Application/Commands/`; queries in `Ordering.API/Application/Queries/` consumed at `OrdersApi.cs:L84, L96`.
Second example: `GetOrderAsync` returns a query-side `Order` DTO (aliased at `OrdersApi.cs:L3`), not the domain Order.
Why it works: the read model can join/flatten freely without polluting the aggregate.
Failure modes: over-CQRS (separate read DBs, event sourcing) when a joined query would do; duplicated shapes drifting.
Use when: domain writes are complex. Avoid when: Catalog-style CRUD — note Catalog.API has no mediator, and that asymmetry is *correct*.
Interview angle: "Do you always use CQRS?" — strong answer: "eShop uses it only in Ordering; Catalog is plain CRUD. Pattern where the invariants are."
Drill: find where query-side `Order` DTO is defined and compare field-by-field with the aggregate.

## Pattern 6: Pipeline Behaviors (decorator middleware for commands)

Problem it solves: logging, validation, transactions repeated in every handler.
General shape: ordered decorators around handlers (MediatR `IPipelineBehavior`).
Real example: `LoggingBehavior`, `ValidatorBehavior.cs:L20-L34` (throws on failures), `TransactionBehavior.cs` — all in `Ordering.API/Application/Behaviors/`.
Second example: HTTP equivalent is ASP.NET middleware (`app.UseStatusCodePages()` in `Catalog.API/Program.cs:L19`).
Failure modes: hidden ordering dependencies (validation MUST precede transaction); behaviors doing too much; exceptions in behaviors masking handler results.
Interview angle: "Where do cross-cutting concerns go?" Both web middleware and mediator pipelines are decorator chains — say that sentence and you sound senior.
Drill: find the registration that orders these behaviors (grep `AddOpenBehavior` in `Ordering.API/Extensions/`). What happens if the order flips?

## Pattern 7: Integration Events over a broker (pub/sub, routed by type name)

Problem it solves: services must react to each other without synchronous coupling.
General shape: publish JSON to an exchange with routing key = event class name; each service has one durable queue bound per subscribed event.
Real example: `RabbitMQEventBus.cs:L31-L111` (publish), `:L226-L295` (consume setup), subscriptions declared per service (`Basket.API/Extensions/Extensions.cs:L18-L20`, `Catalog.API/Extensions/Extensions.cs:L31-L33`, `WebApp/Extensions.cs:L43-L51`).
Failure modes: **ack-on-exception drops messages** (`RabbitMQEventBus.cs:L177-L180` — the code comments say use a DLX in production); type-name routing means class renames = silent unsubscription; no schema registry — payload drift is discovered at deserialize time.
Use when: cross-service facts. Avoid when: you need a reply (that's RPC — use gRPC/HTTP, like WebApp→Basket).
Interview angle: "at-least-once vs at-most-once": this bus is at-most-once on handler failure (ack anyway) but at-least-once on redelivery before ack — being able to say *which* is a differentiator.
Drill: diagram exchange → queues → bindings for a system with all services running (one queue per service; which events bind where?).

## Pattern 8: Guarded State Machine

Problem it solves: distributed events arrive late, twice, or out of order; state must only move forward.
General shape: transitions check current state; illegal jumps throw or no-op.
Real example: `Order.cs:L99-L128` (no-op guards on Submitted/AwaitingValidation/StockConfirmed), `:L130-L153` (throwing guards for Ship/Cancel).
Second example: outbox states `EventStateEnum` NotPublished→InProgress→Published/Failed.
Why it works: duplicate `GracePeriodConfirmed` events (which the poller *will* send — it re-queries every cycle) hit the `if (OrderStatus == Submitted)` guard and become no-ops.
Failure modes: silent no-ops hide bugs (SetPaid on a Cancelled order does nothing and nobody logs it — *possible observability gap*); the inconsistency between throwing vs silent guards in the same class is worth critiquing.
Interview angle: "How do you handle out-of-order events?" — state guards + idempotent transitions, not message ordering guarantees.
Drill: make a table of all 6 statuses × all 6 setters: throw / transition / silent no-op. Three minutes; you now know the machine better than most contributors.

## Pattern 9: Typed HTTP/gRPC Clients with delegating handlers

Problem it solves: every call site re-building base URLs, auth headers, API versions.
General shape: register a named/typed client once with base address, version, auth token handler; inject the typed client.
Real example: `WebApp/Extensions.cs:L31-L40` (`AddGrpcClient` + two `AddHttpClient` with `.AddApiVersion` and `.AddAuthToken()` — implemented in `eShop.ServiceDefaults/HttpClientExtensions.cs`).
Failure modes: singleton services capturing a typed client with per-user state; forgetting the auth handler on a new client (calls mysteriously 401).
Interview angle: `HttpClient` lifetime management ("socket exhaustion") is a classic .NET question — `IHttpClientFactory` via `AddHttpClient` is the answer, and you can point at this file.
Drill: follow `.AddAuthToken()` into ServiceDefaults and explain where the token comes from per request.

## Pattern 10: Backend-for-Frontend (YARP mobile-bff)

Problem it solves: mobile clients shouldn't juggle N service endpoints, CORS, and versions.
General shape: a reverse proxy exposing one surface, routing to internal services.
Real example: `eShop.AppHost/Program.cs:L60-L62` + route config in `eShop.AppHost/Extensions.cs` (`ConfigureMobileBffRoutes`).
Second example: the WebApp's image forwarder `MapForwarder` (`WebApp/Program.cs:L32`) — a one-route mini-BFF.
Failure modes: BFF accretes business logic (it must stay dumb); one more hop of latency; auth token relay misconfig.
Interview angle: "How do mobile apps talk to microservices?" BFF is the expected answer; you've seen a real one.
Drill: read `ConfigureMobileBffRoutes` and list the exposed route prefixes and their targets.

## Pattern 11: Options Pattern (typed config)

Problem it solves: stringly-typed `Configuration["..."]` scattered everywhere.
General shape: POCO bound to a config section, injected as `IOptions<T>` / `IOptionsMonitor<T>`.
Real example: `Catalog.API/Extensions/Extensions.cs:L35-L36` (`AddOptions<CatalogOptions>().BindConfiguration(...)`).
Second example: `PaymentProcessor` uses `IOptionsMonitor<PaymentOptions>` (`OrderStatusChangedToStockConfirmed...Handler.cs:L5,L21`) — *Monitor*, so flipping `PaymentSucceeded` at runtime changes behavior without restart.
Failure modes: reading `IOptions<T>` (snapshot at startup) when you needed live reload; validation absent (garbage config discovered at use time — consider `ValidateOnStart`).
Interview angle: minor but reliable .NET screener: "difference between IOptions, IOptionsSnapshot, IOptionsMonitor."
Drill: find every `IOptions*` use (grep) and justify each variant choice.

## Pattern 12: BackgroundService worker (poll → act)

Problem it solves: time-based work with no user request (grace-period expiry).
General shape: `BackgroundService.ExecuteAsync` loop with delay + cancellation token.
Real example: `OrderProcessor/Services/GracePeriodManagerService.cs:L16-L42`.
Failure modes: unobserved exceptions killing the loop silently (here the SQL is try/caught, `:L87-L92`, so the loop survives — good); `Task.Delay` drift; polling frequency vs load; **duplicate work when scaled to 2+ replicas** (no leader election — each replica would publish duplicate GracePeriodConfirmed events; consumers' guards absorb it, but it's wasteful).
Interview angle: "How do you run scheduled jobs in .NET?" and the follow-up "what happens when you scale it out?" — you have the exact anchor for both.
Drill: what happens if RabbitMQ is down during `PublishAsync`? Follow the exception path from `:L59` outward.

## Pattern 13: Aspire Composition Root / infrastructure-as-code-in-C#

Problem it solves: docker-compose sprawl, connection-string plumbing, service startup ordering.
General shape: one AppHost declares resources; `WithReference` injects config; `WaitFor` orders startup.
Real example: `eShop.AppHost/Program.cs` throughout; note the deliberate cycle handling for identity callbacks (L96-L101) — you can't `WithReference` a cycle, so raw env vars are used.
Failure modes: dev/prod parity drift (Aspire dev vs azd/K8s prod manifests); hidden coupling in env var names (`Identity__Url` must match the config path in code).
Interview angle: "How do you run 8 services locally?" — a modern, concrete answer beats "docker-compose" in .NET shops.
Drill: add (on paper) a new worker service that needs Redis + the bus: which 3 lines in AppHost?

## Pattern 14: Versioned Minimal APIs

Problem it solves: evolving a public contract without breaking existing clients.
General shape: version-set route groups; v1 and v2 handlers side by side; clients pin a version.
Real example: `CatalogApi.cs:L15-L18` (groups), `:L21-L30` (two `/items` versions), `:L93-L102` (UpdateItem v1 body-id vs v2 route-id); WebApp pins 2.0 (`WebApp/Extensions.cs:L35`), Ordering client pins 1.0 (L39).
Failure modes: v1 handlers silently delegating to v2 logic drift apart; version in URL vs header vs query inconsistencies; forgetting deprecation headers (here `ReportApiVersions = true`, `Catalog.API/Program.cs:L7-L11`).
Interview angle: "How do you version an API?" — show the v1→v2 UpdateItem change (id moved from body to route) as a real example of *why*: better REST semantics, idempotent PUT by key.
Drill: write the request line for both UpdateItem versions and explain which is more cache/proxy-friendly and why.

---

Recognition drill (whole catalog): pick any other repo you know. For each of the 14 cards, write "present at <path>", "absent — because…", or "present but degraded — how". That exercise *is* the mid-level interview.
