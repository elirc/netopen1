# ASTRA-064: Make the contribution's checks discoverable in CI

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 11 — Design and delivery  
**Type:** Delivery tooling · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-063](ASTRA-063.md), [ASTRA-039](ASTRA-039.md)  
**Read first:** [Stage lesson](../01-lessons/11-design-and-delivery.md)

## User story

As a reviewer, I want each added test included in the right checks so that local confidence carries into the shared workflow.

## Starting point and scope

Audit course-added test projects and browser files. Correct one demonstrated discovery gap or produce verified evidence that all relevant additions are already included.

- [eShop.slnx](../../eShop.slnx)
- [eShop.Web.slnf](../../eShop.Web.slnf)
- [pr-validation.yml](../../.github/workflows/pr-validation.yml)
- [playwright.yml](../../.github/workflows/playwright.yml)
- [playwright.config.ts](../../playwright.config.ts)

## Acceptance criteria

- [ ] Every added web test project belongs to the intended solution/filter or has an explicit separate command.
- [ ] New browser specs match the correct Playwright project.
- [ ] The relevant local commands discover and run the expected tests.
- [ ] Documentation-only and code-change workflow triggers are explained accurately.

## Suggested approach

1. Compare the story branch's new test files with solution and workflow configuration.
2. Fix only the proven discovery gap.
3. Record commands and counts before/after the correction.

## Verification and evidence

Run the appropriate solution test command after rebuilding and list browser tests. Do not claim an actual remote CI run unless one was performed.

## Hints, in order

1. CI reads paths and project lists, not your story tracker.
2. A docs-only PR may skip the web workflows while Markdown lint still runs.

## Review conversation

What would make a new test pass locally but never run in the shared check? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
