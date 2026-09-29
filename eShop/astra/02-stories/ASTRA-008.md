# ASTRA-008: Characterize order totals with meaningful values

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 2 — C# and focused tests  
**Type:** First unit test · **Estimate:** 1-3 hours  
**Prerequisites:** [ASTRA-007](ASTRA-007.md)  
**Read first:** [Stage lesson](../01-lessons/02-csharp-and-testing-basics.md)

## User story

As an order maintainer, I want tests for current totals so that future changes preserve the agreed arithmetic.

## Starting point and scope

Add focused tests in Ordering.UnitTests. Current GetTotal sums units times price and does not subtract Discount; capture that behavior without inventing new discount policy.

- [Order.cs](../../src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs)
- [OrderAggregateTest.cs](../../tests/Ordering.UnitTests/Domain/OrderAggregateTest.cs)
- [Builders.cs](../../tests/Ordering.UnitTests/Builders.cs)

## Acceptance criteria

- [ ] A draft or appropriately constructed empty order totals zero.
- [ ] Two distinct products with decimal prices produce the hand-calculated total.
- [ ] The test data would catch ignoring quantity or rounding to integers.
- [ ] A deliberate wrong assertion fails for the intended reason before being restored.

## Suggested approach

1. Use the existing builders and read GetTotal.
2. Calculate expected values by hand using decimal literals.
3. Add small MSTest methods and run the Ordering unit-test project.

## Verification and evidence

Record dotnet test --project tests/Ordering.UnitTests/Ordering.UnitTests.csproj and the assertion failure experiment. Assert the numeric outcome, not only object existence.

## Hints, in order

1. Use values such as 2 × 12.50 plus 3 × 1.25.
2. Avoid copying the production Sum expression into the assertion.

## Review conversation

Which plausible implementation bug would each test catch? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
