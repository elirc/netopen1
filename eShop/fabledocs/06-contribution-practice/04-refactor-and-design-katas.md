# Refactor & Design Katas

Judgment reps. Output is usually a document or a small diff; grade yourself with the criteria attached. Do these *after* the corresponding modules.

## Kata A: Boundary-leak remediation memo (OrderProcessor raw SQL)
Task: write one page: keep, wrap, or replace `GracePeriodManagerService`'s direct query (`GracePeriodManagerService.cs:L69-L74`)? Cover: coupling cost, the API alternative's new failure modes, the "schema-drift canary test" middle path.
Self-grade — Strong: your recommendation is *keep + canary test* or a better-argued alternative; you priced each option in failure modes, not aesthetics. (The critique file's position is one answer, not the answer.)

## Kata B: Design the outbox dispatcher (before reading M1)
Task: from `IntegrationEventLogService.cs` alone, design the sweeper: query, locking, retry policy, idempotency interaction. Then compare against ticket M1's design questions.
Self-grade — Solid: you independently hit the replica-race problem. Strong: you also handled poison events (max TimesSent → Failed-terminal + alert).

## Kata C: Split `CatalogApi.cs`
Task: 423 lines, queries + mutations + AI search + images in one static class. Propose a split that *improves* something measurable (review surface, test targeting, ownership) — or argue for leaving it. Constraint: routes must not change.
Self-grade — Strong: you noticed a split by *change-reason* (search evolves with AI; images with CDN work; CRUD is stable) beats a split by HTTP verb; and you said what stays together and why.

## Kata D: Remove the duplication in the six status-changed handlers
Task: WebApp has six near-identical `OrderStatusChangedTo*IntegrationEventHandler` classes (`WebApp/Services/OrderStatus/IntegrationEvents/`). Design the dedup (generic handler? single event with status field? — the latter changes the *wire contract*, the former only the code). State what you gain and what you lose (explicitness, per-event divergence room).
Self-grade — Strong: you rejected the wire-contract change and can say why event *types* (not a status enum) are load-bearing: routing keys = class names (`RabbitMQEventBus.cs:L33`), so one-event-with-field changes subscription granularity for every service.

## Kata E: Type-safety upgrade — strongly-typed IDs (scoped)
Task: from module 02/03's drill, produce the actual small diff for `BuyerId` in Ordering.Domain only, with EF value-converter. Measure the churn honestly (files touched, test changes).
Self-grade — Solid: compiles, tests pass. Strong: your PR description quantifies cost vs the bug class prevented, and you *recommend against proceeding* if the numbers don't justify it. (Recommending against your own work is a senior signal.)

## Kata F: Migration design — split `Description` from status text
Task: `Order.Description` mixes machine state narration ("The order was cancelled.") with data (rejected product names, `Order.cs:L155-L168`). Design the schema + code migration to a structured `CancellationReason` (expand/contract, backfill parsing? or forward-only?), including what the UI and query DTOs do during the window.
Self-grade — Strong: forward-only with legacy fallback read, and you explicitly declined to parse old free text.

## Kata G: Write the RFC — "HTTP contract honesty for order commands" (R3)
Task: full RFC per the template in [../07-career-and-collaboration/02-writing-prs-and-rfcs.md](../07-career-and-collaboration/02-writing-prs-and-rfcs.md): problem, options (fix swallow / API-layer patch / status quo), consumer impact audit, rollout (versioned? coordinated deploy?).
Self-grade — Strong: your RFC's "risks" section found the WebApp's current behavior on non-2xx (you read `OrderingService.cs` to write it).

## Kata H: Review a flawed PR, out loud, timed
Task: kata 2 or 6 from the review gym, 20-minute timer, spoken as if pairing with the author. Record it.
Self-grade — Solid: findings correctly graded, tone kind. Strong: you opened with what's *good* in the PR, asked one genuine question before asserting, and offered a concrete next step for each blocking item.
