# Senior trade-off: should this repo have an outbox retry sweeper?

Sequel to `fabledoc2/README.md` ADR-003 ("choreographed events over RabbitMQ"), which names "no retry dispatcher"
as an accepted consequence without designing the alternative. This card does that design, in the format the
apprenticeship curriculum uses for senior trade-offs, and it is the direct setup for `04-change-request.md`.

**Problem.** `OrderingIntegrationEventService.PublishEventsThroughEventBusAsync` (and Catalog's equivalent) marks
a row `PublishedFailed` on a broker publish exception and returns normally — the HTTP request that triggered it
already committed and returned 200. No process ever revisits `PublishedFailed` or stale `NotPublished` rows.
(Evidence: `01-checkout-outbox-correctness.md` row 4 — grep confirms zero readers of `PublishedFailed` anywhere in
`src`.)

**Naive approach.** Retry the publish inline, in the same request, before returning to the caller (e.g. wrap
`_eventBus.PublishAsync` in a retry loop with backoff inside `PublishEventsThroughEventBusAsync`).

**Where it fails.** This makes the checkout request's latency and success depend on RabbitMQ's *current*
availability, which is exactly the coupling the choreographed-event design (ADR-003) exists to avoid — a broker
outage would turn into checkout 500s or multi-second hangs instead of a queued-for-later state. It also doesn't
help crash-mid-retry: if the API process dies between commit and the retry loop finishing, you're back to a
stranded row with nobody watching it.

**Options considered:**
- **A — Inline retry with backoff** (above). Rejected: re-couples checkout availability to broker availability.
- **B — Background sweeper polling `IntegrationEventLogEntry` for stale `NotPublished`/`PublishedFailed` rows**,
  republishing on a timer, similar in shape to `GracePeriodManagerService`. Requires a new method on
  `IIntegrationEventLogService` — the current interface only exposes
  `RetrieveEventLogsPendingToPublishAsync(Guid transactionId)`, scoped to one transaction; a sweeper needs an
  unscoped "give me everything stale" query, and because each service (`Catalog.API`, `Ordering.API`) registers
  its own closed generic `IntegrationEventLogService<TContext>`, the sweeper has to live per-service, not as one
  shared worker, unless the interface/DI shape changes too.
- **C — Outbox relay via change-data-capture** (e.g. Debezium on the Postgres WAL) publishing from the DB log
  directly, bypassing the API process entirely. Removes the API-process-dies-mid-publish window completely, but
  is real infrastructure this sample explicitly avoids (it already avoids MassTransit/NServiceBus per ADR-003 for
  the same "don't hide the mechanics" reason) and adds an ops dependency far outside the sample's teaching scope.

**Trade-offs.** B is bounded, incremental, and matches the codebase's existing idiom (a `BackgroundService`
worker per concern — see `GracePeriodManagerService`), at the cost of at-least-once delivery becoming *visibly*
at-least-once (a republished event must be a safe no-op downstream — already true here, since `Order.cs`'s
status guards and Basket's idempotent-delete already assume at-least-once). A also needs idempotent consumers but
buys nothing over B while adding latency coupling. C is the "right" production answer at larger scale but is not
a one-PR change and not this sample's pedagogy.

**Choice.** B — a bounded per-service sweeper — is the one worth designing as a change request, because it's
small enough to place in one sitting and it directly exercises the interface-boundary decision (row-per-service
vs. shared) that makes this a real design problem, not a copy-paste `BackgroundService`.

**Failure modes of B.** Sweeper polls too aggressively → duplicate publish storms if `MarkEventAsInProgressAsync`
isn't itself checked before re-publish (there's already a `TimesSent` counter incremented on `InProgress` — a cap
belongs here). Sweeper crashes mid-run → fine, it's idempotent-safe to just poll again next tick, *if* downstream
consumers are idempotent (they are, per row 6 of `01-checkout-outbox-correctness.md`).

**How it's tested.** Not currently — `tests/Ordering.FunctionalTests/` and `tests/Ordering.UnitTests/` have no
coverage of `PublishEventsThroughEventBusAsync`'s failure branch (confirm by grepping those test projects for
`PublishedFailed` before writing the sweeper — if it's untested today, the change request must add that test,
not just the happy path).

**How it's monitored.** Not currently — no metric/log counter surfaces the count of `PublishedFailed`/stale
`NotPublished` rows. A sweeper without an accompanying gauge just moves the invisibility from "message lost" to
"message eventually retried, nobody knows how often."

**When to revisit.** If this sample ever needed multi-region or higher event volume, option C (CDC-based outbox
relay) is what production eShop-scale systems actually use; B is the right stopping point for a sample whose job
is to teach the mechanism, not operate at scale.
