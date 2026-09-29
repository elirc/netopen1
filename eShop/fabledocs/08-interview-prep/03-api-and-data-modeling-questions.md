# API & Data Modeling Questions — 12 Cards

## Q1: Design pagination for a product list. Defend your choices.
Round: API/data.
Repo anchor: `CatalogApi.cs:L124-L159` (`PaginationRequest`, count+page, `PaginatedItems<T>` envelope).
Junior: "LIMIT and OFFSET."
Mid: envelope with pageIndex/pageSize/total; filters composed before count; cap on pageSize (missing here — ticket 15); offset's deep-page cost.
Senior: keyset pagination tradeoff (no random access, stable sort key required); whether `total` is worth its extra query at scale (often dropped or estimated).
Drill: whiteboard both SQL shapes from memory.

## Q2: How do you make POST /orders safe to retry?
Repo anchor: the whole of Flow 3 — `x-requestid` (`OrdersApi.cs:L119`), `IdentifiedCommandHandler.cs:L41-L48`, id minted per intent (`Checkout.razor:L94`).
Mid: client-supplied idempotency key, stored atomically with the write, duplicates get a canned success.
Senior: key scoping (per user? global GUID?), retention window, and the failed-first-attempt wart (pattern card 2) with the fix.
This is the highest-frequency API interview question that exists; over-prepare it.

## Q3: REST vs gRPC vs events — this system uses all three. Why each where?
Repo anchor: Catalog REST (public, cacheable, versioned), Basket gRPC (`basket.proto` — internal, chatty), RabbitMQ events (facts, fan-out, no reply needed).
Mid: request/response vs fire-and-forget; who the consumer is (browser? partner? peer service?).
Senior: the decision table — need a reply now? sync. Multiple independent reactors? events. High-frequency internal + typed contract? gRPC. Then one criticism: WebApp consuming the bus blurs the third category (M10).

## Q4: Version an API without breaking clients.
Repo anchor: `CatalogApi.cs:L15-L30, L93-L102` (v1/v2 side by side; UpdateItem's id moved body→route); clients pin versions (`WebApp/Extensions.cs:L35, L39`); `ReportApiVersions` headers (`Catalog.API/Program.cs:L7-L11`).
Mid: additive = safe; breaking = new version; deprecation signaling.
Senior: version the *contract*, not the code — v1 delegates to v2 logic here (`GetAllItemsV1` → `GetAllItems`, `:L116-L121`), one implementation, two shapes; and events need versioning too (additive fields only — no version machinery exists on the bus, worth volunteering).

## Q5: Model an order. Why snapshot instead of FK to products?
Repo anchor: `Order.AddOrderItem` (`Order.cs:L71-L91`), OrderItem fields.
Mid: receipts are immutable; prices change; FK across service DBs is impossible anyway.
Senior: what snapshotting costs (stale images/names, storage) and where you still need the id (reorder, analytics joins via warehouse).

## Q6: Where do transactions begin and end in a well-factored service?
Repo anchor: `TransactionBehavior.cs:L32-L52` — one command, one transaction, opened in a behavior not in handlers; `OrderingContext.cs:L64-L96`.
Mid: transaction per use-case at the application boundary; handlers stay composable.
Senior: execution strategy interplay (retryable transactions), isolation level choice (ReadCommitted, L68), and the rule "no network I/O inside" (review kata 1).

## Q7: Explain the outbox pattern like I'm a new hire.
Repo anchor: `CatalogApi.cs:L347-L361` is the cleanest single-screen example in existence; states in `EventStateEnum.cs`.
(Prepared answer in pattern card 1 and Flow 6 — rehearse from those.)

## Q8: What makes an event consumer idempotent? Show three techniques.
Repo anchor: state guards (`Order.cs:L99-L128`), naturally idempotent ops (basket delete), dedup-by-key (request ids — and note the *absence* of event-id dedup tables here).
Senior: pick per consumer, cheapest that works; "exactly-once delivery" doesn't exist — exactly-once *effect* is engineered at the consumer.

## Q9: How would you evolve `basket.proto` to add a "saved for later" flag?
Repo anchor: `Basket.API/Proto/basket.proto`, mapping at `BasketService.cs:L77-L110`.
Mid: new optional field, new tag number, old clients ignore it; never reuse/renumber tags.
Senior: default-value semantics in proto3 (absent == false — is that the right default for the feature?), and rollout order (server first, then clients).

## Q10: Cache invalidation for a product catalog — design it.
Repo anchor: the absence (no HTTP caching) + the price-change event (`ProductPriceChangedIntegrationEvent`) as an invalidation signal that already exists.
Mid: TTL first (simplicity), ETag/If-None-Match for free correctness on unchanged data.
Senior: event-driven purge only where staleness is costly (price at checkout — and note this system tolerates it because the *order* snapshots server-side price at creation; the cache can be stale because the money path doesn't trust it. Layered defense = relaxed caching. That connection is a genuinely senior insight — make it).

## Q11: One Postgres server, four databases (`eShop.AppHost/Program.cs:L15-L18`). Better or worse than four servers? Than one shared DB?
Mid: databases give schema/credential isolation and independent migration; shared server saves ops cost; shared *database* would couple deploys and tempt cross-service joins.
Senior: the failure-domain honesty — one server down = all services degraded, so this is *logical* isolation only; migration path to physical isolation is per-database, which is exactly why the boundary was drawn here.

## Q12: A webhook system for order events — sketch the data model and delivery semantics.
Repo anchor: `src/Webhooks.API` exists (subscriptions in webhooksdb; delivery on order events) — conceptual card since we didn't deep-read it; say that honestly if asked to detail.
Mid: subscription (url, event types, secret), delivery log, retries with backoff, HMAC signature.
Senior: SSRF on registration (validate/deny internal ranges), ownership verification (challenge), at-least-once + receiver idempotency guidance, and pause-after-N-failures policy.
