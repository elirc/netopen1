# ASTRA-005: Make a small onboarding documentation contribution

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 1 — Onboard and contribute  
**Type:** First contribution · **Estimate:** 1-2 hours  
**Prerequisites:** [ASTRA-004](ASTRA-004.md)  
**Read first:** [Stage lesson](../00-onboarding/04-first-contribution.md)

## User story

As the next new contributor, I want one confusing setup instruction clarified so that I can get started without guessing.

## Starting point and scope

Choose one verified documentation gap, such as the SDK mismatch or working-directory ambiguity. Write a short course workbook note or a narrowly scoped practice correction to the main README.

- [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [README.md](../../README.md)
- [global.json](../../global.json)

## Acceptance criteria

- [ ] State the exact confusion and the source that resolves it.
- [ ] Create a named practice branch and limit the diff to the chosen correction.
- [ ] Provide commands with an explicit working directory and honest validation status.
- [ ] Prepare a draft PR description using the course template.

## Suggested approach

1. Reproduce the confusing step or compare contradictory sources.
2. Write the smallest useful correction and preview the Markdown.
3. Inspect staged files before committing; preserve unrelated work.

## Verification and evidence

Run git diff --check and lint the changed Markdown with the repository configuration. Include the actual command outcomes and the draft PR text. No code test is needed.

## Hints, in order

1. A local draft PR document is enough if you have no fork.
2. Avoid replacing an old hard-coded version claim with an unexplained new one.

## Review conversation

Could a reviewer understand the change without this conversation? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
