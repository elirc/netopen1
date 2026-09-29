# ASTRA-033: Turn order transitions into a tested state table

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 6 — Persistence and domain rules  
**Type:** Domain characterization · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-032](ASTRA-032.md)  
**Read first:** [Stage lesson](../01-lessons/06-data-and-domain.md)

## User story

As an order maintainer, I want explicit transition coverage so that future changes do not accidentally ship or cancel orders in invalid states.

## Starting point and scope

Characterize existing Order transition methods, including their differing invalid-transition behavior. Do not force a uniform policy in this story.

- [Order.cs](../../src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs)
- [OrderStatus.cs](../../src/Ordering.Domain/AggregatesModel/OrderAggregate/OrderStatus.cs)
- [OrderAggregateTest.cs](../../tests/Ordering.UnitTests/Domain/OrderAggregateTest.cs)

## Acceptance criteria

- [ ] The table covers submitted, awaiting validation, stock confirmed, paid, shipped, and cancelled states.
- [ ] Shipping from paid succeeds; shipping from an invalid state throws.
- [ ] Cancellation restrictions on paid and shipped orders are covered.
- [ ] At least one no-op transition and its lack of extra state change or events are asserted.

## Suggested approach

1. Read each transition and list its guard.
2. Build starting states through public domain methods.
3. Assert final status and relevant emitted domain events.

## Verification and evidence

Run Ordering.UnitTests. Include the state table and explain which invalid calls throw versus leave the state unchanged.

## Hints, in order

1. Do not mutate private setters through reflection merely to avoid valid setup.
2. Some repeated transitions can still emit events; inspect before asserting idempotency.

## Review conversation

Which transition would need a separate policy discussion before changing its semantics? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
