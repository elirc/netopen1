# Observability & Operations

The question that organizes this file: **"how would I know this broke?"** — asked per flow.

## What exists

- **Traces:** OpenTelemetry wired via ServiceDefaults for HTTP/gRPC/EF, *and through the bus* — trace context is injected into RabbitMQ headers on publish (`RabbitMQEventBus.cs:L86`) and extracted on consume (`:L144-L146`), with messaging semantic-convention tags (`:L113-L125`). One checkout = one distributed trace across five services. This is genuinely production-grade.
- **Logs:** structured logging everywhere, with disciplined `IsEnabled` guards for hot paths (`BasketService.cs:L21-L24`) and scopes carrying transaction/request ids (`TransactionBehavior.cs:L39`, `OrdersApi.cs:L138`).
- **Health:** `/health` (readiness, includes dependencies) and `/alive` endpoints from ServiceDefaults; AppHost gates startup on them (`eShop.AppHost/Program.cs:L26,L43`).
- **Metrics:** runtime + ASP.NET defaults via OTel. **No domain metrics** — nothing counts orders created, payments failed, events dead-lettered (there's no DLQ to count).

## "How would I know?" per flow

| Flow | Failure | Today you'd know by… | Should be |
| --- | --- | --- | --- |
| Browse | Catalog down | health check + WebApp errors | fine |
| Basket | Redis down | gRPC errors in traces | fine; add Redis health contribution |
| Checkout | validation silently swallowed (R3) | **nothing** — 200s everywhere, a Warning log nobody watches | alert on `CreateOrderCommand failed` warnings; fix the contract |
| Checkout | outbox row stuck NotPublished (R2) | **nothing** — requires ad-hoc SQL | gauge: outbox backlog age > 1 min → alert |
| Order pipeline | event lost to handler exception (R1) | a Warning "Error Processing message" then silence; order frozen | DLQ + depth metric; plus a *business* alert: orders in AwaitingValidation > 15 min |
| Order pipeline | consumer never connected (bus startup failed, `RabbitMQEventBus.cs:L287-L290`) | service reports healthy, does nothing | health check on consumer channel state (ticket 9) |
| Workers | grace-period loop dead | orders stop progressing; no direct signal | heartbeat metric per loop iteration |
| Webhooks | third-party endpoint down | *unknown (not read)* | delivery success rate + retry queue depth |

The pattern in the "Should be" column: **alert on business invariants, not just infrastructure**. "No order has been Submitted-and-stuck for >15 min" catches R1, R2, dead workers, and broker outages with *one* rule — that's the senior version of monitoring, and a killer interview line.

## Error handling as observability

Where errors are *made visible*: ProblemDetails (`Catalog.API/Program.cs:L5,L19`), exception → trace tags (`RabbitMQEventBus.SetExceptionTags`), WebApp `/Error` page + HSTS split by environment (`WebApp/Program.cs:L17-L22`).
Where errors are *hidden* (the anti-patterns to name): `IdentifiedCommandHandler.cs:L99-L102` (swallow → default), `OrdersApi.cs:L82-L90` (any exception → 404), bus ack-on-error. Observability isn't a tool choice — it's the sum of these small decisions.

## Deploy & rollback posture

Dev: Aspire. Prod: `azd up` to Azure Container Apps (README) — per-service revisions give container-level rollback. The two things that *don't* roll back with a container: **database migrations** (auto-applied at startup, R10 — a rolled-back service still faces the migrated schema; this is why expand/contract in module 03/02 matters) and **in-flight messages** (a new event version in the queue meets old consumer code — version events additively).

Interview angle: "How do you debug a request across services?" (trace id through the queue — you have the exact mechanism), "What would you alert on?" (business invariants), "What breaks a rollback?" (migrations + queued messages). Three questions, all now answered from one repo.

Drill: write the five alerts you'd ship first, each as: metric, threshold, and which failure from the table it catches. Self-grade — Strong: at least one alert catches multiple failure modes, and none fires on a healthy system during deploy.
