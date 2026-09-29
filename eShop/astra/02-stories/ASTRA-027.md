# ASTRA-027: Reject duplicate rows in one basket update

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 5 — Basket and state  
**Type:** Contract consistency · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-026](ASTRA-026.md)  
**Read first:** [Stage lesson](../01-lessons/05-basket-and-state.md)

## User story

As a basket client, I want duplicate product rows rejected clearly so that the server and UI agree on one quantity per product.

## Starting point and scope

Proposed policy: reject duplicate product IDs within one replacement request. This is different from adding a product twice through BasketState, which increments one row.

- [BasketService.cs](../../src/Basket.API/Grpc/BasketService.cs)
- [BasketState.cs](../../src/WebApp/Services/BasketState.cs)
- [BasketServiceTests.cs](../../tests/Basket.UnitTests/BasketServiceTests.cs)

## Acceptance criteria

- [ ] Two rows with the same product ID cause InvalidArgument.
- [ ] Duplicate detection occurs before persistence even if all quantities are valid.
- [ ] Distinct products and an empty list still succeed.
- [ ] Ordinary repeated UI additions still result in one row with accumulated quantity.

## Suggested approach

1. Write duplicate and distinct-row service tests.
2. Add a simple uniqueness check after defining the request policy.
3. Smoke-test repeated additions through the existing browser journey.

## Verification and evidence

Run Basket.UnitTests and the relevant logged-in browser test. Record both direct malformed requests and normal UI additions.

## Hints, in order

1. Grouping and summing duplicates would implement a different policy.
2. Do not confuse two sequential requests with duplicate rows inside one request.

## Review conversation

Why did this story choose rejection instead of implicit merging? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
