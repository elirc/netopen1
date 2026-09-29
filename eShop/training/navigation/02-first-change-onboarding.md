# Before your first production-style change here

One page. This is the minimum you need to understand before touching `src/` in this repo — assumes you've read
`astra/00-onboarding/` (environment/run) already; this is about the *design*, not the setup.

1. **Nothing calls another service's database.** Each API owns one Postgres database (`catalogdb`, `identitydb`,
   `orderingdb`, `webhooksdb` — declared in `src/eShop.AppHost/Program.cs`) or Redis (`Basket.API`). The one
   documented exception is `src/OrderProcessor/Services/GracePeriodManagerService.cs`, which runs raw SQL against
   `ordering.orders` from outside Ordering.API — a deliberate, named trespass (see `fabledoc2` ADR-002). If your
   change wants to read another service's data, that's a signal to use an integration event or a service call,
   not a shortcut.

2. **Cross-service coordination is choreographed events, not calls.** Ordering never calls Catalog directly to
   check stock; it publishes `OrderStatusChangedToAwaitingValidationIntegrationEvent` and Catalog reacts. If your
   change needs another service to know something, you're adding an event and a handler, not a `HttpClient` call
   — unless it's a synchronous read the UI needs immediately (the one exception pattern is Basket reading Catalog
   prices at checkout time, `BasketState.FetchBasketItemsAsync`).

3. **Any DB write in Ordering or Catalog that should notify another service goes through the outbox**, not a
   direct `IEventBus.PublishAsync` call after `SaveChangesAsync`. Write the event via
   `IOrderingIntegrationEventService.AddAndSaveEventAsync` (or Catalog's equivalent) *inside* the same transaction
   as your business write, and let `TransactionBehavior`/the API's own commit-then-publish code publish it after
   commit. Publishing directly reintroduces the exact "half-committed" failure mode the outbox exists to prevent
   — see `01-checkout-outbox-correctness.md` row 3-4 for why.

4. **The outbox's publish step can silently fail** (`01-checkout-outbox-correctness.md` row 4) and nothing
   currently retries it. If your change adds a new integration event, know that a broker hiccup at publish time
   means that event may just never arrive — don't design a feature whose correctness depends on "the event will
   eventually get there" without checking whether your feature can tolerate that gap or needs the sweeper
   discussed in `03-outbox-sweeper-tradeoff.md` first.

5. **Order state is a guarded state machine** (`src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs`):
   every transition method checks the current status before applying. If you add a new transition, add the guard
   — it's the only thing making duplicate/out-of-order event delivery safe for Ordering.

6. **Four layers of validation exist for a reason, and they're not redundant**: DataAnnotations on the Blazor
   form, FluentValidation on the MediatR command (`ValidatorBehavior`), aggregate invariants in `Order.cs`
   (throws `OrderingDomainException`), and — separately — authn/authz at the API boundary. A change that only
   adds client-side validation hasn't protected the API from a non-browser caller.

7. **Check `astra/03-reference/risk-register.md`-equivalent before you assume something is a bug**: both
   `fabledocs` and `astra` label several rough edges (simulated payment, no dead-letter queue, `ValidateAudience
   = false`, `GetOrderAsync` with no ownership check) as either deliberate teaching simplifications or open
   *investigate* items, not confirmed defects. Read `fabledocs/09-reference/risk-register.md` before filing one as
   new.
