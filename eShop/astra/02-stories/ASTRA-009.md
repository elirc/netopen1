# ASTRA-009: Prove repeated product additions merge correctly

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 2 — C# and focused tests  
**Type:** Unit-test practice · **Estimate:** 1-3 hours  
**Prerequisites:** [ASTRA-008](ASTRA-008.md)  
**Read first:** [Stage lesson](../01-lessons/02-csharp-and-testing-basics.md)

## User story

As a shopper, I want repeated additions of the same product to accumulate predictably so that my order has one coherent line for it.

## Starting point and scope

Characterize Order.AddOrderItem's existing merge behavior, including choosing the higher discount. Do not alter discount calculation semantics.

- [Order.cs](../../src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs)
- [OrderItem.cs](../../src/Ordering.Domain/AggregatesModel/OrderAggregate/OrderItem.cs)
- [OrderAggregateTest.cs](../../tests/Ordering.UnitTests/Domain/OrderAggregateTest.cs)

## Acceptance criteria

- [ ] Adding the same product twice yields one line with summed units.
- [ ] Adding a distinct product yields a separate line.
- [ ] A higher later discount replaces the existing discount; a lower one does not.
- [ ] Tests assert line identity, quantity, and discount, not only total.

## Suggested approach

1. Trace the existing-product and new-product branches.
2. Build a small table of two-step additions.
3. Implement missing cases using fresh orders per test.

## Verification and evidence

Run Ordering.UnitTests and demonstrate that a wrong product-ID comparison would fail a test. Preserve the existing tests' semantics.

## Hints, in order

1. Use a stable product ID and deliberately different product names only when testing identity policy.
2. A correct total can still hide duplicate lines.

## Review conversation

Why should the assertion include line count as well as total? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
