# Annotation Drills

For each excerpt: open the anchor, and annotate **inputs, outputs, dependencies, invariants, side effects, failure modes** — six headings, in writing, before reading the notes. Then self-grade.

Rubric (applies to all drills):
- **Basic:** correct inputs/outputs/dependencies.
- **Solid:** plus at least one non-obvious invariant and every side effect (including logs and events).
- **Strong:** plus a failure mode the code does NOT handle, stated with the triggering condition.

---

## Drill 1 — `RedisBasketRepository.UpdateBasketAsync`
Anchor: `src/Basket.API/Repositories/RedisBasketRepository.cs:L34-L48`.
Notes after annotating: output is the basket *re-read from Redis*, not the input echoed — one extra round trip buys read-your-write confirmation. Invariant: key = `/basket/{BuyerId}`. Failure modes worth having found: `StringSetAsync` returning false is treated as "not created" and logged at Information (not Warning) with a vague message; null return propagates into a gRPC NotFound (`BasketService.cs:L51-L54`) — is "Redis write failed" really "basket does not exist"? No.

## Drill 2 — `Order.AddOrderItem`
Anchor: `src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs:L71-L91`.
Notes: invariants — one line per product (merge), discount only ratchets *up* on merge, units accumulate. Side effects: none outside the aggregate (that's the point). Failure mode to find: `SingleOrDefault` throws if the invariant is already violated (two lines, same product) — self-healing? no, self-*detecting*. Also: merging ignores the new line's `unitPrice` — first price wins; a price change between two adds is silently discarded. Strong answers catch that.

## Drill 3 — `IdentifiedCommandHandler.Handle`
Anchor: `src/Ordering.API/Application/Commands/IdentifiedCommandHandler.cs:L39-L104`.
Notes: the ordering of `CreateRequestForCommandAsync` (L48) *before* `Send` (L87) matters — a crash between them leaves a request id with no order; a retry then returns "duplicate → success" for an order that never existed. Is that reachable? Only if the request record committed — which happens… when? (Trace: it saves via a DbContext inside the TransactionBehavior scope? Check `RequestManager` in `Ordering.Infrastructure/Idempotency/` — it calls SaveChanges itself. This is the drill's rabbit hole; chase it.) Failure mode: the catch-all at L99-L102.

## Drill 4 — `RabbitMQEventBus.OnMessageReceived`
Anchor: `src/EventBusRabbitMQ/RabbitMQEventBus.cs:L132-L181`.
Notes: inputs include *message headers* (trace context). Side effects: activity creation, handler execution, **ack always**. Invariant broken knowingly: at-least-once delivery ends where a handler throws. The `throw-fake-exception` test hook (L163-L166) is a built-in chaos lever — Strong answers propose using it in a test.

## Drill 5 — `BasketState.FetchBasketItemsAsync`
Anchor: `src/WebApp/Services/BasketState.cs:L117-L149`.
Notes: memoizes the *Task*. Dependencies: two services (basket, catalog) — a partial failure (catalog down) faults the cached task; does anything reset `_cachedBasket` after a fault? (Read: only mutations null it.) Failure mode: `catalogItems[item.ProductId]` at L135 throws `KeyNotFoundException` if a basket references a deleted product — realistic (baskets have no TTL, ticket 1!). This drill teaches cross-referencing two findings.

## Drill 6 — `GracePeriodManagerService.GetConfirmedGracePeriodOrders`
Anchor: `src/OrderProcessor/Services/GracePeriodManagerService.cs:L63-L93`.
Notes: inputs are *time and the DB*. Invariant: only Submitted orders qualify — enforced by SQL string, not by the domain. Failure modes: DB down → caught, logged, empty list (loop survives — good); RabbitMQ down → exception from `PublishAsync` propagates... to where? (Up through `CheckConfirmedGracePeriodOrders` into `ExecuteAsync` — does the loop die? Read L26-L36 and decide. That's the Strong finding.)

## Drill 7 — `CatalogApi.GetItemsBySemanticRelevance`
Anchor: `src/Catalog.API/Apis/CatalogApi.cs:L237-L289`.
Notes: graceful degradation — AI disabled or embedding null → falls back to name search (L245-L256). Side effects: none (read). Failure modes: `totalItems` counts ALL items but pages only items with embeddings (L259-L286) — total can exceed reachable results; debug logging path executes a *different query shape* than non-debug (L264-L286) — a Heisenbug factory worth flagging.

## Drill 8 — `Checkout.razor` code block
Anchor: `src/WebApp/Components/Pages/Checkout/Checkout.razor:L64-L130`.
Notes: `RequestId` minted in `PopulateFormWithDefaultInfo` (L94) — page load, not click; that's load-bearing for idempotency (Flow 3). Inputs: form + claims (address prefill L89-L93). Failure mode: `CardTypeId` hardcoded to 1 at L113 — what if card type 1 is removed from the DB? Follow it into `CreateOrderCommandValidator` (`NotEmpty` passes, value 1) → Buyer aggregate verification — where would it actually fail?

---

Transferable habit: the six headings are a *universal* reading protocol. Apply them to any function in any interview's code-reading round; interviewers grade exactly these dimensions whether they say so or not.
