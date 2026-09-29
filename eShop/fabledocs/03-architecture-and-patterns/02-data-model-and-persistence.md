# Data Model & Persistence

## The stores

| Store | Owner | Key entities | Notes |
| --- | --- | --- | --- |
| `catalogdb` (Postgres+pgvector) | Catalog.API | CatalogItem, CatalogBrand, CatalogType, IntegrationEventLog | `Embedding` is a `Vector` column (`Catalog.API/Extensions/Extensions.cs:L15-L21`) |
| `orderingdb` (Postgres, schema `ordering`) | Ordering.API | Order, OrderItem, Buyer, PaymentMethod, CardType, ClientRequest (idempotency), IntegrationEventLog | schema set at `OrderingContext.cs:L37`; outbox joined at L44 |
| `identitydb` | Identity.API | ASP.NET Identity users + IdentityServer operational data | mostly framework-owned |
| `webhooksdb` | Webhooks.API | webhook subscriptions | not read in depth (see verification log) |
| Redis | Basket.API | `/basket/{sub}` → JSON CustomerBasket | no TTL set (`RedisBasketRepository.cs:L34-L48`) — *possible risk: unbounded growth* |

## Relationships worth knowing (ordering)

`Order 1—* OrderItem` (owned collection, private field mapping); `Order *—1 Buyer` (nullable FK, `Order.cs:L14` — orders exist before their buyer is verified); `Buyer 1—* PaymentMethod`; `Address` is an **owned value object** on Order (`Order.cs:L10-L12`) — persisted as columns, no identity, compared by value (`Ordering.Domain/SeedWork/ValueObject.cs`).

**OrderItem snapshots product data** (name, price, discount, picture) instead of referencing catalogdb. This is denormalization *as a correctness feature*: your receipt shouldn't change when marketing renames a product. Say "point-in-time snapshot across a service boundary" in an interview and you've explained both microservice data duplication and why FKs can't cross services.

## Transaction boundaries & consistency

- **Within Ordering:** one command = one transaction = one aggregate + its domain-event side effects + the outbox row + the idempotency row. Opened by `TransactionBehavior.cs:L38` with an EF **execution strategy** (retryable transactions), isolation `ReadCommitted` (`OrderingContext.cs:L68`).
- **Across services:** *eventual consistency only.* Stock check happens seconds after checkout; the user sees "Submitted" immediately. No 2PC anywhere, on purpose. Compensation = cancellation (`Order.cs:L155-L168`).
- **Catalog:** implicit transactions per `SaveChangesAsync`, except the price-change path which shares a transaction with the outbox (`CatalogApi.cs:L350-L356`).
- **Dual-write hazard averted:** everywhere a DB write must coincide with an event, the outbox is used. Verify by grepping `PublishAsync` — direct publishes without an outbox occur only in stateless services (PaymentProcessor, OrderProcessor) that have no DB write to keep consistent. That's a coherent rule, not an accident. (OrderProcessor is stateless *per publish* — it re-derives from the DB each poll, so a lost publish self-heals next cycle.)

## Migrations & seeding

- Migrations live in `src/Ordering.Infrastructure/Migrations/` (command documented in `OrderingContext.cs:L5-L9`) and Catalog's equivalent.
- **Auto-migrate-and-seed on startup**: `builder.Services.AddMigration<CatalogContext, CatalogContextSeed>()` (`Catalog.API/Extensions/Extensions.cs:L23-L24`) — flagged in-code with "shouldn't be here in production." Seed data: `src/Catalog.API/Setup/catalog.json` (~100 AI-generated products). AppHost even sequences OrderProcessor *after* Ordering.API because "that contains the EF migrations" (`eShop.AppHost/Program.cs:L49`).
- Why auto-migrate is a dev-only pattern: N replicas racing to migrate; a bad migration takes the service down with no rollback gate; production wants migrations as a deploy *step* with review.

## How to change the schema safely (the transferable checklist)

1. Is the column on a wire contract? (In Catalog, entity = contract — so *yes* by default. Check consumers first.)
2. Write the migration; read the generated SQL, don't trust scaffolding blind.
3. Expand → migrate → contract for anything breaking: add nullable column, backfill, dual-write/dual-read window, then drop the old one. Never rename in place across a deploy boundary.
4. Update snapshot consumers: does OrderProcessor's raw SQL (`GracePeriodManagerService.cs:L69-L74`) touch your table? (It's the one consumer migrations won't flag at compile time.)
5. Test: functional tests here run real Postgres (`CatalogApiFixture.cs:L17-L25`), so migration bugs surface — run them.
6. Plan rollback: down-migration written and tested, or explicitly declared forward-only.

Interview angle: "How do you do zero-downtime schema changes?" = expand/contract, with the OrderProcessor raw-SQL consumer as your war-story-shaped example of the hidden reader that breaks.

Drill: design the migration to add `Order.CancelledAtUtc`. Which files change (entity, EntityConfiguration, migration, query DTO?), who reads it, is it breaking, what's the rollback?
Self-grade — Basic: nullable column + migration. Solid: sets it in `SetCancelledStatus`/`SetCancelledStatusWhenStockIsRejected`, updates the query side. Strong: notes it's non-breaking (nullable, additive), the down-migration is trivial, and the grace-period SQL is unaffected — and says how you verified that last claim.
