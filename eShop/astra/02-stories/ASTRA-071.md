# ASTRA-071: Evaluate capstone performance and failure behavior

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 12 — Capstone: available products  
**Type:** Capstone operational slice · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-070](ASTRA-070.md), [ASTRA-058](ASTRA-058.md), [ASTRA-060](ASTRA-060.md)  
**Read first:** [Stage lesson](../01-lessons/12-capstone.md)

## User story

As a maintainer releasing the filter, I want measured behavior and failure evidence so that I know its cost and limitations.

## Starting point and scope

Compare filtered and unfiltered queries on the same controlled dataset and observe a local catalog failure. Keep inventory consistency claims advisory.

- [CatalogApi.cs](../../src/Catalog.API/Apis/CatalogApi.cs)
- [Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor)
- [Extensions.cs](../../src/eShop.ServiceDefaults/Extensions.cs)

## Acceptance criteria

- [ ] Record repeatable timing samples and result correctness for on/off cases.
- [ ] Show the query remains database-filtered and paginated rather than loading every row.
- [ ] Document the actual UI behavior when Catalog is unavailable and any unresolved recovery limitation.
- [ ] Explain the stock-change race between browsing and checkout.

## Suggested approach

1. Reuse the measurement procedure from ASTRA-058.
2. Inspect a trace and query shape for the new filter.
3. Run one reversible local failure experiment and restore the dependency.

## Verification and evidence

Submit a concise performance/failure report with raw sample references and a recovery check. Do not claim an optimization without comparable evidence.

## Hints, in order

1. Filtering can change the result count, which affects timing interpretation.
2. A friendly empty state must not conceal a failed dependency.

## Review conversation

What is the most important limitation a maintainer should know before accepting the feature? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
