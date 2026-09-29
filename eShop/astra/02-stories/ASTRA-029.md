# ASTRA-029: Handle products missing from a basket's catalog lookup

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 5 — Basket and state  
**Type:** Cross-service recovery · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-028](ASTRA-028.md)  
**Read first:** [Stage lesson](../01-lessons/05-basket-and-state.md)

## User story

As a shopper with an old basket, I want unavailable products explained so that one deleted catalog item does not prevent me from managing the bag.

## Starting point and scope

FetchCoreAsync indexes the catalog lookup by every basket product ID. Proposed behavior: show an unavailable row, exclude it from purchasable totals, and require removal before checkout.

- [BasketState.cs](../../src/WebApp/Services/BasketState.cs)
- [BasketItem.cs](../../src/WebApp/Services/BasketItem.cs)
- [CartPage.razor](../../src/WebApp/Components/Pages/Cart/CartPage.razor)

## Acceptance criteria

- [ ] One absent catalog record does not crash the entire basket view.
- [ ] The unavailable row has a clear explanation and a working remove action.
- [ ] Other products keep correct prices and quantities; missing data is never treated as a free product.
- [ ] Checkout is blocked with actionable feedback until unavailable rows are removed.

## Suggested approach

1. Create a controlled basket response referencing one missing and one present product.
2. Model the unavailable state explicitly at the enrichment boundary.
3. Update display and checkout guards together, then verify recovery.

## Verification and evidence

Use the WebApp harness from ASTRA-028 or a discovered browser test with local controlled data. Assert missing, all-present, and post-removal scenarios.

## Hints, in order

1. TryGetValue avoids the immediate exception but does not define the user experience.
2. Do not delete arbitrary seeded products to set up a repeatable test.

## Review conversation

How does the UI distinguish unavailable information from a legitimate zero price? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
