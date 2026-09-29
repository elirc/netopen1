# ASTRA-001: Record a reproducible workstation

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 1 — Onboard and contribute  
**Type:** Guided onboarding · **Estimate:** 1-2 hours  
**Prerequisites:** None  
**Read first:** [Stage lesson](../00-onboarding/04-first-contribution.md)

## User story

As a new contributor, I want a versioned setup record so that I can distinguish environment problems from code problems.

## Starting point and scope

Inspect the existing checkout before changing it. The README's .NET version and global.json disagree; record the actual selected SDK rather than editing either file during this story.

- [global.json](../../global.json)
- [Directory.Build.props](../../Directory.Build.props)
- [eShop.Web.slnf](../../eShop.Web.slnf)
- [README.md](../../README.md)

## Acceptance criteria

- [ ] Record the Git root, branch, baseline commit, and pre-existing changes.
- [ ] Record SDK selection, Docker client/server outcomes, and editor choice.
- [ ] Run the web restore/build and the two existing web unit-test projects, recording actual outcomes.
- [ ] Explain why the web filter is the starting point and list any unresolved blocker.

## Suggested approach

1. Follow the environment guide and save a private onboarding log.
2. Compare the selected SDK with global.json and the AppHost project.
3. Classify each failure as tool discovery, restore, compile, test, or runtime.

## Verification and evidence

Submit the onboarding log with exact working directory and commands. A setup blocker can complete the diagnosis portion, but keep dependent runtime stories pending until the blocker is resolved.

## Hints, in order

1. A runtime installation does not include the SDK compiler.
2. Docker's client version does not prove its server is reachable.

## Review conversation

Which single observation would convince another developer that your SDK selection is reproducible? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
