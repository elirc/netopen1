# System Design From This Repo

The exercise: **"Design an e-commerce platform: browse products, cart, checkout, order tracking."** You will be asked some variant of this. eShop *is* a worked answer — walk the whiteboard the way this repo walks it, and at each step know what a simpler and a stronger alternative looks like. Cross-reference: [../03-architecture-and-patterns/06-architecture-critique.md](../03-architecture-and-patterns/06-architecture-critique.md).

Rehearse in this order; ~35 minutes aloud.

## Step 1 — Requirements (4 min)

Functional: browse/search catalog; cart; checkout; payment; order status; (stretch: webhooks for partners, admin catalog management). Non-functional: catalog reads ≫ writes (say 100:1); checkout must never double-charge or double-create (**idempotency**); order processing can be eventually consistent — users accept "Submitted → confirmed later"; browse should work even if ordering is down (**failure isolation**).

- *Junior answer:* jumps to tables. *Mid:* states read/write asymmetry and idempotency up front. *Senior:* also states what's allowed to be inconsistent, and for how long.

## Step 2 — API sketch (5 min)

What eShop chose (real anchors):
- `GET /api/catalog/items?pageSize&pageIndex&type&brand&name` — offset pagination, versioned v1/v2 (`CatalogApi.cs:L15-L30`)
- Basket as **gRPC** — internal, chatty, small messages (`basket.proto`); REST everywhere the surface is public
- `POST /api/orders` with **`x-requestid` header** as idempotency key (`OrdersApi.cs:L118-L136`)
- `PUT /api/orders/cancel`, `/ship` — command-style endpoints rather than PATCH state (`OrdersApi.cs:L11-L12`)

Alternatives to name: keyset pagination for deep pages; GraphQL if many client shapes (cost: caching, complexity); idempotency key in body vs header (header keeps it out of the domain model — nice touch to mention).

- *Junior:* CRUD on /orders. *Mid:* idempotency key + why PUT /cancel is a command not a state PATCH. *Senior:* discusses contract versioning strategy from day one (v2 of `/items` exists because v1's shape was wrong — real example, `CatalogApi.cs:L93-L102`).

## Step 3 — Data model (6 min)

What eShop chose: **database per service** — catalogdb, orderingdb, identitydb, webhooksdb on one Postgres server (`eShop.AppHost/Program.cs:L15-L18`); basket in Redis keyed by user id, no TTL (`RedisBasketRepository.cs:L13-L16`); **OrderItem snapshots** product name/price at purchase (`OrderItem` via `Order.AddOrderItem`, `Order.cs:L71-L91`) — receipts are immutable even when the catalog changes; stock counters live *on the catalog item* (`AvailableStock`), not a separate inventory service.

Alternatives: single shared DB (simpler; couples deploys; fine for a real MVP — say so, it shows judgment); separate inventory service (needed when stock has its own workflows — reservations, warehouses).

- *Junior:* FK from OrderItem to Product. *Mid:* explains why that FK **cannot exist** across services and snapshots instead. *Senior:* names the cost — snapshots go stale, product deletion needs tombstoning, and cross-service reporting needs a warehouse/CDC.

## Step 4 — The checkout write path (8 min — spend your time here)

Draw exactly Flow 3 ([../01-codebase-cartography/05-key-flows.md](../01-codebase-cartography/05-key-flows.md#flow-3-checkout)):

```
client --x-requestid--> Ordering API
  -> validate (FluentValidation)
  -> dedup (request id table)          ┐
  -> Order aggregate (invariants)      ├ ONE Postgres transaction
  -> outbox row (OrderStarted)         ┘
  -> commit -> publish to RabbitMQ
  -> consumers: Basket clears; Catalog checks stock; Payment charges; each step guarded + evented
```

Say the three magic sentences: (1) *"Idempotency key recorded in the same transaction as the order, so retries can't double-create"* (`IdentifiedCommandHandler.cs:L41-L48` + `TransactionBehavior.cs`). (2) *"Events go through a transactional outbox so the DB and the bus can't disagree"* (`TransactionBehavior.cs:L38-L52`). (3) *"Consumers are idempotent via state guards, because delivery is at-least-once"* (`Order.cs:L99-L128`).

Stronger alternative to volunteer: orchestrated saga (a saga coordinator owning the order workflow) vs eShop's **choreography** — choreography is simpler but the workflow is implicit; nobody can answer "where is the checkout process defined?" by pointing at one file. That criticism, offered unprompted, reads senior.

## Step 5 — Order state machine & async workers (5 min)

Submitted → (grace-period worker polls DB, `GracePeriodManagerService.cs:L69-L74`) → AwaitingValidation → (catalog stock check) → StockConfirmed → (payment) → Paid → Shipped; Cancelled reachable until Paid (`Order.cs:L99-L168`). Payment is a stub (`PaymentProcessor` flips on a config flag) — in a real design, talk PSP webhooks + signature verification + idempotent callback handling.

Failure story to tell: *"If the stock-check consumer throws, this bus acks anyway and the order freezes — the fix is a dead-letter exchange and a reconciliation job."* (`RabbitMQEventBus.cs:L177-L180`). Bringing a known weakness *and its fix* is the highest-signal move in the round.

## Step 6 — Scaling and ops (5 min)

Reads: catalog is stateless → horizontal scale + CDN for images (note the image pass-through `WebApp/Program.cs:L32`) + cache (none in repo — say you'd add ETag/output caching before Redis-caching entities). Writes: Ordering scales until Postgres is the bottleneck; the request-id table and outbox add one row each per order — fine. Workers: the grace-period poller **duplicates work if replicated** (no leader election) — consumers absorb it, but mention it. Observability: OTel end-to-end *through the queue* (`RabbitMQEventBus.cs:L86`); add metrics on stuck orders + outbox backlog (the repo lacks both).

## Variation prompts (practice each for 10 min)

1. **Add multi-tenancy** (sell the platform to many merchants): tenant id in every key (`/basket/{tenant}/{sub}`), tenant column + composite indexes, tenant claim in tokens, the *isolation* question (row-level vs schema vs DB per tenant) — and which eShop boundaries already make this easy (identity-keyed basket) vs hard (int order ids, R5).
2. **Real-time order tracking at scale**: eShop pushes bus events into Blazor circuits (`WebApp/Extensions.cs:L43-L51`) — works for one node; at scale you need a fan-out layer (SignalR backplane/Redis pub-sub) and to stop making the web tier a durable queue consumer.
3. **10× traffic on checkout**: idempotency table hot? (it's one insert; fine) — the real pressure is Postgres commit rate and RabbitMQ; shard orders by buyer, batch outbox publishing, keep the state machine unchanged. Being able to say *"the design survives 10×; only the infrastructure sizing changes"* is the point of having built it right.
4. **Flash sale / limited stock**: current stock check is check-then-decrement-later across events (`Catalog handler :L20` checks; decrement happens at Paid) — race exists by design. Fix: atomic conditional decrement (`UPDATE ... WHERE AvailableStock >= @units`) at reservation time + reservation expiry. Classic question; this repo gives you the exact "before" picture.
5. **Payments must be real**: PSP integration → their idempotency keys, webhook callbacks with signature verification, and a reconciliation job — map each onto patterns you already have (request-id, outbox, sweeper).

## Grading yourself

Basic: complete design, all boxes named. Solid (the mid-level bar): idempotency + outbox + eventual consistency stated with mechanism, one alternative per step. Strong: volunteered failure modes and their fixes, drew the state machine unprompted, tied every claim to something you can defend from real code.
