# ASTRA-070: Prove the capstone in the browser and across versions

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 12 — Capstone: available products  
**Type:** Capstone test slice · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-069](ASTRA-069.md), [ASTRA-039](ASTRA-039.md), [ASTRA-040](ASTRA-040.md), [ASTRA-042](ASTRA-042.md)  
**Read first:** [Stage lesson](../01-lessons/12-capstone.md)

## User story

As a reviewer, I want discovered acceptance tests so that the availability feature remains reliable after later changes.

## Starting point and scope

Join API tests and browser scenarios with isolated data. Keep anonymous catalog checks independent of saved login state.

- [CatalogApiTests.cs](../../tests/Catalog.FunctionalTests/CatalogApiTests.cs)
- [playwright.config.ts](../../playwright.config.ts)
- [BrowseItemTest.spec.ts](../../e2e/BrowseItemTest.spec.ts)

## Acceptance criteria

- [ ] Browser tests cover toggle on/off, combined filters, pagination, refresh, empty results, and recovery.
- [ ] The selected test file is listed in the intended anonymous project.
- [ ] API coverage preserves V1 and verifies V2's new behavior.
- [ ] Tests own their data and do not rely on stock mutations from earlier exercises.

## Suggested approach

1. Use the stage-7 risk matrix to select the correct test layer.
2. Create only necessary new specs and register them explicitly.
3. Run focused suites, then relevant full checks after a matching build.

## Verification and evidence

Submit test discovery output, actual test counts, command outcomes, and one keyboard check. Every acceptance row must link to evidence, not merely a test filename.

## Hints, in order

1. A full browser run can pass while the new file is not matched.
2. A seed product's current stock may have changed during prior practice.

## Review conversation

Which acceptance criterion still needs manual evidence and why? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
