# Sealed reference answer — retry stranded outbox events

Do not read before writing your own answer to `navigation/04-change-request.md`.

## 1. Files touched

- `src/IntegrationEventLogEF/Services/IIntegrationEventLogService.cs` — new method.
- `src/IntegrationEventLogEF/Services/IntegrationEventLogService.cs` — implementation.
- `src/Ordering.API/` — a new `BackgroundService` (e.g. `Application/Sweepers/IntegrationEventSweeperService.cs` or
  colocated with `Extensions.cs`'s DI registration), registered alongside the existing
  `services.AddTransient<IIntegrationEventLogService, IntegrationEventLogService<OrderingContext>>()` line.
- `src/Catalog.API/` — the same shape, its own sweeper instance over `CatalogContext`, since it registers its own
  closed-generic service the same way.
- `tests/Ordering.UnitTests/` (or a new `Ordering.FunctionalTests` case) — a test for the sweeper's retry
  behavior.
- Nothing in `src/EventBusRabbitMQ`, `Order.cs`, or `OrdersApi.cs` needs to change — the sweeper is additive; it
  reuses `IEventBus.PublishAsync` and the existing `MarkEventAsInProgressAsync`/`MarkEventAsPublishedAsync`/
  `MarkEventAsFailedAsync` calls, it doesn't change the checkout path at all.

## 2. Interface change

Yes, a new method is required. `RetrieveEventLogsPendingToPublishAsync(Guid transactionId)` is scoped to one
transaction by design (it's called right after that transaction's commit, from `TransactionBehavior`). A sweeper
has no transaction ID to scope by — it needs to find rows across *all* transactions that are stale. Add:

```
Task<IEnumerable<IntegrationEventLogEntry>> RetrieveStaleEventLogsAsync(TimeSpan olderThan);
```

implemented as a query over `EventStateEnum.NotPublished` OR `EventStateEnum.PublishedFailed` where
`CreationTime < utcNow - olderThan`, ordered by `CreationTime` (mirrors the existing method's ordering). Using an
age cutoff rather than "all `NotPublished` rows" matters: a row that's `NotPublished` because its transaction
committed 200ms ago and `PublishEventsThroughEventBusAsync` just hasn't run yet is *not* stranded — treating it as
stranded risks a race where the sweeper and the original request both try to publish the same fresh row.

## 3. Where the loop lives

A new `BackgroundService`, following `src/OrderProcessor/Services/GracePeriodManagerService.cs`'s shape exactly:
constructor-injected `IServiceScopeFactory` (to get a scoped `DbContext`/`IIntegrationEventLogService` per tick,
since `IntegrationEventLogService<TContext>` and the `DbContext` are not singletons), a `PeriodicTimer` or
`Task.Delay` loop, and per-tick: fetch stale rows, republish, mark. `GracePeriodManagerService` is a good template
for *shape* (timer-driven `BackgroundService` polling a DB table and publishing events) but a poor template for
*placement* — it lives in a separate `OrderProcessor` project specifically because it needs to run independently
of Ordering.API's request-handling lifecycle and be scaled/restarted separately. The sweeper doesn't need that:
it only ever acts on rows written by its own service's own outbox, so it belongs *inside* `Ordering.API` (and
`Catalog.API`) as a hosted service registered via `builder.Services.AddHostedService<...>()`, not as a new
standalone worker project. Standing up a whole new project for this is over-engineering a one-table poller.

## 4. Shared vs. per-service

Per-service, one sweeper instance per API that registers `IIntegrationEventLogService`. The registration is
`AddTransient<IIntegrationEventLogService, IntegrationEventLogService<TContext>>()`, closed over each service's
own `DbContext` (`OrderingContext`, `CatalogContext`) — there is no single connection string or context a shared
sweeper could poll across services. Building one shared sweeper would mean either (a) giving one process
connection strings to every service's database, which breaks the database-per-service boundary this repo commits
to everywhere else (`fabledoc2` ADR-002), or (b) exposing an HTTP endpoint per service for "retry my stale
events," which is more moving parts than the problem justifies. Per-service, in-process is the answer consistent
with the rest of the codebase.

## 5. What makes redelivery safe (and where it isn't guaranteed)

- Ordering: `Order.cs` status-guarded transitions make a redelivered `OrderStatusChangedTo*` handler a safe no-op
  once the order has already advanced past that state.
- Basket: `OrderStartedIntegrationEventHandler` deleting a basket is naturally idempotent (deleting an
  already-deleted key is a no-op).
- Catalog: stock-check and price-change handlers — **not independently verified as idempotent in this pass**.
  `OrderStatusChangedToPaidIntegrationEventHandler` *decrements* stock (per `fabledocs` Flow 4) — a decrement is
  **not** naturally idempotent; a redelivery here could double-decrement stock if the original publish actually
  succeeded and only the outbox row's status update failed (a narrower race than "publish itself failed," but the
  sweeper's age-cutoff query can't distinguish "genuinely never published" from "published, but marking it
  `Published` afterward crashed"). This is the honest gap: the correct write-up flags this as `UNKNOWN — needs
  inspection of the stock-decrement handler and whatever unique-constraint/version-check it does or doesn't have`
  rather than asserting safety. A rigorous version of this change would either confirm the decrement handler is
  itself idempotent (e.g. checks a processed-event-id table) or scope the sweeper to *only* retry rows that are
  provably never-published (i.e., separate "never made it to the broker" from "made it to the broker but the
  status update after didn't commit" — the latter needs at minimum a broker-side confirm/ack correlated back
  before marking `Published`, which today's code doesn't do either: `PublishAsync` is called and then immediately
  marked `Published` with no confirmation callback). A senior answer says this out loud instead of assuming the
  status guards fully cover it.

## 6. Test

`tests/Ordering.UnitTests/` (or a new functional test): inject a fake `IEventBus` whose `PublishAsync` throws on
the first N calls (simulating the broker being down) and succeeds after; assert that after the sweeper's method
runs (called directly, not via the timer, for a unit test) the row transitions `PublishedFailed` → eventual
`Published`, and that `TimesSent` increments each attempt. Confirmed via grep that `tests/` currently has zero
references to `PublishedFailed` or `PublishEventsThroughEventBusAsync` — this would be new coverage, not an
extension of an existing suite.

## 7. Failure mode of the sweeper itself, and the bound

Two consumers of the same stale row (a slow request's own publish-after-commit plus the sweeper's next tick)
could both attempt to publish it concurrently if the age cutoff is too aggressive relative to normal publish
latency — this is the reason for the age cutoff in answer 2, and it should be generous (minutes, not seconds) per
Ops's own stated tolerance ("a minute or two of delay before recovery is fine"). The other bound needed: cap
retries using the existing `TimesSent` counter (already incremented on every `InProgress` mark) — after N
attempts, stop retrying and leave the row `PublishedFailed` for a human/alert rather than retrying forever against
a broker that might be down for hours, which is the "hammering a broker that's still down" failure Ops explicitly
asked to avoid. A metric/log line on "row exceeded max retries" is what closes `03-outbox-sweeper-tradeoff.md`'s
"how is it monitored" gap — without it, this change trades one invisible failure mode for a slightly-less-invisible
one.

## Grading notes

A **Basic** answer gets 1-4 roughly right and proposes *some* test. A **Solid** answer additionally identifies
the per-service registration constraint (4) correctly and proposes the age-cutoff reasoning in 2. A **Strong**
answer reaches the idempotency gap in 5 unprompted — flagging that stock decrement may not be safely
re-publishable is the single hardest part of this exercise, and catching it without being told is what separates
a change that looks done from one that's actually safe to ship.
