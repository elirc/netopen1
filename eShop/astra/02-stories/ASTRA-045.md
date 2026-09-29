# ASTRA-045: Restrict order mutations to the owner

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 8 — Identity and defensive coding  
**Type:** Authorization feature · **Estimate:** 4-7 hours  
**Prerequisites:** [ASTRA-044](ASTRA-044.md)  
**Read first:** [Stage lesson](../01-lessons/08-identity-and-security.md)

## User story

As an order owner, I want another shopper unable to cancel or ship my order so that state changes require the correct authority.

## Starting point and scope

Apply the course owner-only policy to cancel and ship, preserving each domain transition rule. Administrative fulfillment roles remain a separate design question.

- [OrdersApi.cs](../../src/Ordering.API/Apis/OrdersApi.cs)
- [CancelOrderCommandHandler.cs](../../src/Ordering.API/Application/Commands/CancelOrderCommandHandler.cs)
- [ShipOrderCommandHandler.cs](../../src/Ordering.API/Application/Commands/ShipOrderCommandHandler.cs)
- [OrderingApiTests.cs](../../tests/Ordering.FunctionalTests/OrderingApiTests.cs)

## Acceptance criteria

- [ ] A non-owner cannot cancel or ship another user's test order.
- [ ] Denied operations leave order status and related event intent unchanged.
- [ ] An owner can perform only transitions already valid for the current state.
- [ ] Missing and non-owned orders follow the chosen concealed-not-found policy.

## Suggested approach

1. Decide where ownership belongs relative to request deduplication and domain mutation.
2. Pass trusted identity through the chosen boundary and update affected contracts.
3. Use fresh contexts to inspect state after denied operations.

## Verification and evidence

Run Ordering unit and functional tests for two principals, both operations, and valid/invalid states. Check persisted effects rather than status codes alone.

## Hints, in order

1. A successful authorization check does not make shipping an unpaid order valid.
2. Decide whether a denied request should consume a deduplication key.

## Review conversation

What would need to change if an administrator were allowed to ship any order? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
