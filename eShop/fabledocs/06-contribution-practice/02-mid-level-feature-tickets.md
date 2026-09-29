# Mid-Level Feature Tickets

Rule: write a half-page **design note first** (approach, alternatives rejected, risk, rollback) and review it against the acceptance criteria before typing code. That habit — design-before-diff — is the observable difference between junior and mid.

## Ticket M1: Outbox sweeper service
Skills: hosted services, outbox, idempotency. Est: 2–3 days.
Story: as an operator, crash-orphaned integration events (R2) must eventually publish.
Anchors: `IntegrationEventLogService.cs:L19-L32` (needs a new query: pending-by-age, not by-transaction), `EventStateEnum.cs`, publishers in Catalog + Ordering.
Design questions your note must answer: sweep interval? max retries before `PublishedFailed` is terminal? multiple replicas racing (row locking / `FOR UPDATE SKIP LOCKED`)? does re-publish break any consumer (audit each — they're guarded; *prove* it, don't assert it).
Risk: double-publish storms if marking-published fails repeatedly. Rollback: feature-flag the hosted service; disabling it returns to today's behavior.
Tests: unit (query selects only stale NotPublished), integration (kill broker, create order, restart broker, assert delivery).
Interview story potential: "Designed and shipped the missing half of an outbox implementation" — a top-tier reliability story.

## Ticket M2: Dead-letter exchange for failed messages
Skills: RabbitMQ topology, failure design. Est: 2–3 days. Fixes R1.
Anchors: `RabbitMQEventBus.cs:L170-L180` (stop acking failures), `:L254-L263` (queue declaration gains DLX args).
Design note must answer: retry N times before DLX or straight to DLX? (Kata 5 shows naive requeue is a hot loop.) Who consumes the DLX (alerting? redrive tool?)? Is the change backward-compatible with existing queues (RabbitMQ won't redeclare a queue with different args — **migration plan required**: new queue name or delete-and-recreate window).
Rollback: config flag selecting old behavior.
Interview story: "Changed message-failure semantics in a live topology, including the queue-migration gotcha" — the gotcha is the story.

## Ticket M3: Ownership check on GET /api/orders/{orderId}
Skills: authZ, CQRS queries, API contracts. Est: 1 day. Resolves R5.
Anchors: `OrdersApi.cs:L80-L91`, `Application/Queries/OrderQueries.cs`, identity via `OrderServices.IdentityService`.
Design note: 404 vs 403 (404 — don't confirm existence); admin/support override? (out of scope, note it); does the WebApp ever fetch orders it doesn't own (webhooks client?) — audit callers first.
Tests: functional with two identities; unit on the query filter.
Interview story: "Found and closed an IDOR in an order API, with the caller audit that made it safe to ship."

## Ticket M4: Cancel-order button in the storefront
Skills: full-stack feature, Blazor, existing API. Est: 2 days.
Anchors: API exists (`OrdersApi.cs:L11`, `CancelOrderCommand`); UI `WebApp/Components/Pages/User/Orders.razor`; client `WebApp/Services/OrderingService.cs`.
Design note: which statuses show the button (mirror the domain guard `Order.cs:L142-L153` — but *don't duplicate the rule*: derive from status list or let the API refuse); optimistic UI vs wait-for-event (order status updates arrive via the bus subscription — use it).
Risk: race — user cancels as payment succeeds; the domain guard wins; UI must render the refusal gracefully.
Interview story: "Shipped a full-stack feature against an event-sourced status flow, handling the cancel/pay race."

## Ticket M5: Response caching + ETags on catalog reads
Skills: HTTP caching, middleware. Est: 2 days.
Anchors: `CatalogApi.cs:L124-L159` (list), `:L205-L224` (pics — already sets lastModified! extend to If-Modified-Since handling — check what `PhysicalFile` gives you free).
Design note: cache key must include version + query params; invalidation on item update (event-driven purge vs short TTL — argue TTL first for simplicity); what's *incorrect* to cache (per-user anything — nothing here, it's anonymous).
Interview story: "Added HTTP-correct caching with an invalidation story, and knew what not to cache."

## Ticket M6: Idempotency for basket updates via If-Match/version
Skills: concurrency, gRPC contract evolution. Est: 2–3 days. Fixes Flow 2's lost update.
Anchors: `RedisBasketRepository.cs:L34-L48`, `basket.proto` (additive field: `int64 version`).
Design note: optimistic concurrency (version check via Lua/WATCH) vs server-side delta ops (`AddItem` RPC) — the note must compare both and pick delta ops or justify otherwise; proto evolution rules (new field, never renumber).
Rollback: new RPC alongside old — old path untouched.
Interview story: "Fixed a read-modify-write race across a gRPC boundary with a contract-compatible change."

## Ticket M7: Structured audit log for admin catalog mutations
Skills: middleware, cross-cutting concerns. Est: 1–2 days. (Pairs with ticket 3's auth.)
Design note: what's logged (who/what/before-after price), where (structured log + trace tag vs DB table), and PII discipline.
Interview story: "Added an audit trail to write endpoints as part of hardening a service."

## Ticket M8: `TimeProvider` for testable time
Skills: refactoring, .NET 8+ APIs. Est: 2 days.
Anchors: `Order.cs:L58` (`DateTime.UtcNow`), grace-period SQL comparison, checkout card expiry (`BasketState.cs:L102`).
Design note: inject `TimeProvider` where DI reaches; the aggregate can't take DI — options: pass time into the ctor (contract change) vs ambient default with test override; discuss honestly. Scope: Ordering only.
Tests: the previously-unwritable test "order older than grace period is picked up" becomes writable — write it.
Interview story: "Made time injectable across a service and unlocked a class of tests."

## Ticket M9: Consumer-driven contract test for CreateOrderRequest
Skills: contract testing. Est: 1–2 days. Pairs with ticket 10 (the duplicated record, R9).
Design note: snapshot the serialized shape from WebApp's copy; assert Ordering's binder accepts it (functional test posting the WebApp-serialized JSON). Where does the test live so *both* sides' CI would catch drift? (Honest answer in one repo: one functional test project referencing both — note the coupling.)
Interview story: "Protected a hand-duplicated cross-service contract with a drift test."

## Ticket M10: Order status page — remove bus dependency from WebApp (spike)
Skills: architecture spike, written recommendation. Est: 2 days, output is a doc not code.
Anchors: `WebApp/Extensions.cs:L43-L51`, `OrderStatusNotificationService`, `OrdersRefreshOnStatusChange.razor`.
Task: evaluate replacing the WebApp's RabbitMQ subscription with (a) polling the ordering API, (b) SignalR pushed from Ordering, (c) status quo. Deliver a one-page recommendation with the scaling analysis (multi-node WebApp = N durable queues? competing consumers eating each other's notifications? — investigate how `SubscriptionClientName` is set for WebApp).
Interview story: "Wrote the spike that decided how order notifications scale" — spikes make *great* interview stories because they're pure judgment.
