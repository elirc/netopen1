# ASTRA-069: Connect the shared client and catalog toggle

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 12 — Capstone: available products  
**Type:** Capstone UI slice · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-068](ASTRA-068.md), [ASTRA-013](ASTRA-013.md), [ASTRA-017](ASTRA-017.md), [ASTRA-063](ASTRA-063.md)  
**Read first:** [Stage lesson](../01-lessons/12-capstone.md)

## User story

As a shopper, I want a visible in-stock toggle reflected in my URL so that the choice survives navigation and sharing.

## Starting point and scope

Pass the optional filter through the existing catalog client and query-driven page. Inspect shared implementers and preserve brand/type behavior.

- [CatalogService.cs](../../src/WebAppComponents/Services/CatalogService.cs)
- [ICatalogService.cs](../../src/WebAppComponents/Services/ICatalogService.cs)
- [CatalogSearch.razor](../../src/WebAppComponents/Catalog/CatalogSearch.razor)
- [Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor)
- [CatalogService.cs](../../src/HybridApp/Services/CatalogService.cs)

## Acceptance criteria

- [ ] The accessible toggle sends the chosen value through the shared client to V2.
- [ ] Refresh and pagination retain the stock, brand, and type selections.
- [ ] Changing any filter resets page while preserving other active selections.
- [ ] The filtered empty state has a useful recovery action and the off state preserves existing browsing.

## Suggested approach

1. Update the narrow client query seam and enumerate affected callers.
2. Implement the toggle using the page's actual server-rendered navigation style.
3. Verify the final URI and result set after each change.

## Verification and evidence

Run client-seam tests, the web build, and manual browser checks. Record any unexecuted platform build; inspect implementer signatures even when platform tools are unavailable.

## Hints, in order

1. Do not introduce client-only state when the requirement is URL persistence.
2. BrandUri and TypeUri must retain the new filter as they clear page.

## Review conversation

What happens when a shopper copies the URL into a new browser session? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
