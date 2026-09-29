# ASTRA-041: Test authentication boundaries honestly

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 7 — Reliable test suites  
**Type:** Fixture audit · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-040](ASTRA-040.md)  
**Read first:** [Stage lesson](../01-lessons/07-testing-strategy.md)

## User story

As a reviewer, I want tests to declare when they bypass authentication so that I can assess what their green results prove.

## Starting point and scope

Audit OrderingApiFixture and AutoAuthorizeMiddleware, then add controlled-user support for ownership tests. Do not place test identity middleware in production.

- [AutoAuthorizeMiddleware.cs](../../tests/Ordering.FunctionalTests/AutoAuthorizeMiddleware.cs)
- [OrderingApiFixture.cs](../../tests/Ordering.FunctionalTests/OrderingApiFixture.cs)
- [Program.cs](../../src/Ordering.API/Program.cs)

## Acceptance criteria

- [ ] Document where and how the fixture supplies identity.
- [ ] Provide a test-only mechanism for selecting two distinct principals and an anonymous case where the host setup allows it.
- [ ] Demonstrate that the chosen principal reaches the API identity service.
- [ ] Keep a separate real browser login check for the configured authentication flow.

## Suggested approach

1. Trace fixture host configuration and middleware order.
2. Add explicit per-test identity selection with no cross-test mutable global user.
3. Write one identity-observation test before using the helper for ownership.

## Verification and evidence

Run Ordering.FunctionalTests and record which paths bypass token validation. Prove the helper cannot affect normal production startup.

## Hints, in order

1. A fake principal is appropriate for authorization tests if its limits are explicit.
2. An anonymous fixture case is meaningless if middleware always injects a user.

## Review conversation

Which claim can this fixture establish, and which needs a real sign-in flow? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
