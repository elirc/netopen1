# ASTRA-063: Refactor one shared-client seam without changing behavior

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 11 — Design and delivery  
**Type:** Maintainability refactor · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-062](ASTRA-062.md)  
**Read first:** [Stage lesson](../01-lessons/11-design-and-delivery.md)

## User story

As a developer adding a catalog filter, I want a clear client query-building seam so that the change can be tested without obscuring existing URLs.

## Starting point and scope

Refactor a small part of CatalogService's URI construction or request boundary. Preserve the current contract and inspect all shared interface implementers.

- [CatalogService.cs](../../src/WebAppComponents/Services/CatalogService.cs)
- [ICatalogService.cs](../../src/WebAppComponents/Services/ICatalogService.cs)
- [CatalogService.cs](../../src/HybridApp/Services/CatalogService.cs)

## Acceptance criteria

- [ ] Existing page, brand, and type requests preserve their meaning.
- [ ] The extracted seam has one clear responsibility and no unnecessary framework abstraction.
- [ ] Tests cover omission and inclusion of optional filters with correct encoding where applicable.
- [ ] Affected callers and implementers are identified, with platform-build limitations stated.

## Suggested approach

1. Capture representative current request URIs using a fake HTTP handler or pure builder test.
2. Extract only the repeated or hard-to-observe behavior.
3. Run the relevant web and shared-client tests.

## Verification and evidence

Provide behavior-preserving tests and the web build outcome. A new test project must follow MTP and solution-discovery conventions; document any unexecuted mobile checks.

## Hints, in order

1. A default interface parameter does not automatically update implementer signatures.
2. Query parameter ordering rarely belongs in a semantic assertion.

## Review conversation

What concrete future change is easier after this refactor? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
