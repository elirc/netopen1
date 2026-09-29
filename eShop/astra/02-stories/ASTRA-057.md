# ASTRA-057: Propagate cancellation through a background database read

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 10 — Diagnosis and operations  
**Type:** Async reliability feature · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-056](ASTRA-056.md), [ASTRA-012](ASTRA-012.md)  
**Read first:** [Stage lesson](../01-lessons/10-debugging-and-observability.md)

## User story

As an operator stopping the order processor, I want pending database work to observe shutdown so that the service can stop promptly.

## Starting point and scope

GracePeriodManagerService passes the stopping token to its delay but its database helper calls currently omit it. Thread cancellation through this chosen read path.

- [GracePeriodManagerService.cs](../../src/OrderProcessor/Services/GracePeriodManagerService.cs)
- [Program.cs](../../src/OrderProcessor/Program.cs)

## Acceptance criteria

- [ ] The stopping token reaches connection open, reader execution, and row reading where supported.
- [ ] Cancellation does not become a successful empty-result interpretation or a misleading fatal database error.
- [ ] Normal eligible-order selection remains unchanged.
- [ ] Shutdown completion is tested without arbitrary long sleeps.

## Suggested approach

1. Trace the token from ExecuteAsync into the private helpers.
2. Change the narrow signatures and awaited database calls.
3. Use a new focused processor harness or controlled integration setup to cancel in flight.

## Verification and evidence

Record the newly introduced harness and direct test command if needed. Provide deterministic cancellation evidence and a normal-query regression.

## Hints, in order

1. A token on Task.Delay cannot cancel an earlier database read.
2. Do not pretend IEventBus supports cancellation if its current contract does not.

## Review conversation

What work can still continue after this narrowly scoped cancellation change? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
