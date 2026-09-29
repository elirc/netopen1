# ASTRA-042: Publish a risk-based test plan for a feature

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 7 — Reliable test suites  
**Type:** Quality planning · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-041](ASTRA-041.md)  
**Read first:** [Stage lesson](../01-lessons/07-testing-strategy.md)

## User story

As a reviewer of a cross-layer change, I want a test plan tied to failure risks so that gaps are visible before implementation.

## Starting point and scope

Use the completed basket recovery work or the future availability filter. Produce a plan and implement one missing high-value regression.

- [README.md](../../tests/README.md)
- [eShop.Web.slnf](../../eShop.Web.slnf)
- [playwright.config.ts](../../playwright.config.ts)

## Acceptance criteria

- [ ] Map at least six acceptance or failure cases to unit, functional, browser, or manual evidence.
- [ ] Explain why the chosen layer can prove each case.
- [ ] Identify one current gap and add a meaningful discovered regression test.
- [ ] Record pending infrastructure checks without describing them as passed.

## Suggested approach

1. Start with user-visible failures, not a target coverage percentage.
2. Map dependencies that must be real and ones that can be substituted.
3. Review and execute the selected missing test.

## Verification and evidence

Submit the matrix plus exact commands and outcomes for the new regression. Pass the stage-7 gate by explaining the limitations of every test layer.

## Hints, in order

1. Many unit tests cannot replace a missing routing test.
2. A percentage alone does not tell you whether ownership is covered.

## Review conversation

Which single untested failure would worry you most before sharing this feature? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
