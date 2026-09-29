# ASTRA-052: Prototype duplicate-safe stock processing

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 9 — Events and consistency  
**Type:** Advanced consistency spike · **Estimate:** 6-10 hours  
**Prerequisites:** [ASTRA-051](ASTRA-051.md), [ASTRA-032](ASTRA-032.md)  
**Read first:** [Stage lesson](../01-lessons/09-events-and-consistency.md)

## User story

As an inventory maintainer, I want duplicate paid-order events to avoid removing stock twice so that message replay does not corrupt quantities.

## Starting point and scope

The current paid-event handler decrements stock without a deduplication record. Design and prototype one durable processed-event boundary in Catalog, with mentor review.

- [OrderStatusChangedToPaidIntegrationEventHandler.cs](../../src/Catalog.API/IntegrationEvents/EventHandling/OrderStatusChangedToPaidIntegrationEventHandler.cs)
- [CatalogContext.cs](../../src/Catalog.API/Infrastructure/CatalogContext.cs)
- [IntegrationEvent.cs](../../src/EventBus/Events/IntegrationEvent.cs)

## Acceptance criteria

- [ ] Replaying the same event ID through fresh contexts removes stock once.
- [ ] Different event IDs remain distinct operations.
- [ ] The deduplication marker and stock change commit or roll back together.
- [ ] A simultaneous duplicate case has a database-enforced outcome or an explicitly demonstrated unresolved limitation.

## Suggested approach

1. Write an ADR comparing an in-memory set and a durable unique marker.
2. Prototype the durable approach in a practice branch with any required migration.
3. Use a controlled stock value and two deliveries, then inject failure before commit.

## Verification and evidence

Run database-backed duplicate and rollback tests, including a concurrency experiment. If concurrency remains unresolved, label the spike incomplete for a production guarantee and record the next step.

## Hints, in order

1. An in-memory HashSet forgets history after restart.
2. Saving a marker before a failed stock change can permanently suppress valid retry.

## Review conversation

Which database constraint and transaction make the effect durable? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
