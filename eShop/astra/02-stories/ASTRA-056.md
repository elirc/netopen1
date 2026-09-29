# ASTRA-056: Compare liveness and readiness during an outage

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 10 — Diagnosis and operations  
**Type:** Operational experiment · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-055](ASTRA-055.md)  
**Read first:** [Stage lesson](../01-lessons/10-debugging-and-observability.md)

## User story

As a developer operating the app, I want to understand health responses so that I do not confuse a live process with a usable dependency path.

## Starting point and scope

Inspect development-only /alive and /health mappings and actual registered checks. Test one local dependency failure with reversible resource control.

- [Extensions.cs](../../src/eShop.ServiceDefaults/Extensions.cs)
- [Program.cs](../../src/eShop.AppHost/Program.cs)
- [Extensions.cs](../../src/Catalog.API/Extensions/Extensions.cs)

## Acceptance criteria

- [ ] Record baseline /alive and /health responses for the selected service.
- [ ] Identify which dependency checks are actually registered.
- [ ] During a controlled outage, compare health responses and a real user request.
- [ ] Restore the resource and verify a fresh successful request.

## Suggested approach

1. Choose a local service/resource pair and document the expected observation.
2. Stop only that resource or use an isolated failure harness.
3. Record actual results and revise any incorrect expectation.

## Verification and evidence

Provide a before/during/after table and the exact resource restored. If a probe remains green while the operation fails, describe that coverage gap accurately.

## Hints, in order

1. MapDefaultEndpoints maps these routes only in Development.
2. The default self check alone does not test PostgreSQL.

## Review conversation

Which probe would you use for process responsiveness, and what additional evidence proves readiness? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
