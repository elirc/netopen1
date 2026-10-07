# Implicit ADRs — Reverse-Engineered from the eShop Codebase

Ten Architecture Decision Records the authors never wrote down but demonstrably made. Each is grounded in code read on 2026-07-16 at commit `9b4f943` (line anchors verified at read time; see `../fabledocs/09-reference/verification-log.md`). "Status" reflects what the code and its comments say, not an official record.

An ADR reconstructed from code is an inference: the *Decision* is fact (the code exists), the *Context* and *Alternatives Considered* are informed reconstruction. Where the authors left comments confirming intent, those are quoted.

---

## ADR-001: One repository, many deployables, with an Aspire AppHost as the composition root

**Context.** The system comprises 7+ runnable services (WebApp, Catalog, Basket, Ordering, Identity, Webhooks, two workers), three infrastructure dependencies (Postgres, Redis, RabbitMQ), and cross-cutting concerns (telemetry, discovery, health). Developers need to run all of it locally with one command; the topology (who talks to whom, who waits for whom) must live somewhere authoritative.

**Decision.** Keep everything in a single solution (`eShop.slnx`: 19 source projects plus 5 test projects) that deploys as independent services, and encode the entire runtime topology in a .NET Aspire AppHost project: `src/eShop.AppHost/Program.cs` declares every container, database, service, dependency edge (`WithReference`), startup ordering (`WaitFor` — e.g., OrderProcessor waits for Ordering.API "because that contains the EF migrations", L46-L49), and even the cyclic identity-callback wiring that references can't express (L96-L101). Cross-cutting defaults are centralized in `src/eShop.ServiceDefaults` (OTel, health endpoints, service discovery, default JWT auth), consumed by every service via `AddServiceDefaults()`.

**Alternatives considered.** (a) Polyrepo per service — maximal team autonomy, but for a system meant to be cloned and run whole, coordination costs dominate. (b) docker-compose + per-service config files — the pre-Aspire norm; topology scattered across YAML and connection strings duplicated per service. (c) A true monolith — abandons the microservices teaching goal.

**Consequences.**
- (+) `dotnet run --project src/eShop.AppHost` boots the world; the AppHost file doubles as an always-accurate architecture diagram.
- (+) Connection strings and service URLs are injected, not hardcoded — services reference logical names like `https+http://catalog-api` (`src/WebApp/Extensions/Extensions.cs:L34`).
- (+) Atomic cross-service changes (one PR can change an event contract and both its ends) — with the matching risk that nothing *forces* you to keep services independently deployable.
- (−) Dev/prod parity gap: Aspire orchestrates dev; production (azd/Container Apps) is a different deployment path that can drift.
- (−) The filtered solution `eShop.Web.slnf` exists because the full solution needs MAUI workloads — monorepo breadth taxes every build.

**Status.** Accepted; actively maintained (recent commits track Aspire 13.x upgrades).

---

## ADR-002: Database-per-service on one Postgres server; Redis for basket state

**Context.** Microservices lose their independence if they share tables. But this is a sample meant to run on a laptop — four Postgres *servers* would be waste.

**Decision.** One Postgres container hosts four isolated databases — `catalogdb`, `identitydb`, `orderingdb`, `webhooksdb` (`src/eShop.AppHost/Program.cs:L15-L18`) — each owned exclusively by one service. Ordering additionally namespaces itself under a `ordering` schema (`src/Ordering.Infrastructure/OrderingContext.cs:L37`). The basket lives in Redis as one JSON document per user, key `/basket/{sub}` (`src/Basket.API/Repositories/RedisBasketRepository.cs:L13-L16`), with no TTL. Cross-service "joins" are replaced by data duplication: `OrderItem` snapshots product name/price/picture at purchase time (`Order.cs:L71-L91`) rather than referencing the catalog.

**Alternatives considered.** (a) Shared database — simpler queries, but couples schema migrations across services and invites cross-service joins. (b) Physical server per service — real production isolation, pointless locally. (c) Basket in Postgres — durable, but the basket is ephemeral, per-user, whole-document read/write — a textbook cache-store workload.

**Consequences.**
- (+) Schema changes are service-local; ownership is unambiguous (the ownership map is enforceable by connection string).
- (+) Receipts are immutable by construction — the snapshot means marketing renaming a product doesn't rewrite history.
- (−) Logical isolation only: one server down degrades everything; the isolation is a *migration path*, not a failure domain.
- (−) The rule is already bent once: OrderProcessor reads `ordering.orders` with raw SQL (`GracePeriodManagerService.cs:L69-L74`) — a documented-by-code trespass that migrations won't flag.
- (−) No TTL on Redis keys means unbounded growth and stale product references (a deleted product crashes basket hydration at `BasketState.cs:L135`).

**Status.** Accepted; the OrderProcessor trespass is a deliberate, undocumented exception.

---

## ADR-003: Services coordinate by choreographed events over RabbitMQ, not synchronous calls

**Context.** Checkout spans four services (Ordering, Catalog stock, Payment, Basket). Synchronous chains (Ordering → Catalog → Payment) couple availability: any dependency down fails checkout, and distributed transactions across services are off the table.

**Decision.** Order workflow progress happens exclusively through integration events on a RabbitMQ direct exchange (`eshop_event_bus`), routed by **event class name** (`RabbitMQEventBus.cs:L33`), one durable queue per service (`:L258-L263`). There is no saga orchestrator: each service reacts to facts and publishes new facts (choreography). Ordering never calls Catalog; stock validation is a Catalog reaction to `OrderStatusChangedToAwaitingValidation` (`Catalog.API/IntegrationEvents/EventHandling/OrderStatusChangedToAwaitingValidationIntegrationEventHandler.cs:L15-L32`). Where a synchronous answer *is* required (UI reading the basket), a direct call is used instead (ADR-007). Time-based progress uses a polling worker (`GracePeriodManagerService`), and even the WebApp subscribes to the bus for live status updates (`WebApp/Extensions.cs:L43-L51`).

**Alternatives considered.** (a) Synchronous REST chains — simpler mental model, availability coupling. (b) Orchestrated saga (a coordinator owning the workflow) — the workflow would be legible in one file, at the cost of a new central component; the authors chose implicit choreography. (c) A heavier broker abstraction (MassTransit/NServiceBus) — retries/DLQ/sagas for free, but hides the mechanics this sample exists to teach.

**Consequences.**
- (+) Failure isolation: Catalog down means orders queue in AwaitingValidation instead of checkout 500s.
- (+) New reactions are additive — the WebApp added itself as a consumer without touching any publisher.
- (−) The workflow is invisible: "where is checkout defined?" has no answer shorter than six files.
- (−) Class-name routing makes an event rename a silent cross-service break — convention, not compiler, holds the widest contract.
- (−) Eventual consistency is user-visible (order shows "Submitted" until workers act), and compensation, not rollback, handles failure (`Order.SetCancelledStatusWhenStockIsRejected`, `Order.cs:L155-L168`).

**Status.** Accepted.

---

## ADR-004: Transactional outbox for every DB-write-plus-publish operation

**Context.** Given ADR-003, services constantly need to "save state AND announce it." Two independent systems (Postgres, RabbitMQ) cannot be updated atomically; naive sequential writes leave the system inconsistent whenever a process dies between them (the dual-write problem).

**Decision.** A shared library, `src/IntegrationEventLogEF`, persists events into an `IntegrationEventLog` table *inside the same database transaction* as the business change (`IntegrationEventLogService.cs:L34-L44`, enlisting via `UseTransaction`), then publishes after commit and marks state (`NotPublished → InProgress → Published/Failed`). Ordering wires this into the MediatR `TransactionBehavior` — commit first, `PublishEventsThroughEventBusAsync(transactionId)` strictly after (`TransactionBehavior.cs:L38-L52`). Catalog uses it selectively: a price change saves event+entity in one local transaction (`CatalogApi.cs:L347-L357`). Stateless publishers (PaymentProcessor, OrderProcessor) skip the outbox — they have no DB write to keep consistent, and the poller self-heals lost publishes by re-deriving from the DB each cycle.

**Alternatives considered.** (a) Publish-then-save or save-then-publish — simpler, and wrong under crashes. (b) Two-phase commit across DB and broker — heavyweight, poorly supported. (c) CDC/Debezium reading the WAL — production-grade, operationally heavy for a sample.

**Consequences.**
- (+) The dual-write problem simply doesn't exist here; the rule "outbox iff a DB write coexists" is applied coherently across services.
- (+) Event state is queryable — failures leave rows, not mysteries.
- (−) **Half-built:** nothing sweeps orphaned rows. `RetrieveEventLogsPendingToPublishAsync` is only ever called with the *current* transaction id (`IntegrationEventLogService.cs:L19-L32`); a crash after commit but before publish strands the event as `NotPublished` forever.
- (−) Publish-after-commit means possible double-publish (crash before mark-published), which is why ADR-006's consumer idempotency is load-bearing, not optional.

**Status.** Accepted, incomplete by design (sample); the missing dispatcher is the highest-value extension.

---

## ADR-005: Rich DDD/CQRS in Ordering only; plain CRUD everywhere else

**Context.** Ordering has genuine invariants: a state machine (Submitted→…→Shipped), aggregate consistency (order items, best-discount merging), money. Catalog is lookup tables with filters. Uniform architecture would over-engineer one side or under-engineer the other.

**Decision.** Ordering gets the full treatment: a framework-free domain project (`Ordering.Domain` references neither EF nor ASP.NET; invariants in the `Order` aggregate root with a private, read-only-exposed item collection, `Order.cs:L31-L33, L71-L91`), MediatR commands with a pipeline (Logging → Validator → Transaction, registration order fixed at `Ordering.API/Extensions/Extensions.cs:L39-L41`), domain events dispatched *before* save so handler effects join the same transaction (`OrderingContext.SaveEntitiesAsync`, `OrderingContext.cs:L47-L62` — the comment there explicitly weighs option A vs B), and a separate query side. Catalog, by contrast, is static-method minimal APIs hitting `DbContext` directly (`CatalogApi.cs`), no mediator, no repositories. Notably the CQRS is *lite*: `OrderQueries` reuses the same EF `OrderingContext` and hand-maps to DTOs (`OrderQueries.cs:L3-L35`) — no Dapper, no read database.

**Alternatives considered.** (a) DDD everywhere — ceremony for Catalog's CRUD, the classic sample-app disease. (b) CRUD everywhere — order invariants scattered across handlers, the anemic-domain disease. (c) Full CQRS with separate read store/event sourcing — unjustified by any query need present.

**Consequences.**
- (+) The most valuable logic in the system is the cheapest to test — `OrderAggregateTest.cs` needs zero mocks.
- (+) The asymmetry itself teaches judgment: pattern weight proportional to invariant richness.
- (−) Two architectural dialects in one repo raise onboarding cost; contributors must know which side they're on.
- (−) MediatR indirection: answering "who handles CreateOrderCommand?" requires tooling, not reading.
- (−) A visible seam: DbContext pooling is disabled because the two-constructor OrderingContext can't be pooled (comment at `Ordering.API/Extensions/Extensions.cs:L12-L18`) — a real cost paid for injecting IMediator into the context.

**Status.** Accepted. The strongest deliberate decision in the codebase.

---

## ADR-006: Idempotency via client-supplied request IDs plus state-guarded transitions

**Context.** ADR-003/004 guarantee at-least-once delivery; browsers double-click; networks retry. "Create order" and every state transition must tolerate duplicates.

**Decision.** Two complementary mechanisms. (1) At the API edge: commands arrive wrapped in `IdentifiedCommand<T,R>` carrying a client GUID from the `x-requestid` header (`OrdersApi.cs:L118-L146`); `IdentifiedCommandHandler` checks a `requests` table and short-circuits duplicates to a canned result — for create-order, `true` (`CreateOrderCommandHandler.cs:L67-L70`). The GUID is minted once per checkout *intent* — at page initialization, not per click (`Checkout.razor:L94`). The dedup record commits inside the same transaction as the order (TransactionBehavior wraps both). (2) In the domain: every status setter guards on current state — `SetAwaitingValidationStatus` no-ops unless Submitted (`Order.cs:L99-L106`) — so the grace-period poller re-publishing the same event every cycle (`GracePeriodManagerService.cs:L44-L61`) is harmless by construction. Naturally idempotent consumers (basket delete, `OrderStartedIntegrationEventHandler.cs:L10-L15`) need nothing.

**Alternatives considered.** (a) Server-generated dedup (hash of payload/time window) — false positives, no client intent signal. (b) Exactly-once via broker features — doesn't exist; "exactly-once effect" must be built at consumers regardless. (c) Distributed locks — heavier, and still needs the state guard for out-of-order arrivals.

**Consequences.**
- (+) Layered: edge dedup absorbs client retries; state guards absorb bus redeliveries and reordering; either surviving alone still protects the money path.
- (−) A confirmed wart: the catch-all in `IdentifiedCommandHandler.cs:L99-L102` records the request id even when the inner command *fails*, so a legitimate retry of a failed create is treated as a duplicate success (interacts with ADR-009).
- (−) Silent no-op guards hide misrouted events — a `SetPaidStatus` on a Cancelled order does nothing and logs nothing.

**Status.** Accepted; the failed-retry interaction is an open flaw.

---

## ADR-007: Transport chosen per audience — versioned REST public, gRPC internal, BFF for mobile, events for facts

**Context.** Different consumers have different needs: browsers and partners need cacheable, evolvable HTTP; the WebApp→Basket hop is chatty, internal, and typed; mobile apps shouldn't juggle N endpoints; peer services need fire-and-forget facts (ADR-003).

**Decision.** Four transports, each scoped: Catalog and Ordering expose **versioned REST** (route groups `HasApiVersion(1,0)/(2,0)`, `CatalogApi.cs:L15-L18`; clients pin versions centrally — WebApp pins Catalog v2.0 and Ordering v1.0, `WebApp/Extensions.cs:L34-L40`). Basket is **gRPC-only**, contract-first from `basket.proto`, and the proto deliberately carries no prices — quantity and product id only (`BasketService.cs:L77-L110`) so clients can never assert a price. Mobile gets a **YARP BFF** (`mobile-bff`, `eShop.AppHost/Program.cs:L60-L62`); the WebApp even runs a one-route mini-BFF forwarding product images (`WebApp/Program.cs:L32`). Cross-service facts ride the bus.

**Alternatives considered.** (a) REST everywhere — simplest, loses typed contracts on the hot internal hop. (b) gRPC everywhere — browsers can't speak it natively; partners want REST. (c) GraphQL for clients — one shape-flexible surface at the cost of caching/complexity; nothing here needs it.

**Consequences.**
- (+) Version pinning lives in DI registration, not call sites; v1 and v2 handlers coexist and v1 delegates to v2 logic (`GetAllItemsV1` → `GetAllItems`, `CatalogApi.cs:L116-L121`) — one implementation, two contracts.
- (+) The proto's missing price field is a security decision expressed as a contract (server re-resolves prices, `BasketState.cs:L117-L149`).
- (−) Four transports = four sets of auth wiring, error semantics, and debugging skills; the repo pays it to teach it — a real team should ask whether they need all four.
- (−) The v2 `/items` semantic-search variant exposes an inconsistency (total counts all items, page filters by embedding, `CatalogApi.cs:L259-L286`) — versioning multiplies surfaces to keep correct.

**Status.** Accepted.

---

## ADR-008: Response contracts as types; entity-as-contract tolerated in Catalog, DTO separation enforced in Ordering

**Context.** Minimal APIs need a convention for what endpoints return and how errors serialize; and each service must decide whether wire shapes are distinct types or reused persistence models.

**Decision.** Endpoints declare their full response surface as compile-checked unions — `Results<Ok<CatalogItem>, NotFound, BadRequest<ProblemDetails>>` (`CatalogApi.cs:L171`) — with RFC 7807 `ProblemDetails` as the error body (`AddProblemDetails`, `Catalog.API/Program.cs:L5`; explicit guard producing it at `CatalogApi.cs:L176-L181`). On shapes, the services split: **Catalog returns EF entities directly** (`PaginatedItems<CatalogItem>`, `CatalogApi.cs:L158` — DB shape = wire shape), while **Ordering maps aggregates to dedicated query DTOs** (`OrderQueries.cs:L15-L34` builds a flattened `Order` DTO; the API even aliases it to avoid confusion with the domain type, `OrdersApi.cs:L3`). Where a contract must cross the WebApp→Ordering boundary, it is *duplicated by hand* rather than shared via project reference (`CreateOrderRequest` in both `BasketState.cs:L158-L172` and `OrdersApi.cs:L171-L185`) — decoupled deploys valued over DRY.

**Alternatives considered.** (a) DTOs everywhere — safest, most boilerplate; Catalog's entities are innocuous *today*, so the tax was skipped. (b) Shared contracts assembly — compile-time sync at the cost of coupling WebApp and Ordering deployments. (c) OpenAPI-generated clients — the repo generates specs (`Catalog.API.json`) but hand-writes clients.

**Consequences.**
- (+) An endpoint's possible responses are readable from its signature and feed OpenAPI generation automatically.
- (+) Ordering's read DTOs decouple its wire shape from aggregate refactoring; note `UnitPrice` deliberately widens to `double` in the DTO (`OrderQueries.cs:L31`) — the DTO is a *presentation* contract.
- (−) Catalog's choice means any schema addition leaks to the wire by default (stock thresholds and embedding metadata already do), and mass-assignment-shaped writes exist (`SetValues(productToUpdate)`, `CatalogApi.cs:L340-L341`).
- (−) The duplicated `CreateOrderRequest` drifts silently — a missing field deserializes to a default, no error.

**Status.** Accepted, mixed-discipline; the Catalog side is the first thing to revisit if the API gains external consumers.

---

## ADR-009: Error-handling philosophy — typed and visible at HTTP edges, fail-open and log-only in the messaging core

**Context.** A teaching sample must keep the happy path legible; production-grade failure handling (DLQs, poison-message quarantine, retry budgets) adds machinery that obscures the lesson. A line had to be drawn.

**Decision.** At HTTP boundaries, failures are first-class: ProblemDetails bodies, typed NotFound/BadRequest results, validation failures thrown by `ValidatorBehavior` (`ValidatorBehavior.cs:L28-L34`), sensitive data masked before logging (card number masking, and the comment "don't log the request as it has CC number", `OrdersApi.cs:L124-L144`). In the messaging core, the opposite: consumer exceptions are logged and the message is **acked anyway** — with an in-code confession: "in a REAL WORLD app this should be handled with a Dead Letter Exchange (DLX)" (`RabbitMQEventBus.cs:L177-L180`). Transport-level publish failures get retries with exponential backoff, scoped to `BrokerUnreachableException`/`SocketException` only (`:L302-L320`) — retry transient faults, never business failures. Two deeper fail-opens: `IdentifiedCommandHandler` swallows all inner exceptions to `default` (`:L99-L102`), which surfaces as HTTP 200 for failed order creation (`OrdersApi.cs:L157-L166`), and `GetOrderAsync` maps *any* exception to 404 (`:L82-L90`).

**Alternatives considered.** (a) Full DLX + retry topology — correct, and the authors knowingly deferred it. (b) Fail-closed consumers (nack + requeue) — without a retry cap this hot-loops on poison messages, arguably worse than loss. (c) Result types instead of exceptions in the pipeline — cleaner contracts, more plumbing.

**Consequences.**
- (+) The demo never wedges: a bad message disappears rather than jamming the queue.
- (+) Where errors *are* surfaced, the patterns are exemplary (ProblemDetails, masked logging, exception→trace tags).
- (−) Confirmed failure modes: any handler bug silently freezes an order mid-state-machine; failed creates report success; a DB outage reads as "order not found." All three are invisible without log archaeology.
- (−) The philosophy is *inconsistent by layer*, and nothing but tribal knowledge tells a contributor which convention a new component should follow.

**Status.** Accepted for the sample, explicitly acknowledged as unsuitable for production in the code's own comments. Treat the messaging half as a documented TODO, not a model.

---

## ADR-010: Test where the invariants are — mock-free domain units, real-infrastructure functional tests, thin e2e; CI builds only

**Context.** Test strategy follows architecture: ADR-005 made the domain framework-free, and the persistence layer leans on Postgres-specific features (pgvector, schemas) that in-memory fakes cannot honestly represent.

**Decision.** Three layers, each shaped by what it verifies. (1) Domain/unit: MSTest suites exercising pure aggregates with zero mocks (`tests/Ordering.UnitTests/Domain/OrderAggregateTest.cs` — e.g., negative units throw `OrderingDomainException`, L31-L43), plus service-level tests with hand-rolled fakes (`tests/Basket.UnitTests`). (2) Functional: xUnit + `WebApplicationFactory` against **real containers** — the fixture builds a miniature Aspire app hosting pgvector Postgres and injects its live connection string (`tests/Catalog.FunctionalTests/CatalogApiFixture.cs:L17-L37`); `Program.Testing.cs` partials expose the entry points. (3) e2e: three Playwright specs (`e2e/`) covering browse/add/remove, with a login setup project and an HTTP-only mode env hook built into the AppHost for CI convenience (`ESHOP_USE_HTTP_ENDPOINTS`, `eShop.AppHost/Program.cs:L106-L115`). The public CI pipeline, meanwhile, only builds (`ci.yml:L44` — `dotnet build eShop.Web.slnf`); no test execution is wired there. Cross-service event flows (the ADR-003 choreography) have **no automated coverage** at all.

**Alternatives considered.** (a) Mocked `DbContext`/in-memory provider — fast and dishonest: passes tests that SQL translation would fail. (b) Full integration environment per PR (Testcontainers/compose in CI) — the fixtures are already 90% of this; the missing piece is CI wiring, likely omitted for public-pipeline cost/flakiness. (c) Heavy e2e coverage — slow and brittle; the suite instead keeps e2e to three journeys (and misses checkout, the money path).

**Consequences.**
- (+) Test cost tracks logic value: the richest rules run in milliseconds with no test doubles to drift.
- (+) Functional tests catch real-SQL and migration bugs (migrations auto-apply at startup, so the fixture exercises them implicitly).
- (−) A green public CI badge means "it compiles," nothing more.
- (−) The distributed workflow — the system's defining behavior — is verified only by running it and looking; the seams where ADR-009's failures hide are precisely the untested ones.
- (−) `DateTime.UtcNow` baked into the domain (`Order.cs:L58`) makes time-dependent rules (grace period) untestable as written.

**Status.** Accepted; the layer shapes are exemplary, the coverage gaps (CI execution, cross-service, checkout e2e) are real.

---

# Interview Translation

For each ADR: a ~90-second spoken answer (150–200 words — rehearse aloud), then the follow-up you should expect. The pattern every answer follows: *decision → why → tradeoff accepted → where I saw it bite.*

## ADR-001 — Monorepo + AppHost
**Say:** "The repo I know best keeps nineteen projects in one solution but deploys them as seven independent services, and the interesting decision is that the entire topology lives in code — a .NET Aspire AppHost declares every container, database, and dependency edge, including startup ordering like 'the order processor waits for the ordering API because that's where migrations run.' That file is an architecture diagram that can't go stale. The tradeoff: monorepos make cross-service changes atomic, which is convenient but also dangerous — nothing stops you changing an event contract and both its consumers in one PR, so independent deployability erodes unless you're disciplined. And there's a dev/prod parity risk: the orchestrator that runs your laptop isn't the one running production. I'd take this setup again for a team under ~30 engineers; past that, ownership boundaries start wanting repo boundaries."
**Follow-up to expect:** "How would you preserve independent deployability inside a monorepo?" (Answer direction: contract tests on event/API shapes, deploy pipelines per service, and a rule that contract changes ship backward-compatible.)

## ADR-002 — Database per service
**Say:** "Each service owns its database — four logical databases on one Postgres server, plus Redis for baskets. Owning means *exclusive*: no other service's connection string can reach your tables, so cross-service foreign keys are impossible by construction. The consequence people underestimate is data duplication as a feature: order lines snapshot the product name and price at purchase time, because your receipt shouldn't change when the catalog does. The tradeoffs I watched play out: one background worker cheats — it reads the ordering database directly with raw SQL to find expired orders, which is invisible to the compiler and to migrations; it's the kind of pragmatic leak you document and canary-test rather than eliminate. And 'four databases on one server' is logical isolation only — one failure domain. I'd call it the right first step with a clear path to physical isolation later."
**Follow-up:** "How do you run a report that joins orders with product data?" (Direction: you don't join live stores — replicate via events into a read model/warehouse, or accept the snapshot data already on the order.)

## ADR-003 — Event choreography
**Say:** "Checkout spans four services and they never call each other synchronously — everything moves by integration events on RabbitMQ. The order service publishes 'order awaiting validation,' catalog reacts with a stock check and publishes confirmed or rejected, payment reacts to that, and each transition is a fact another service consumes. That's choreography, no central orchestrator. What you buy is failure isolation — if catalog is down, orders queue up instead of checkout throwing 500s — and additive extension: the web frontend added itself as a consumer for live status updates without touching a single publisher. What you pay is legibility: there is no file where the checkout workflow is written down; I had to reconstruct it across six handlers. And events are routed by class name, so a rename is a silent cross-service break. For a workflow this linear I'd genuinely consider an orchestrated saga next time — choreography scales in flexibility, orchestration scales in auditability."
**Follow-up:** "An order is stuck mid-workflow — how do you find where and why?" (Direction: hop checklist through the trace — the system propagates OpenTelemetry context through the queue — then the ack-on-error gap from ADR-009.)

## ADR-004 — Transactional outbox
**Say:** "Anywhere a service writes to its database and needs to announce it, there's a dual-write problem: the DB commit and the message publish can't be atomic, so a crash between them either loses the event or announces something that never happened. This codebase solves it with a transactional outbox: the event is serialized into a log table *inside the same database transaction* as the business change, then published after commit and marked published. I can point at the price-change endpoint where the event row and the price update commit together. The accepted consequence is possible double-publish — crash after publishing but before marking — which is why every consumer downstream is idempotent; the outbox and consumer idempotency are one decision, not two. The gap I found: nothing re-publishes rows orphaned by a crash after commit — the sweeper is the missing half, and it's the first thing I'd build."
**Follow-up:** "Why not just publish first and then save?" (Direction: walk the crash matrix — every ordering of two non-atomic writes fails some way; only co-transactional persistence closes it.)

## ADR-005 — Selective DDD/CQRS
**Say:** "The most senior decision in that codebase is asymmetry: the ordering service gets full DDD — a framework-free domain project, an aggregate root that owns its item collection and enforces a status state machine, commands through a mediator pipeline with validation and transaction behaviors — while the catalog service is deliberately plain: static-method endpoints straight onto the DbContext. The reasoning is that pattern weight should track invariant richness. Orders have real rules — you can't cancel a shipped order, discounts merge in specific ways — and putting those in one aggregate makes them testable in milliseconds with zero mocks. The catalog is lookup tables; a repository-mediator sandwich there would be ceremony. Even the CQRS is proportionate — the query side reuses the same EF context and just maps to DTOs, no separate read store, because no query needed one. The cost is two dialects in one repo, so contributors need a rule for which side they're on."
**Follow-up:** "How big should an aggregate be?" (Direction: consistency boundary = transaction boundary; reference other aggregates by ID — the order holds a nullable BuyerId, not a Buyer graph.)

## ADR-006 — Idempotency layers
**Say:** "Order creation is protected against duplicates at two layers, and the layering is the point. At the edge, the client sends a request ID in a header — generated when the checkout *page loads*, not when the button is clicked, so a double-click or a network retry carries the same ID — and the server records it in the same transaction as the order; duplicates short-circuit to success. In the domain, every status transition is guarded by current state: 'set paid' does nothing unless the order is stock-confirmed. That second layer is what makes at-least-once delivery survivable — there's a poller that re-publishes the same event every cycle by design, and the guards just absorb it. The flaw I'd fix: the wrapper catches all exceptions and still records the request ID, so retrying a *failed* create gets treated as a duplicate success. Idempotency machinery interacting badly with error handling — that seam is where I'd focus review."
**Follow-up:** "Where does the idempotency key come from and what's its scope?" (Direction: per-intent not per-attempt; discuss key lifetime and collision handling.)

## ADR-007 — Transport per audience
**Say:** "The system uses four transports and I think each is defensible: versioned REST where contracts face humans and partners — catalog and orders, with v1 and v2 route groups coexisting and clients pinning versions in DI registration; gRPC on the one internal, chatty hop — the basket — where the proto is the contract; a YARP reverse-proxy BFF so mobile clients see one surface; and the message bus for facts between services. My favorite detail is a security decision hiding in a contract: the basket proto has no price field — clients physically cannot assert what something costs; the server re-resolves prices from the catalog. The cost of four transports is real: four auth wirings, four error semantics, four debugging skills. On a smaller team I'd collapse to two — REST plus events — and only add gRPC when a hop measurably needs it."
**Follow-up:** "How do you version the gRPC contract vs the REST one?" (Direction: proto field-number discipline and additive-only changes vs REST route-group versioning; events version additively too.)

## ADR-008 — Contracts as types
**Say:** "Endpoints declare their entire response surface in the type system — a handler returns a union like 'Ok of item, or NotFound, or BadRequest of ProblemDetails,' so the compiler and the OpenAPI doc both know every status it can produce, and errors are RFC-7807 problem details everywhere. On payload shapes the repo splits pragmatically: catalog returns its EF entities directly — cheap, and acceptable while the type has nothing sensitive, but it means every schema addition leaks to the wire by default, and I'd revisit it the day the API gets external consumers. Ordering does it properly — dedicated query DTOs mapped from the aggregate, so the wire shape survives domain refactoring. There's also one contract duplicated by hand between the frontend and the ordering API rather than shared as a package — that's a deliberate decoupling of deployments, and the mitigation it's missing is a serialization drift test, not a shared assembly."
**Follow-up:** "When is returning entities directly actually fine?" (Direction: internal-only consumers, no sensitive columns, and you've accepted schema=contract knowingly — plus the mass-assignment caveat on writes.)

## ADR-009 — Split error philosophy
**Say:** "The error handling has two personalities and knowing which you're in matters. At HTTP edges it's exemplary: typed results, problem-details bodies, validation as a pipeline stage, and card numbers masked before anything logs. In the messaging core it's fail-open: if an event handler throws, the message gets logged and *acknowledged anyway* — the code's own comment says a real system needs a dead-letter exchange. I confirmed two consequences: a handler bug silently freezes an order mid-workflow, and a swallowed exception in the command wrapper means a failed order creation returns HTTP 200. That taught me a durable lesson: error handling isn't a global policy, it's a per-boundary decision, and the failure modes concentrate exactly where handling is weakest. My first production change would be the DLX plus one business-level alert — 'no order stuck in a non-terminal state over fifteen minutes' — which catches lost messages, dead workers, and broker outages with a single rule."
**Follow-up:** "Why not just nack and requeue failed messages?" (Direction: poison-message hot loop; you need a retry cap and a DLX, and consumers stay idempotent because redelivery is now real.)

## ADR-010 — Test where invariants live
**Say:** "The test strategy mirrors the architecture. The domain is framework-free, so its invariants — negative quantities throw, illegal status transitions throw — are tested with pure objects, no mocks at all, in milliseconds. The functional tier refuses to fake the database: fixtures boot a real Postgres container with the pgvector extension and point the app at it, because a mocked DbContext passes tests that real SQL translation would fail. End-to-end is deliberately thin — three Playwright journeys. The gaps are as instructive as the shape: the public CI pipeline only *builds*, so a green badge means it compiles; the cross-service event choreography — the system's defining behavior — has no automated coverage; and checkout, the money path, has no e2e spec. If I owned it, my first test investment would be exactly there: one functional test per event consumer under duplicate delivery, and a checkout e2e. Test where the invariants and the money are, not where coverage is easy."
**Follow-up:** "How do you test event-driven flows without standing up the whole system?" (Direction: in-process bus fake for handler wiring, per-consumer contract tests with duplicate/out-of-order delivery, one thin smoke over the real broker.)
