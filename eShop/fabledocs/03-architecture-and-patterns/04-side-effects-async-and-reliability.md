# Side Effects, Async Work, and Reliability

A **side effect** is anything a request does beyond computing its response: DB writes, messages, external calls, cache mutations. Reliability engineering is deciding, for each one: *what if it runs twice? what if it never runs? how would we know?*

## Side-effect inventory

| Side effect | Trigger | Where | Twice? | Never? | Visible? |
| --- | --- | --- | --- | --- | --- |
| Order rows written | CreateOrderCommand | `CreateOrderCommandHandler.cs:L49-L51` | deduped by request id | client sees 200-with-failure-log (wart) | logs + traces |
| Outbox row written | any integration event from Catalog/Ordering | `IntegrationEventLogService.cs:L34-L44` | same tx as business data | same tx — can't diverge | table queryable |
| RabbitMQ publish | after commit | `TransactionBehavior.cs:L52`, `CatalogApi.cs:L356` | consumers guarded → harmless | row stuck `NotPublished`; **no sweeper** | `EventStateEnum` states |
| Basket deleted | OrderStarted event + direct call | `OrderStartedIntegrationEventHandler.cs:L10-L15`, `BasketState.cs:L108` | delete is idempotent | basket lingers (annoyance, not corruption) | logs |
| Stock check | AwaitingValidation event | Catalog handler `:L15-L32` | re-check → same result (read-only + outbox) | order stuck AwaitingValidation | logs only |
| Stock decrement | Paid event | `OrderStatusChangedToPaidIntegrationEventHandler.cs` | **decrement twice = real damage** — *investigate what guards it* | oversell risk later | — |
| Payment simulated | StockConfirmed event | PaymentProcessor handler `:L21-L32` | publishes twice → Ordering guard absorbs | order stuck StockConfirmed | logs |
| Grace-period events | timer poll | `GracePeriodManagerService.cs:L44-L61` | by design, every poll until state changes | next poll retries — self-healing | logs |
| Webhook HTTP calls | order status events | `Webhooks.API` (not read in depth) | third parties must dedupe | delivery not guaranteed | *unknown* |
| UI notification | status events → WebApp | `WebApp/Extensions.cs:L43-L51` | re-render, harmless | user refreshes manually | — |

## The reliability toolkit, as implemented here

- **Idempotency** (safe to run twice): three distinct techniques in one repo — request-id dedup (`IdentifiedCommandHandler`), state-guarded transitions (`Order.cs:L99-L128`), naturally idempotent ops (delete, full-replace `StringSetAsync`). Interviews love "name three ways to achieve idempotency" — you have them.
- **Retries**: publish path retries `BrokerUnreachableException`/`SocketException` with exponential backoff, `2^attempt` seconds (`RabbitMQEventBus.cs:L302-L320`); EF execution strategy retries transient DB failures (`TransactionBehavior.cs:L32`); HTTP resilience handlers come standard from ServiceDefaults. Rule visible in all three: retry only *transient*, transport-level failures — never business failures.
- **Timeouts/backpressure**: largely absent (sample app). Consumer processes messages one at a time (single consumer channel), which is accidental backpressure.
- **At-least-once vs at-most-once**: the consumer acks *after* processing (redelivery if the process dies mid-handler → at-least-once) **but also acks on handler exception** (`RabbitMQEventBus.cs:L177-L180`) → at-most-once under bugs. The code comment itself prescribes the fix: dead-letter exchange. This is the repo's most important known weakness — the maintainers say so in a comment.
- **Compensation, not rollback**: stock rejected ⇒ `SetCancelledStatusWhenStockIsRejected` (`Order.cs:L155-L168`) with a human-readable reason. Distributed systems can't roll back a committed step; they apply a compensating action. That sentence + this anchor = saga question answered.
- **Failure visibility**: every handler logs event id + payload; OTel traces flow through the queue (`RabbitMQEventBus.cs:L86, L144-L146`). Missing: metrics/alerts on stuck orders or `NotPublished` outbox rows — you can *find* failures but nothing *tells* you.

## Where side effects sit in risky places

1. Handler exceptions = silent message loss (ack-anyway, above). Blast radius: any order can freeze mid-pipeline.
2. `IntegrationEventLogService` has no background dispatcher — `RetrieveEventLogsPendingToPublishAsync` (`:L19-L32`) is only invoked with the current transaction id. Crash-after-commit events are orphaned forever.
3. Basket deletion fires from **two places** (event + direct call). Harmless here (idempotent), but a pattern to interrogate: if the direct call succeeded and the event later fails to publish, the flow still works — which means the event path is untested in practice. Redundancy hides rot.
4. Domain event handlers run inside the DB transaction (`OrderingContext.cs:L47-L62`). Anyone who adds an HTTP call in a domain event handler stretches a Postgres transaction across a network call. Nothing prevents it but review.

Interview angle: the whole file is the answer bank for "design a reliable order pipeline," "exactly-once — real or myth?" (myth; you get at-least-once + idempotency), and "how do you handle a failed payment callback?"

Drill: pick the stock-decrement handler (`OrderStatusChangedToPaidIntegrationEventHandler.cs` — you haven't read it yet). Predict, in writing: is it guarded against double delivery? Then read it and grade your prediction.
Self-grade — Basic: read and understood the handler. Solid: correct prediction with reasoning from the patterns above. Strong: if unguarded, you sketched the fix (dedup table keyed by event id, or conditional UPDATE with stock >= units) and the test.
