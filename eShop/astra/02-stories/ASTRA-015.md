# ASTRA-015: Help shoppers recover from a missing product

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 3 — Blazor and accessible UI  
**Type:** UI recovery · **Estimate:** 2-4 hours  
**Prerequisites:** [ASTRA-014](ASTRA-014.md)  
**Read first:** [Stage lesson](../01-lessons/03-blazor-and-browser.md)

## User story

As a shopper opening an old product link, I want a clear route back to shopping so that a missing product is not a dead end.

## Starting point and scope

ItemPage already handles an HTTP 404 and displays a not-found message. Add a useful recovery action and verify existing behavior.

- [ItemPage.razor](../../src/WebApp/Components/Pages/Item/ItemPage.razor)
- [CatalogService.cs](../../src/WebAppComponents/Services/CatalogService.cs)
- [BrowseItemTest.spec.ts](../../e2e/BrowseItemTest.spec.ts)

## Acceptance criteria

- [ ] A positive missing product ID shows the not-found branch and returns the intended HTTP status on direct navigation.
- [ ] A browse link is reachable by keyboard and leads to the catalog.
- [ ] A real product still renders its name, description, and purchase action.
- [ ] A service failure is not incorrectly converted into product-not-found.

## Suggested approach

1. Confirm an unused positive ID in local data.
2. Improve the existing not-found branch rather than adding a second implementation.
3. Test direct navigation and recovery alongside a known product.

## Verification and evidence

Extend the anonymous browser suite. Record response status from a direct page navigation and the recovery action outcome.

## Hints, in order

1. A route constraint can reject malformed paths before item loading.
2. The current catch is restricted to HttpStatusCode.NotFound.

## Review conversation

Why test a positive missing ID separately from non-integer route input? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
