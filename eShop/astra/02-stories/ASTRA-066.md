# ASTRA-066: Lead a focused feature review

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 11 — Design and delivery  
**Type:** Independent contribution gate · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-065](ASTRA-065.md)  
**Read first:** [Stage lesson](../01-lessons/11-design-and-delivery.md)

## User story

As a junior ready for a larger feature, I want to lead a review so that I can explain decisions and respond to technical questions independently.

## Starting point and scope

Review one completed feature branch from the course with its implementation, tests, and operational evidence.

- [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [pr-validation.yml](../../.github/workflows/pr-validation.yml)

## Acceptance criteria

- [ ] Present the problem, resulting behavior, and important tradeoff in five minutes.
- [ ] Walk through one production method and its regression test.
- [ ] Answer a boundary or failure question using source evidence.
- [ ] Address one review concern in a focused follow-up or document a reasoned decision to retain the design.

## Suggested approach

1. Prepare a small review packet using the PR and review templates.
2. Ask a mentor to choose an unprepared edge case, or select one after a delayed self-review.
3. Update the implementation or explanation and rerun affected checks.

## Verification and evidence

Submit the review notes, final diff, command outcomes, and a self-assessment against the stage-11 gate. Do not claim independent mastery if you cannot explain your own changes.

## Hints, in order

1. Reading the entire diff aloud hides the important decisions.
2. A useful answer can identify an honest limit and propose a concrete verification.

## Review conversation

Which skill is now independent, and which still benefits from pairing? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
