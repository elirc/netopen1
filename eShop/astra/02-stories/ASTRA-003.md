# ASTRA-003: Create a one-page codebase map

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 1 — Onboard and contribute  
**Type:** Code reading · **Estimate:** 1-2 hours  
**Prerequisites:** [ASTRA-002](ASTRA-002.md)  
**Read first:** [Stage lesson](../00-onboarding/04-first-contribution.md)

## User story

As a junior joining the team, I want a responsibility map so that I can locate the right project before making a change.

## Starting point and scope

Map the web learning path, then label mobile and webhook components as supporting paths. Use the codebase-map lesson as a starting point, not a diagram to copy without checking.

- [Program.cs](../../src/eShop.AppHost/Program.cs)
- [Program.cs](../../src/WebApp/Program.cs)
- [Program.cs](../../src/Catalog.API/Program.cs)
- [Program.cs](../../src/Ordering.API/Program.cs)

## Acceptance criteria

- [ ] Map at least eight projects or resources to a concrete responsibility.
- [ ] Distinguish HTTP, gRPC, direct calls, and event messages.
- [ ] Identify who owns catalog data, basket quantities, and order state.
- [ ] Link each important statement to an existing source file.

## Suggested approach

1. Read the AppHost registrations and follow three project entry points.
2. Draw your own map and mark anything you have inferred.
3. Use symbol search to resolve one question the diagram cannot answer.

## Verification and evidence

Submit a Markdown map plus a three-minute explanation. Verify every local link. Runtime evidence is not required for every arrow if source evidence is labeled.

## Hints, in order

1. A project reference is not necessarily a runtime request.
2. WebAppComponents is shared code; AppHost is orchestration.

## Review conversation

Where would you begin to change product pagination, and what would make you inspect a second project? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
