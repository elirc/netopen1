# ASTRA-051: Map integration-event log failure windows

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 9 — Events and consistency  
**Type:** Consistency investigation · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-050](ASTRA-050.md), [ASTRA-036](ASTRA-036.md)  
**Read first:** [Stage lesson](../01-lessons/09-events-and-consistency.md)

## User story

As an operator, I want to know where publish intent can remain unfinished so that I can design recovery based on evidence.

## Starting point and scope

Inspect NotPublished, InProgress, Published, and PublishedFailed transitions and transaction-scoped retrieval. This story produces a tested state analysis, not an automatic recovery worker.

- [IntegrationEventLogService.cs](../../src/IntegrationEventLogEF/Services/IntegrationEventLogService.cs)
- [EventStateEnum.cs](../../src/IntegrationEventLogEF/EventStateEnum.cs)
- [OrderingIntegrationEventService.cs](../../src/Ordering.API/Application/IntegrationEvents/OrderingIntegrationEventService.cs)
- [TransactionBehavior.cs](../../src/Ordering.API/Application/Behaviors/TransactionBehavior.cs)

## Acceptance criteria

- [ ] Describe behavior before commit, after commit/before publish, after publish/before status update, and after publish failure.
- [ ] Identify which states the current retrieval method selects.
- [ ] Locate any recovery mechanism or explicitly state it was not found in the inspected scope.
- [ ] Use a test double to verify the publisher's success and failure status-call sequence.

## Suggested approach

1. Draw a timeline and annotate persisted state at each interruption.
2. Reuse a justified Ordering test boundary or propose a focused new harness.
3. Force PublishAsync to fail and inspect the resulting log-service calls.

## Verification and evidence

Run the selected tests and submit the failure-window table. Do not equate a mocked status call with a persisted database row; use a functional check for that claim.

## Hints, in order

1. The retrieval method filters by transaction ID as well as state.
2. An entry marked failed is not selected by a predicate for NotPublished.

## Review conversation

Which unfinished state would your first recovery design need to handle? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
