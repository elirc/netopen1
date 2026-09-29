# ASTRA-036: Prove order writes roll back together

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 6 — Persistence and domain rules  
**Type:** Transaction integration lab · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-035](ASTRA-035.md)  
**Read first:** [Stage lesson](../01-lessons/06-data-and-domain.md)

## User story

As an order maintainer, I want a failed local transaction to leave no partial order so that related database state stays consistent.

## Starting point and scope

Use Ordering's existing transaction behavior and local database. This story proves a local transaction boundary, not a transaction spanning RabbitMQ or Redis.

- [TransactionBehavior.cs](../../src/Ordering.API/Application/Behaviors/TransactionBehavior.cs)
- [OrderingContext.cs](../../src/Ordering.Infrastructure/OrderingContext.cs)
- [OrderingIntegrationEventService.cs](../../src/Ordering.API/Application/IntegrationEvents/OrderingIntegrationEventService.cs)
- [OrderingApiFixture.cs](../../tests/Ordering.FunctionalTests/OrderingApiFixture.cs)

## Acceptance criteria

- [ ] A controlled failure before commit leaves no test-owned order row.
- [ ] Related integration-event intent written in that transaction also rolls back.
- [ ] A corresponding success case commits the intended rows.
- [ ] Verification uses a fresh context rather than trusting tracked objects after failure.

## Suggested approach

1. Trace BeginTransactionAsync and CommitTransactionAsync before creating the test.
2. Introduce failure through a test-only seam inside the transaction boundary.
3. Inspect persisted state from a fresh scope after completion.

## Verification and evidence

Run the appropriate Docker-backed functional test and record the deterministic failure point. If a new test helper is needed, keep it outside production runtime configuration.

## Hints, in order

1. A fault after commit tests a different guarantee.
2. In-memory object state does not prove what the database committed.

## Review conversation

Which failure window remains after this transaction test passes? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
