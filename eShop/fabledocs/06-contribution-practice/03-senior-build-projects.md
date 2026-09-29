# Senior Build Projects

Five projects, 3 days–4 weeks each. Each is realistic — something a maintainer of a system *like this* would actually accept (a few are sample-app-inappropriate and say so; build them on a fork as portfolio work).

---

## Project 1: Reliability hardening bundle (DLX + sweeper + stuck-order reconciler)
Scope: 2–3 weeks. Combines tickets M1 + M2 + a reconciliation job.
Problem: R1 + R2 mean orders can silently freeze. Product value: no lost orders, ops visibility.
Architecture decisions: DLX topology and queue migration (M2); sweeper concurrency (M1); reconciler = periodic query for orders stuck in non-terminal status > threshold → re-drive or alert (design question: re-drive by re-publishing the *last expected* event vs flagging for humans — start with humans).
Likely files: `EventBusRabbitMQ/*`, new hosted services in Catalog/Ordering/OrderProcessor, `IntegrationEventLogService`.
Migration plan: new queue names (v2) with DLX args; consume-from-both window; retire old.
Test plan: chaos-style integration tests using the `throw-fake-exception` hook (`RabbitMQEventBus.cs:L163-L166`); broker kill/restart; duplicate-delivery assertions on every consumer.
Security: DLX redrive tool is an admin surface — authZ it.
Rollout/rollback: feature flags per component; DLX is additive; sweeper off-switch.
Open questions: alert destinations; retention on DLX.
Stretch: outbox → Debezium/CDC comparison doc.
Interview story potential: a complete "made an event-driven system production-grade" narrative — the strongest single portfolio item this repo can produce.

## Project 2: Real payment integration (Stripe-shaped)
Scope: 3–4 weeks (fork-only; the sample deliberately stubs this).
Problem: `PaymentProcessor` flips on a config flag. Value: the single most interview-relevant gap.
Design checklist: PSP idempotency keys (map from order id); payment intent lifecycle vs order state machine (new statuses? no — map PSP states onto StockConfirmed→Paid/Cancelled); **webhook callback endpoint** with signature verification + replay tolerance; reconciliation job for webhook loss; secrets via user-secrets/KeyVault.
Likely files: PaymentProcessor grows an HTTP surface (or a new Payments.API — argue the boundary!), Ordering handlers unchanged (events in, events out — prove the seam holds).
Test plan: PSP sandbox + a fake-PSP in-proc for CI; the golden test: webhook delivered twice = one Paid transition (state guard already gives this — demonstrate it).
Rollout: dark-launch behind the existing simulator flag.
Interview story: "Integrated a real payment provider into an event-driven order pipeline, idempotent end to end."

## Project 3: Inventory reservations (fix the flash-sale race)
Scope: 2–3 weeks.
Problem: stock is *checked* at AwaitingValidation (`Catalog handler :L20`) but *decremented* at Paid — overselling window. Value: correctness under load; variation prompt 4 in the system-design file, built for real.
Architecture decisions: reservation record with expiry at stock-check time; atomic conditional decrement (`UPDATE ... WHERE AvailableStock >= @n`); compensation event on expiry; new integration events (additive).
Likely files: Catalog handlers + model + migration; Ordering unaffected except event names — that asymmetry is the design's proof of boundary quality.
Migration: additive table + backfill nothing; feature-flag the reservation path per… (product? percentage? decide and defend).
Test plan: concurrent checkout integration test (two orders, stock=1, exactly one confirms) — the test *is* the deliverable.
Interview story: "Designed reservation semantics to close an oversell race, with a concurrency test proving it."

## Project 4: Multi-tenant catalog (white-label mode)
Scope: 4 weeks, fork-only. The system-design variation prompt 1, implemented.
Design checklist: tenant resolution (host header? claim?), tenant column + composite indexes + EF global query filters, per-tenant seeding, tenant claim in Identity, basket keys `/basket/{tenant}/{sub}`, event payloads gain TenantId (versioning!), the isolation test suite (cross-tenant reads must 404).
The senior deliverable is the **isolation test suite** and the written threat model, not the plumbing.
Interview story: "Retrofitted tenant isolation across services, queues, and cache keys."

## Project 5: Observability-as-product
Scope: 3 days–1 week. The most upstreamable.
Problem: no domain metrics/alerts (module 05/06). Value: "how would I know?" answered by dashboards.
Design: `System.Diagnostics.Metrics` counters/histograms — orders_created, order_stage_duration (per transition, tagged by from/to), outbox_backlog_age, consumer_connected gauge; Grafana/dashboard JSON committed; alert rules as code with the "stuck > 15 min" business invariant rule.
Likely files: small touches in command handlers + event handlers + bus; ServiceDefaults for meter registration.
Test plan: metric emission asserted via `MetricCollector<T>` in unit tests.
Interview story: "Instrumented a distributed order pipeline with business-level SLO metrics" — pairs perfectly with any SRE-flavored question.
