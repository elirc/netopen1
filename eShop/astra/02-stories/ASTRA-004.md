# ASTRA-004: Trace a catalog request with real values

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 1 — Onboard and contribute  
**Type:** Guided debugging · **Estimate:** 1-2 hours  
**Prerequisites:** [ASTRA-003](ASTRA-003.md)  
**Read first:** [Stage lesson](../00-onboarding/04-first-contribution.md)

## User story

As a developer diagnosing catalog behavior, I want a request trace so that I can explain how URL filters become database results.

## Starting point and scope

Trace the existing browse flow without changing its behavior. Include the UI's one-based page and API's zero-based page index.

- [Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor)
- [CatalogService.cs](../../src/WebAppComponents/Services/CatalogService.cs)
- [Extensions.cs](../../src/WebApp/Extensions/Extensions.cs)
- [CatalogApi.cs](../../src/Catalog.API/Apis/CatalogApi.cs)

## Acceptance criteria

- [ ] Capture the browser URL, requested API version, page size, page index, and active filters.
- [ ] Identify where the query is built and where it executes.
- [ ] Explain the difference between total count and returned rows.
- [ ] Record a breakpoint observation or downstream trace alongside the source path.

## Suggested approach

1. Predict the values for the second page before navigating.
2. Inspect the relevant process using the debugger or dashboard.
3. Replay one equivalent API request with the local endpoint.

## Verification and evidence

Submit a completed trace table with a populated request and an empty-page request. Explain each result using observed parameters.

## Hints, in order

1. Catalog.razor sets PageSize to 9.
2. Server-side HTTP calls need not appear as browser fetches.

## Review conversation

At which point would an incorrect page offset first become visible? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
