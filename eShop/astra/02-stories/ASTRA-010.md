# ASTRA-010: Test domain guard boundaries

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 2 — C# and focused tests  
**Type:** Boundary testing · **Estimate:** 1-3 hours  
**Prerequisites:** [ASTRA-009](ASTRA-009.md)  
**Read first:** [Stage lesson](../01-lessons/02-csharp-and-testing-basics.md)

## User story

As a domain maintainer, I want boundary tests so that invalid item changes cannot silently corrupt an order.

## Starting point and scope

Cover existing OrderItem constructor, AddUnits, and SetNewDiscount guards. Distinguish the constructor's positive quantity requirement from AddUnits allowing zero.

- [OrderItem.cs](../../src/Ordering.Domain/AggregatesModel/OrderAggregate/OrderItem.cs)
- [OrderAggregateTest.cs](../../tests/Ordering.UnitTests/Domain/OrderAggregateTest.cs)

## Acceptance criteria

- [ ] Constructor tests cover zero, negative, and valid units.
- [ ] AddUnits tests cover negative, zero, and positive increments.
- [ ] A rejected operation leaves the prior item's state unchanged.
- [ ] Discount tests describe the current guard rather than imposing an unapproved pricing rule.

## Suggested approach

1. Write the expected behavior table before coding.
2. Add only missing boundary coverage using the existing MSTest style.
3. Use exact exception assertions where the domain contract calls for them.

## Verification and evidence

Run Ordering.UnitTests and include one example proving state did not change after rejection. Explain any case that currently lacks a guard instead of silently fixing it.

## Hints, in order

1. An exception assertion alone does not prove state preservation.
2. Constructor and mutation methods can have different input contracts.

## Review conversation

Which unguarded input would you raise as a separate product question? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
