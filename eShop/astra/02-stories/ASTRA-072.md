# ASTRA-072: Deliver and teach the completed capstone

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 12 — Capstone: available products  
**Type:** Final assessment · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-071](ASTRA-071.md), [ASTRA-065](ASTRA-065.md), [ASTRA-066](ASTRA-066.md)  
**Read first:** [Stage lesson](../01-lessons/12-capstone.md)

## User story

As the next maintainer, I want a complete handoff so that I can understand, verify, and extend the availability feature.

## Starting point and scope

Finish the capstone as a coherent practice PR package with implementation, tests, design notes, and a local runbook. Publication to upstream is optional.

- [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [eShop.Web.slnf](../../eShop.Web.slnf)
- [playwright.config.ts](../../playwright.config.ts)

## Acceptance criteria

- [ ] All six capstone slices and their acceptance evidence are complete.
- [ ] The final PR title and description explain the resulting feature without conversational history.
- [ ] The demo covers a normal journey, an empty result, compatibility, and one failure limitation.
- [ ] The local release procedure, rollback approach, and next three learning goals are recorded.

## Suggested approach

1. Review the complete diff for scope, naming, generated files, and missing evidence.
2. Perform the capstone demonstration from the lesson.
3. Apply the rubric and resolve review findings with focused changes and checks.

## Verification and evidence

Submit the PR package, demo notes, test results, and scored rubric. Graduation requires no unresolved critical behavior or evidence gap; blocked checks remain visible until completed.

## Hints, in order

1. Rewrite the PR description around the final implementation, not abandoned approaches.
2. Explain your code without relying on generated text or a mentor to supply the reasoning.

## Review conversation

What can you now own independently, and what would you investigate next? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
