# ASTRA-068: Implement the version 2 in-stock API filter

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 12 — Capstone: available products  
**Type:** Capstone API slice · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-067](ASTRA-067.md), [ASTRA-020](ASTRA-020.md), [ASTRA-021](ASTRA-021.md), [ASTRA-022](ASTRA-022.md)  
**Read first:** [Stage lesson](../01-lessons/12-capstone.md)

## User story

As a catalog API consumer, I want inStockOnly=true to return available products so that clients can offer focused browsing.

## Starting point and scope

Add the optional V2 list filter, applying AvailableStock > 0 before counting and pagination. Retain the baseline behavior when false or absent and preserve V1 semantics.

- [CatalogApi.cs](../../src/Catalog.API/Apis/CatalogApi.cs)
- [CatalogItem.cs](../../src/Catalog.API/Model/CatalogItem.cs)
- [CatalogApiTests.cs](../../tests/Catalog.FunctionalTests/CatalogApiTests.cs)

## Acceptance criteria

- [ ] True excludes zero-stock rows; false/absent preserves ordinary results.
- [ ] The filter composes with brand, type, and current name matching.
- [ ] Count and page membership reflect all applied filters with stable ordering.
- [ ] Invalid boolean input has the documented client error and V1 behavior remains covered.

## Suggested approach

1. Seed controlled rows with stock 0, 1, and a larger positive value.
2. Add functional acceptance tests before changing the query.
3. Update the V2 handler, wrappers as required, and metadata without changing unrelated routes.

## Verification and evidence

Run Catalog.FunctionalTests and build the web filter. Include IDs, counts, and status assertions for all capstone API cases.

## Hints, in order

1. Filtering after Take gives incorrect counts and sparse pages.
2. A shared implementation method can accidentally alter V1 if defaults are not deliberate.

## Review conversation

Which test catches applying the filter after pagination? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
