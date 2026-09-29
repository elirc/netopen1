# ASTRA-017: Lock in filter reset behavior

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 3 — Blazor and accessible UI  
**Type:** Browser characterization · **Estimate:** 2-4 hours  
**Prerequisites:** [ASTRA-016](ASTRA-016.md)  
**Read first:** [Stage lesson](../01-lessons/03-blazor-and-browser.md)

## User story

As a shopper narrowing results, I want a filter change to start at the first page so that I do not land beyond the matching products.

## Starting point and scope

CatalogSearch already clears page when brand or type changes. Add regression coverage for the current URL behavior instead of reimplementing it.

- [CatalogSearch.razor](../../src/WebAppComponents/Catalog/CatalogSearch.razor)
- [Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor)
- [BrowseItemTest.spec.ts](../../e2e/BrowseItemTest.spec.ts)

## Acceptance criteria

- [ ] Changing brand from a later page clears the page query and preserves type.
- [ ] Changing type clears page and preserves brand.
- [ ] Selecting All clears only the selected filter plus page.
- [ ] Displayed results correspond to the final URL after navigation and refresh.

## Suggested approach

1. Read BrandUri and TypeUri and predict the resulting queries.
2. Choose dataset values with enough products for pagination.
3. Extend browser coverage with explicit URL and result assertions.

## Verification and evidence

Run the anonymous suite and report the selected brand/type data. Avoid assertions tied to an unrelated global product count.

## Hints, in order

1. Use URL parsing when parameter ordering is irrelevant.
2. Refresh distinguishes URL-backed state from a transient visual selection.

## Review conversation

Which regression would a screenshot-only check miss? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
