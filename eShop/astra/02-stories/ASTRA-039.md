# ASTRA-039: Make a new browser test discoverable

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 7 — Reliable test suites  
**Type:** Test infrastructure · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-038](ASTRA-038.md)  
**Read first:** [Stage lesson](../01-lessons/07-testing-strategy.md)

## User story

As a test contributor, I want my new browser scenario included in the intended project so that local and CI runs actually execute it.

## Starting point and scope

Playwright configuration uses explicit file match lists. Add a small new anonymous navigation spec and deliberately include it without triggering unnecessary login.

- [playwright.config.ts](../../playwright.config.ts)
- [BrowseItemTest.spec.ts](../../e2e/BrowseItemTest.spec.ts)
- [playwright.yml](../../.github/workflows/playwright.yml)

## Acceptance criteria

- [ ] A new proposed e2e/CatalogNavigation.spec.ts is listed in the anonymous project.
- [ ] The new scenario checks a real navigation or filter behavior.
- [ ] It does not run in the logged-in or setup project.
- [ ] The normal Playwright command still discovers existing tests.

## Suggested approach

1. Inspect current project testMatch definitions.
2. Create the small spec and update the matching project.
3. Use test --list before running the new scenario.

## Verification and evidence

Record npx.cmd playwright test --list and the anonymous-project run. Include project names in evidence so a merely existing file cannot be mistaken for coverage.

## Hints, in order

1. The default filename convention is overridden by project matching here.
2. A setup dependency belongs only where authentication is needed.

## Review conversation

How could a future test silently escape CI, and what would reveal it? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
