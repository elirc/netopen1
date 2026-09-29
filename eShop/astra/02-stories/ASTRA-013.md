# ASTRA-013: Give an empty catalog a recovery action

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 3 — Blazor and accessible UI  
**Type:** First UI feature · **Estimate:** 2-4 hours  
**Prerequisites:** [ASTRA-006](ASTRA-006.md), [ASTRA-012](ASTRA-012.md)  
**Read first:** [Stage lesson](../01-lessons/03-blazor-and-browser.md)

## User story

As a shopper whose filters match no products, I want a helpful empty state so that I can continue browsing.

## Starting point and scope

The catalog has loading and populated branches. Add a successful-empty branch without treating request failures as empty results.

- [Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor)
- [BrowseItemTest.spec.ts](../../e2e/BrowseItemTest.spec.ts)

## Acceptance criteria

- [ ] A successful zero-result query shows a clear message and a working reset or browse link.
- [ ] Loading remains distinguishable from an empty result.
- [ ] A populated query still shows product cards and valid pagination.
- [ ] The recovery action returns to a useful catalog view.

## Suggested approach

1. Find a reproducible empty brand/type combination or controlled test data.
2. Add the smallest markup branch and recovery link.
3. Extend the existing anonymous browse test and perform a keyboard pass.

## Verification and evidence

Run the anonymous Playwright project from the commands guide. Include empty, populated, and recovery evidence; record the test data used.

## Hints, in order

1. Check catalogResult before reading its Data.
2. Resetting filters and retrying a failed service are different actions.

## Review conversation

What would a user see if the API were unavailable instead of empty? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
