# ASTRA-040: Isolate logged-in basket browser scenarios

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 7 — Reliable test suites  
**Type:** Browser reliability · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-039](ASTRA-039.md)  
**Read first:** [Stage lesson](../01-lessons/07-testing-strategy.md)

## User story

As a developer running browser tests in parallel, I want controlled basket state so that one test's updates do not break another.

## Starting point and scope

Logged-in tests share saved authentication state and can mutate the same basket. Improve data or identity isolation; document any intentionally scoped serialization.

- [playwright.config.ts](../../playwright.config.ts)
- [login.setup.ts](../../e2e/login.setup.ts)
- [AddItemTest.spec.ts](../../e2e/AddItemTest.spec.ts)
- [RemoveItemTest.spec.ts](../../e2e/RemoveItemTest.spec.ts)

## Acceptance criteria

- [ ] Each basket scenario has a known starting state and reliable cleanup.
- [ ] Tests do not depend on add-before-remove execution order.
- [ ] Repeated runs with the chosen worker configuration produce consistent results.
- [ ] The solution explains whether identities, data ownership, or a scoped serial group provides isolation.

## Suggested approach

1. Reproduce the shared-state risk using the current tests.
2. Choose the smallest practical isolation strategy for the local sample identity setup.
3. Remove fixed sleeps and wait for observable state.

## Verification and evidence

Run the affected project repeatedly with the documented workers. Report test count and any limitation if shared identity forces serialization.

## Hints, in order

1. A fresh browser context can still use the same server-side basket.
2. Cleanup after a passing test alone does not handle failures.

## Review conversation

What state remains shared even with separate browser tabs? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
