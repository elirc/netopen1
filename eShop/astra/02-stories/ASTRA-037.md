# ASTRA-037: Remove catalog tests' dependence on global counts

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 7 — Reliable test suites  
**Type:** Test reliability correction · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-036](ASTRA-036.md)  
**Read first:** [Stage lesson](../01-lessons/07-testing-strategy.md)

## User story

As a contributor running one test at a time, I want catalog assertions independent of other tests so that focused and full runs agree.

## Starting point and scope

CatalogApiTests expects 103 rows based on seeded rows plus additions elsewhere. Replace order-dependent assumptions with explicit test data ownership.

- [CatalogApiTests.cs](../../tests/Catalog.FunctionalTests/CatalogApiTests.cs)
- [CatalogApiFixture.cs](../../tests/Catalog.FunctionalTests/CatalogApiFixture.cs)

## Acceptance criteria

- [ ] The page-size test passes independently and with the full catalog suite.
- [ ] Its expected count does not assume another test has run.
- [ ] Create/update tests own their data or restore it reliably.
- [ ] The selected fixture isolation and concurrency behavior are documented.

## Suggested approach

1. Identify every shared seed mutation and count assumption.
2. Choose per-test data, an isolated fixture, or a controlled collection boundary.
3. Run focused and full scenarios to demonstrate independence.

## Verification and evidence

Record runner-supported focused commands and a full Catalog.FunctionalTests run. Prove the revised test still fails for an incorrect page size or count.

## Hints, in order

1. Reading a baseline count can still race with another writer.
2. Disabling parallelism alone does not remove execution-order dependencies.

## Review conversation

Who owns every row that can affect this assertion? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
