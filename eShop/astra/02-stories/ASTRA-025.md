# ASTRA-025: Test unauthenticated basket mutations

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 5 — Basket and state  
**Type:** gRPC boundary tests · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-024](ASTRA-024.md)  
**Read first:** [Stage lesson](../01-lessons/05-basket-and-state.md)

## User story

As a basket owner, I want unauthenticated writes rejected so that an anonymous caller cannot mutate stored baskets.

## Starting point and scope

UpdateBasket and DeleteBasket already guard missing identity. Add coverage to the current small basket suite without redesigning authentication.

- [BasketService.cs](../../src/Basket.API/Grpc/BasketService.cs)
- [BasketServiceTests.cs](../../tests/Basket.UnitTests/BasketServiceTests.cs)
- [TestServerCallContext.cs](../../tests/Basket.UnitTests/Helpers/TestServerCallContext.cs)

## Acceptance criteria

- [ ] Missing identity produces StatusCode.Unauthenticated for update and delete.
- [ ] Neither rejected operation calls its repository mutation.
- [ ] Authenticated operations pass the subject identity to storage.
- [ ] Anonymous GetBasket keeps its established empty-read behavior.

## Suggested approach

1. Reuse the context helper and fresh substitutes.
2. Test update and delete separately with absent and present subjects.
3. Assert status codes and side-effect boundaries.

## Verification and evidence

Run Basket.UnitTests. Explain that real token validation requires a hosted transport test and is not established by the fake call context.

## Hints, in order

1. An empty ClaimsPrincipal and one with a sub claim exercise different branches.
2. Catch the RpcException through the framework's async exception assertion.

## Review conversation

Why is a no-write assertion needed in addition to an error status? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
