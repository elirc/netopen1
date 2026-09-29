# Architecture Critique

The senior exercise: not "is this good?" but "what does this design commit us to, who pays, and what would I change first if I owned it for three months?" This file doubles as system-design interview material — cross-linked from [08-interview-prep/04-system-design-from-this-repo.md](../08-interview-prep/04-system-design-from-this-repo.md).

## Strongest design choices (defend these in an interview)

1. **Outbox everywhere a DB write meets an event** (`TransactionBehavior.cs:L38-L52`, `CatalogApi.cs:L350-L356`). The dual-write problem is *the* microservices failure mode; this repo simply doesn't have it.
2. **Idempotency as a layered system**, not a feature: request-id dedup at the edge, state guards in the domain, naturally idempotent consumers. Any one layer failing is absorbed by another.
3. **A pure domain project.** `Ordering.Domain` referencing no frameworks makes the most valuable logic in the system the cheapest to test (`OrderAggregateTest.cs` needs no mocks).
4. **Prices/identity never trusted from clients** — recomputed or re-derived server-side at every boundary (`BasketState.FetchBasketItemsAsync`, `OrdersApi` reading identity from the token).
5. **Observability by default**: OTel across HTTP *and* the message bus with context propagation (`RabbitMQEventBus.cs:L86`). Most real systems lose the trace at the queue; this one doesn't.
6. **Deliberate pattern asymmetry**: DDD/CQRS only where invariants are rich (Ordering); plain CRUD where they aren't (Catalog). Uniformity would have been worse. This is the single most senior thing about the codebase.

## Risks and tradeoffs (confirmed vs hypothesis)

| # | Finding | Status | Evidence |
| --- | --- | --- | --- |
| R1 | Handler exception ⇒ message acked ⇒ **event lost**; orders freeze mid-state-machine | **Confirmed** (code + its own comment) | `RabbitMQEventBus.cs:L177-L180` |
| R2 | Outbox rows orphaned on crash-after-commit — no background dispatcher | **Confirmed** (only caller passes current tx id) | `IntegrationEventLogService.cs:L19-L32` |
| R3 | Create-order failures return HTTP 200 (exception swallowed → `default` → `Ok()`) | **Confirmed** | `IdentifiedCommandHandler.cs:L99-L102` + `OrdersApi.cs:L157-L166` |
| R4 | Catalog write endpoints unauthenticated | **Confirmed** | `CatalogApi.cs:L93-L110` (no auth metadata anywhere in file) |
| R5 | Possible IDOR on `GET api/orders/{id}` | **Hypothesis** — depends on `OrderQueries` filtering | `OrdersApi.cs:L80-L91` |
| R6 | `ValidateAudience=false` flattens scope boundaries between services | **Confirmed** (impact judgment, not bug) | `AuthenticationExtensions.cs:L49` |
| R7 | OrderProcessor raw SQL against Ordering's schema — runtime coupling invisible to compiler and migrations | **Confirmed** | `GracePeriodManagerService.cs:L69-L74` |
| R8 | Redis baskets have no TTL — unbounded keyspace growth | **Confirmed** (no `expiry` arg) | `RedisBasketRepository.cs:L37` |
| R9 | Contract duplication: `CreateOrderRequest` maintained twice | **Confirmed** | `BasketState.cs:L158-L172` vs `OrdersApi.cs:L171-L185` |
| R10 | Auto-migrate+seed at startup unsafe for multi-replica prod | **Confirmed** (code comment agrees) | `Catalog.API/Extensions/Extensions.cs:L23-L24` |

(Fuller table with likelihood/impact: [../09-reference/risk-register.md](../09-reference/risk-register.md).)

## "Owning this for 3 months" — prioritized changes

1. **Dead-letter exchange + stop acking failures** (fixes R1). Migration path: add DLX config to queue declaration (`RabbitMQEventBus.cs:L258-L263`), nack-without-requeue on exception, small consumer for the DLX that logs/alerts. Test: publish `throw-fake-exception` message (the hook already exists, `:L163-L166`!) and assert it lands in the DLX. Blast radius: messaging layer only; consumers unchanged.
2. **Outbox sweeper** (fixes R2): `BackgroundService` in each publisher polling `NotPublished`/`PublishedFailed` older than N seconds, republish, mark. Consumers are already guarded, so re-publish is safe — that's *why* you built idempotent consumers. Test: kill publish (stop RabbitMQ container) mid-flow, restart, assert delivery.
3. **Honest HTTP semantics on create-order** (fixes R3): stop swallowing in `IdentifiedCommandHandler`; let ValidatorBehavior's exception map to 400 ProblemDetails; return 500 on real failures. Risk: clients that treated 200-failure as success — audit WebApp's `OrderingService.CreateOrder` first. This is a *contract change*; do it behind a version or with consumer sign-off.
4. **AuthZ pass** (R4, R5, R6): `RequireAuthorization("CatalogWrite")` policy on catalog mutations; ownership filter in order queries; turn audience validation on and give each client only its scopes.
5. **Basket TTL** (R8): `StringSetAsync(..., expiry: TimeSpan.FromDays(90))` — one line, one test, real ops win.

Each of these is sized as a ticket/project in [06-contribution-practice](../06-contribution-practice/).

## What I would *not* change

- The raw-SQL grace-period query (R7): an API would add a network dependency to a poller whose whole virtue is simplicity. Document it, add a schema-drift test, move on. Knowing when a leak is *rent worth paying* is the difference between senior and dogmatic.
- The CQRS asymmetry, entity-as-contract in Catalog (until the API has external consumers), Blazor Server (right choice for this demo's goals).

Interview angle: bring R1–R3 to any "what would you improve about a system you've worked with?" question. The pattern of a strong answer: *observed evidence → failure scenario → smallest fix → how you'd test it → who's affected.* Never lead with a rewrite.

Drill: write the one-page RFC for change #1 (DLX) using the template in [../07-career-and-collaboration/02-writing-prs-and-rfcs.md](../07-career-and-collaboration/02-writing-prs-and-rfcs.md).
