# ASTRA-026: Validate basket product IDs and quantities

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 5 — Basket and state  
**Type:** gRPC validation feature · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-025](ASTRA-025.md)  
**Read first:** [Stage lesson](../01-lessons/05-basket-and-state.md)

## User story

As a shopper, I want malformed basket rows rejected before saving so that stored quantities remain usable.

## Starting point and scope

Proposed gRPC policy: positive product IDs and quantities from 1 to 99. A valid empty list is still allowed; UI zero-quantity removal sends a list without that row.

- [BasketService.cs](../../src/Basket.API/Grpc/BasketService.cs)
- [basket.proto](../../src/Basket.API/Proto/basket.proto)
- [BasketServiceTests.cs](../../tests/Basket.UnitTests/BasketServiceTests.cs)

## Acceptance criteria

- [ ] Zero/negative product IDs and quantities outside 1-99 return InvalidArgument.
- [ ] The complete request is validated before any repository write.
- [ ] An empty list and valid boundary quantities are accepted.
- [ ] A mixed valid/invalid request produces no partial persistence.

## Suggested approach

1. Add invalid-input tests with a valid first row and invalid second row.
2. Validate at the service boundary before mapping and saving.
3. Keep the protobuf wire fields unchanged.

## Verification and evidence

Run Basket.UnitTests and the web build. Demonstrate acceptance at 1 and 99, rejection at 0 and 100, and no repository call on invalid input.

## Hints, in order

1. Do not reuse UI zero-means-remove semantics as a stored row.
2. Returning an empty response would conceal the caller's invalid request.

## Review conversation

Where does the quantity cap come from, and how is that proposed policy documented? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
