# ASTRA-021: Make catalog pagination stable for tied names

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 4 — HTTP and API contracts  
**Type:** Query correction · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-020](ASTRA-020.md)  
**Read first:** [Stage lesson](../01-lessons/04-http-and-contracts.md)

## User story

As a shopper paging through similarly named products, I want deterministic ordering so that equal names do not make page membership ambiguous.

## Starting point and scope

Add a stable tie-breaker to the ordinary catalog list query. Do not claim snapshot consistency during concurrent inserts.

- [CatalogApi.cs](../../src/Catalog.API/Apis/CatalogApi.cs)
- [CatalogApiTests.cs](../../tests/Catalog.FunctionalTests/CatalogApiTests.cs)

## Acceptance criteria

- [ ] Two products with the same name have a documented secondary order.
- [ ] Adjacent pages over a fixed dataset do not repeat or omit those tied products.
- [ ] Total count and active filters retain their meaning.
- [ ] Tests use controlled tied-name rows and do not depend on seed insertion order.

## Suggested approach

1. Inspect OrderBy before Skip and Take.
2. Add a stable unique secondary key.
3. Write database-backed assertions over adjacent small pages.

## Verification and evidence

Run Catalog.FunctionalTests on a fixed dataset and include the ordered IDs from both pages. State the limitation under concurrent writes.

## Hints, in order

1. ThenBy must be applied before pagination.
2. Repeatability on one local run does not prove the database guarantees a tie order.

## Review conversation

What problem remains even after deterministic ordering is added? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
