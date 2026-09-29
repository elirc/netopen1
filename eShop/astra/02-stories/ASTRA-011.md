# ASTRA-011: Verify anonymous basket reads never reach storage

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 2 — C# and focused tests  
**Type:** Mock-boundary testing · **Estimate:** 1-3 hours  
**Prerequisites:** [ASTRA-010](ASTRA-010.md)  
**Read first:** [Stage lesson](../01-lessons/02-csharp-and-testing-basics.md)

## User story

As an anonymous visitor, I want an empty basket response so that browsing does not require a user-specific storage lookup.

## Starting point and scope

Strengthen the existing GetBasketReturnsEmptyForNoUser test using IBasketRepository and the supplied gRPC context helper. Preserve the existing anonymous-read behavior.

- [BasketServiceTests.cs](../../tests/Basket.UnitTests/BasketServiceTests.cs)
- [TestServerCallContext.cs](../../tests/Basket.UnitTests/Helpers/TestServerCallContext.cs)
- [BasketService.cs](../../src/Basket.API/Grpc/BasketService.cs)

## Acceptance criteria

- [ ] An anonymous read returns an empty CustomerBasketResponse.
- [ ] The repository receives no GetBasketAsync call for that request.
- [ ] A known authenticated subject reads the matching user's key.
- [ ] Each test owns its substitute and call context.

## Suggested approach

1. Read how the helper stores HttpContext in the call context.
2. Add a no-interaction assertion to the anonymous case.
3. Use a distinctive synthetic subject value for the authenticated case.

## Verification and evidence

Run dotnet test --project tests/Basket.UnitTests/Basket.UnitTests.csproj. Record why this service test does not prove actual token authentication.

## Hints, in order

1. Look for context.GetUserIdentity in the service.
2. NSubstitute can verify a call was not received.

## Review conversation

Why is avoiding a repository call part of this behavior? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
