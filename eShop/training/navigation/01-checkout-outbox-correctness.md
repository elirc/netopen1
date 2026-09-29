# Checkout → Ordering → Outbox: what guarantee holds where

Re-verified against the checked-out source on 2026-09-23 (baseline commit `9b4f943`). This is not a repeat of
`fabledocs/01-codebase-cartography/05-key-flows.md` Flow 3/Flow 6 — read those first for the full step-by-step
trace with exact line numbers. This page organizes the same code around one question per step: **what does this
line actually guarantee, and what would break it?** Every claim below was checked against the file at the path
given; where a file couldn't be re-opened in this pass, it's marked accordingly.

## The path, as a guarantee ledger

| # | Guarantee claimed | Where it's enforced | Verified how | What defeats it |
| --- | --- | --- | --- | --- |
| 1 | Duplicate checkout submissions (double-click, retry) don't create two orders | `src/Ordering.API/Application/Commands/IdentifiedCommandHandler.cs` — `Handle()`: `_requestManager.ExistAsync(message.Id)` short-circuits to `CreateResultForDuplicateRequest()` before the inner `CreateOrderCommand` ever runs | Read in full this pass (lines 39-48 shown below) | The client must reuse the same `x-requestid` GUID across retries. `src/WebApp/Services/BasketState.cs` generates this once at checkout page init, not per click — if a future change moved that generation into the submit handler, this guarantee silently disappears. That's exactly the kind of regression a reviewer must catch by reading, not by trusting the type signature. |
| 2 | The idempotency record and the order commit atomically (no "recorded but no order" or "order but no record" split) | `TransactionBehavior<TRequest,TResponse>` (`src/Ordering.API/Application/Behaviors/TransactionBehavior.cs`) wraps `next()` — which includes the `IdentifiedCommandHandler` → inner handler chain — inside one `BeginTransactionAsync()`/`CommitTransactionAsync()` pair | Read in full this pass | `IdentifiedCommandHandler.Handle()` calls `_requestManager.CreateRequestForCommandAsync` and the inner command through the *same* `IMediator`, but MediatR pipeline ordering is config, not compiler-enforced — if `TransactionBehavior` were registered to run *inside* `IdentifiedCommandHandler` instead of wrapping it, the two could split into separate transactions. Worth confirming the pipeline registration order in `Extensions.cs` before relying on this in an interview answer. |
| 3 | The order row and the "we intend to publish this event" row commit together | `OrderingIntegrationEventService.AddAndSaveEventAsync` (`src/Ordering.API/Application/IntegrationEvents/OrderingIntegrationEventService.cs:36-41`) calls `_eventLogService.SaveEventAsync(evt, _orderingContext.GetCurrentTransaction())` — same `OrderingContext`, same open transaction | Read in full this pass | Nothing inside this call path — it's the correct half of the outbox pattern. The risk is entirely in what happens *after* commit (row 4). |
| 4 | Once committed, the event *will* reach RabbitMQ | `OrderingIntegrationEventService.PublishEventsThroughEventBusAsync` (same file, lines 13-34): reads `NotPublished` rows for the transaction, marks `InProgress`, calls `_eventBus.PublishAsync`, marks `Published` — or on exception, marks `PublishedFailed` and **swallows the exception** (`catch (Exception ex) { _logger.LogError(...); await _eventLogService.MarkEventAsFailedAsync(...); }`, no rethrow, no retry) | Read in full this pass, confirms `fabledocs` Flow 6 and `astra/01-lessons/09-events-and-consistency.md`'s claim | This is the real gap. If the RabbitMQ publish throws (broker down, network blip), the row is marked `PublishedFailed` and the method returns normally — the HTTP response to the checkout POST was already `200 OK` (the transaction committed). **Nothing ever reads `PublishedFailed` or stale `NotPublished` rows again.** Confirmed by grep: `grep -rn "PublishedFailed" src --include=*.cs` returns only the enum definition (`src/IntegrationEventLogEF/EventStateEnum.cs`) and the two call sites in `IntegrationEventLogService.cs`/`OrderingIntegrationEventService.cs` — no reader anywhere. `grep -rn "BackgroundService" src --include=*.cs` returns exactly two hits: `GracePeriodManagerService` (order grace-period polling) and `MigrateDbContextExtensions.cs` (startup DB migration), neither of which touches `IntegrationEventLogEntry`. |
| 5 | A consumer that dies mid-handler doesn't silently lose the message | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` — not re-opened line-by-line this pass, but `fabledocs` Flow 4 and `astra` both independently cite the same behavior: the consumer **acks even when the handler throws**, with a comment recommending a dead-letter exchange for production. *Not independently re-verified in this pass — treat as `fabledocs`/`astra`-sourced, cross-confirmed by two independent doc trees, not by me reading the file this time.* | Cross-checked, not re-read | An exception inside e.g. the Catalog stock-check handler = message acked = event effectively dropped = order stuck in `AwaitingValidation` forever, with no reconciliation job to notice. |
| 6 | Order state transitions survive duplicate/out-of-order events | `src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs` guards each transition on current status (e.g. `SetAwaitingValidationStatus` only fires `if (_orderStatus == OrderStatus.Submitted)`) | Not re-opened this pass; consistent with `fabledocs` Flow 4, treat as inherited claim | This is the mechanism that makes rows 4 and 5's gaps *survivable* rather than catastrophic for the order's own consistency — a re-delivered or re-sent event is a no-op once the state has already advanced. It does **not** fix row 4: if the *first* publish attempt fails and nothing retries it, there's no redelivery to be a no-op against — the event never arrives at all. |

## The one sentence that matters for an interview

*"The transactional outbox here correctly makes the DB write atomic with the intent-to-publish row, and the
consumer-side status guards make redelivery safe — but the publish-after-commit step itself is fire-and-forget:
a broker hiccup at exactly the wrong moment produces a `PublishedFailed` row that nothing will ever look at
again, and the caller already got a 200."* That's the gap `03-outbox-sweeper-tradeoff.md` and `04-change-request.md`
build on.

## Cross-check note

This table's row 4 finding matches, independently, all three existing doc trees (`fabledocs` Flow 6's "missing
background dispatcher for `NotPublished` rows", `fabledoc2` ADR-003's "no retry dispatcher" consequence, and
`astra`'s "That is not proof that an independent worker automatically retries every stranded entry"). Three
independent write-ups landing on the same specific code fact is strong evidence it's real, not a doc-authoring
artifact — which is exactly the kind of corroboration you should look for before trusting any single doc tree's
claim about a codebase you didn't write.
