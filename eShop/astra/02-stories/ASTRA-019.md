# ASTRA-019: Document the catalog HTTP response contract

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 4 — HTTP and API contracts  
**Type:** API investigation · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-018](ASTRA-018.md)  
**Read first:** [Stage lesson](../01-lessons/04-http-and-contracts.md)

## User story

As an API consumer, I want a concrete response matrix so that I can distinguish bad input, absent data, and successful results.

## Starting point and scope

Observe existing version 1 and 2 behavior. Do not change handlers in this story.

- [CatalogApi.cs](../../src/Catalog.API/Apis/CatalogApi.cs)
- [PaginationRequest.cs](../../src/Catalog.API/Model/PaginationRequest.cs)
- [CatalogApiTests.cs](../../tests/Catalog.FunctionalTests/CatalogApiTests.cs)

## Acceptance criteria

- [ ] Document method, path, version, status, and body shape for list and single-item requests.
- [ ] Exercise valid, zero, negative, missing, and malformed identifiers.
- [ ] Record default pagination and a valid empty page.
- [ ] Separate route/binding outcomes from handler decisions and label proposed improvements.

## Suggested approach

1. Follow the functional test's API-version client setup.
2. Send local requests and compare responses with typed result signatures.
3. Write a short contract table using sanitized request examples.

## Verification and evidence

Provide actual status/body observations with local commands and source references. If an input fails before the handler, identify that boundary.

## Hints, in order

1. A response metadata attribute does not enforce validation.
2. Versioned PUT routes differ even when the data model is shared.

## Review conversation

Which response in your table surprised you, and what explains it? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
