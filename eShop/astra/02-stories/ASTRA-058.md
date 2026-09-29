# ASTRA-058: Measure a catalog page with a repeatable workload

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 10 — Diagnosis and operations  
**Type:** Performance investigation · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-057](ASTRA-057.md), [ASTRA-021](ASTRA-021.md)  
**Read first:** [Stage lesson](../01-lessons/10-debugging-and-observability.md)

## User story

As a catalog maintainer, I want a repeatable latency measurement so that future query changes can be evaluated fairly.

## Starting point and scope

Measure a fixed filtered list request using controlled local data. The output is a baseline report; an optimization is optional and requires evidence.

- [CatalogApi.cs](../../src/Catalog.API/Apis/CatalogApi.cs)
- [CatalogItemEntityTypeConfiguration.cs](../../src/Catalog.API/Infrastructure/EntityConfigurations/CatalogItemEntityTypeConfiguration.cs)
- [Extensions.cs](../../src/eShop.ServiceDefaults/Extensions.cs)

## Acceptance criteria

- [ ] Record dataset size, filter, page size, warm-up, sample count, and environment.
- [ ] Report median and a tail or spread measure with the raw observations.
- [ ] Separate correctness assertions from timing observations.
- [ ] Any proposed query/index change includes before/after results under the same conditions.

## Suggested approach

1. Choose a request meaningful to a shopper.
2. Collect repeated timings and inspect query/trace evidence.
3. Explain the most plausible bottleneck and one uncertainty.

## Verification and evidence

Submit a reproducible local script or commands plus results. Avoid timing thresholds in ordinary unit tests and do not compare different datasets.

## Hints, in order

1. Container startup and JIT warm-up can dominate a first request.
2. A smaller response may explain a speedup without a better query.

## Review conversation

What would make this benchmark misleading on another developer's machine? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
