# ASTRA-022: Prove version 2 filters compose correctly

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 4 — HTTP and API contracts  
**Type:** Contract tests · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-021](ASTRA-021.md)  
**Read first:** [Stage lesson](../01-lessons/04-http-and-contracts.md)

## User story

As an API consumer, I want combined name, brand, and type filters to apply together so that a query returns precisely the intended products.

## Starting point and scope

Characterize the current V2 StartsWith name behavior and combined predicates. Preserve V1 compatibility and existing pagination bounds.

- [CatalogApi.cs](../../src/Catalog.API/Apis/CatalogApi.cs)
- [CatalogApiTests.cs](../../tests/Catalog.FunctionalTests/CatalogApiTests.cs)

## Acceptance criteria

- [ ] Controlled rows distinguish name-only, brand-only, type-only, and combined filters.
- [ ] Count reflects all matches before pagination.
- [ ] A no-match combination returns an empty successful page.
- [ ] Name matching tests describe current provider behavior, including observed case handling, without assuming case insensitivity.

## Suggested approach

1. Create a tiny dataset whose rows each challenge one predicate.
2. Use the V2 client and inspect both Count and Data IDs.
3. Include one V1 regression case for unchanged list behavior.

## Verification and evidence

Run Catalog.FunctionalTests and show why an implementation that ORs the filters would fail. Keep cleanup or fixture isolation explicit.

## Hints, in order

1. The existing name condition uses StartsWith.
2. A count assertion alone cannot identify wrong returned products.

## Review conversation

Which test input makes each filter necessary to the final result? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
