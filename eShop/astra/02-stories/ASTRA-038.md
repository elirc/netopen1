# ASTRA-038: Create reusable test data without hidden state

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 7 — Reliable test suites  
**Type:** Test maintainability · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-037](ASTRA-037.md)  
**Read first:** [Stage lesson](../01-lessons/07-testing-strategy.md)

## User story

As a test author, I want readable data builders so that each scenario declares what matters without copying a large setup.

## Starting point and scope

Use existing Ordering builders as an example. Improve repeated setup in one suite only, preserving per-test ownership and behavior.

- [Builders.cs](../../tests/Ordering.UnitTests/Builders.cs)
- [OrderAggregateTest.cs](../../tests/Ordering.UnitTests/Domain/OrderAggregateTest.cs)
- [CatalogApiTests.cs](../../tests/Catalog.FunctionalTests/CatalogApiTests.cs)

## Acceptance criteria

- [ ] A selected repeated setup becomes a small builder or factory with sensible explicit defaults.
- [ ] Tests can override the values central to their scenario.
- [ ] Each call creates independent mutable objects and unique persisted data where needed.
- [ ] Assertions remain visible in the test rather than hidden in the builder.

## Suggested approach

1. Choose at least three examples of meaningful repeated setup.
2. Extract creation only, leaving behavior and assertions local.
3. Verify mutating one created object does not affect another.

## Verification and evidence

Run the selected test project and review before/after test readability. Add an independence check only if shared mutable defaults are a realistic concern.

## Hints, in order

1. A builder that calls production business logic can hide the setup's meaning.
2. Avoid a universal fixture abstraction spanning unrelated services.

## Review conversation

Does the reader still see why each test should pass? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
