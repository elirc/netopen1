# ASTRA-046: Derive checkout identity from the authenticated caller

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 8 — Identity and defensive coding  
**Type:** Trust-boundary correction · **Estimate:** 4-7 hours  
**Prerequisites:** [ASTRA-045](ASTRA-045.md), [ASTRA-024](ASTRA-024.md)  
**Read first:** [Stage lesson](../01-lessons/08-identity-and-security.md)

## User story

As a shopper placing an order, I want the server to use my authenticated identity so that a forged payload cannot create an order as someone else.

## Starting point and scope

CreateOrderRequest contains identity fields. Define their compatibility behavior while deriving the acting identity from trusted request context.

- [OrdersApi.cs](../../src/Ordering.API/Apis/OrdersApi.cs)
- [IdentityService.cs](../../src/Ordering.API/Infrastructure/Services/IdentityService.cs)
- [BasketState.cs](../../src/WebApp/Services/BasketState.cs)
- [OrderingApiTests.cs](../../tests/Ordering.FunctionalTests/OrderingApiTests.cs)

## Acceptance criteria

- [ ] A request with conflicting body and principal identities is rejected or uses the principal according to the explicit policy.
- [ ] An accepted order belongs to the authenticated caller.
- [ ] Anonymous access remains rejected by the real configured boundary.
- [ ] The WebApp checkout path and request ID behavior still work.

## Suggested approach

1. Trace which identity fields reach CreateOrderCommand.
2. Choose a clear transition policy for existing client payload fields.
3. Test conflicting identities and normal checkout with test-owned data.

## Verification and evidence

Run Ordering unit and functional tests, plus a local checkout smoke test when the full app is available. State which check uses a test principal and which uses real login.

## Hints, in order

1. Ignoring one UserId field may leave another trusted-looking Buyer field unexamined.
2. A client-generated identity string is not proof of authentication.

## Review conversation

What compatibility tradeoff did you make for existing callers? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
