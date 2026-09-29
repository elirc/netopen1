# ASTRA-020: Reject invalid catalog pagination before querying

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 4 — HTTP and API contracts  
**Type:** API validation feature · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-019](ASTRA-019.md)  
**Read first:** [Stage lesson](../01-lessons/04-http-and-contracts.md)

## User story

As an API consumer, I want invalid pagination rejected clearly so that mistakes do not produce database errors or excessive reads.

## Starting point and scope

Proposed policy for the V1/V2 list routes: pageIndex >= 0, pageSize 1-100, and a safe offset. Inspect wrappers and shared pagination use before changing signatures.

- [PaginationRequest.cs](../../src/Catalog.API/Model/PaginationRequest.cs)
- [CatalogApi.cs](../../src/Catalog.API/Apis/CatalogApi.cs)
- [CatalogApiTests.cs](../../tests/Catalog.FunctionalTests/CatalogApiTests.cs)

## Acceptance criteria

- [ ] Both list versions reject negative indexes and page sizes 0 or above 100 with a documented 400 body.
- [ ] Huge indexes cannot overflow page-size multiplication.
- [ ] Defaults and valid boundary values still succeed; valid empty pages remain 200.
- [ ] Typed result signatures, wrappers, and API metadata agree with the new response.

## Suggested approach

1. Write the invalid-input tests before changing the handlers.
2. Choose one reusable validation approach and state which related routes it covers.
3. Keep filtering and query execution after validation.

## Verification and evidence

Run Catalog.FunctionalTests with Docker and the web build. Include both API versions and malformed numeric binding cases in the evidence matrix.

## Hints, in order

1. Computing the overflowed offset before checking it is too late.
2. A shared PaginationRequest also appears outside the main list route.

## Review conversation

Why did you choose a 400 response instead of silently shrinking an excessive page size? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
