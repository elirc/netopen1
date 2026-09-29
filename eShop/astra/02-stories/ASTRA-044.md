# ASTRA-044: Restrict order detail reads to the owner

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 8 — Identity and defensive coding  
**Type:** Authorization feature · **Estimate:** 4-7 hours  
**Prerequisites:** [ASTRA-043](ASTRA-043.md), [ASTRA-023](ASTRA-023.md)  
**Read first:** [Stage lesson](../01-lessons/08-identity-and-security.md)

## User story

As an order owner, I want other shoppers prevented from reading my order details so that my address and purchases stay private.

## Starting point and scope

Implement the owner-only detail-read policy from ASTRA-043 using trusted identity. Preserve genuine missing-order handling and unexpected-failure visibility.

- [OrdersApi.cs](../../src/Ordering.API/Apis/OrdersApi.cs)
- [IOrderQueries.cs](../../src/Ordering.API/Application/Queries/IOrderQueries.cs)
- [OrderQueries.cs](../../src/Ordering.API/Application/Queries/OrderQueries.cs)
- [OrderingApiTests.cs](../../tests/Ordering.FunctionalTests/OrderingApiTests.cs)

## Acceptance criteria

- [ ] The owner can read the order.
- [ ] A second authenticated user receives the documented 404 and no order fields.
- [ ] A missing order returns the same public not-found shape.
- [ ] Unexpected infrastructure failure remains distinguishable from a missing or concealed order.

## Suggested approach

1. Pass trusted identity to the appropriate query boundary.
2. Filter by order and buyer together rather than loading sensitive data for the caller first.
3. Update callers and tests for any interface change.

## Verification and evidence

Run Ordering unit and functional tests with two controlled principals and test-owned orders. Include an actual HTTP response-body assertion for the non-owner.

## Hints, in order

1. A test mocking the query cannot prove its SQL ownership predicate.
2. Avoid weakening ASTRA-023's narrowed exception behavior.

## Review conversation

What prevents a caller from supplying another user's ID to bypass this check? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
