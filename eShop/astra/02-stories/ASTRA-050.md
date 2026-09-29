# ASTRA-050: Characterize duplicate command handling

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 9 — Events and consistency  
**Type:** Idempotency testing · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-049](ASTRA-049.md), [ASTRA-012](ASTRA-012.md)  
**Read first:** [Stage lesson](../01-lessons/09-events-and-consistency.md)

## User story

As a client retrying an order command, I want known duplicate behavior so that I can assess whether retrying causes another business effect.

## Starting point and scope

Test IdentifiedCommandHandler's existing sequential duplicate path and document failure/concurrency gaps. Do not claim exactly-once processing.

- [IdentifiedCommandHandler.cs](../../src/Ordering.API/Application/Commands/IdentifiedCommandHandler.cs)
- [RequestManager.cs](../../src/Ordering.Infrastructure/Idempotency/RequestManager.cs)
- [IdentifiedCommandHandlerTest.cs](../../tests/Ordering.UnitTests/Application/IdentifiedCommandHandlerTest.cs)

## Acceptance criteria

- [ ] A known duplicate returns the concrete handler's duplicate result without invoking the inner command.
- [ ] A new ID records a request and invokes the inner command.
- [ ] An inner failure's current returned result and marker timing are documented.
- [ ] Concurrent first requests are identified as a separate unproven case.

## Suggested approach

1. Read the concrete duplicate-result override used in existing tests.
2. Add distinctive return values and mediator interaction assertions.
3. Draw the check, marker save, command, and failure sequence.

## Verification and evidence

Run Ordering.UnitTests and include a sequence table. The unit test proves the selected branch logic; it does not prove database uniqueness under concurrency.

## Hints, in order

1. Two 200 responses do not tell you the number of order rows created.
2. The marker can outlive failed inner work depending on the transaction boundary.

## Review conversation

What must a robust retry contract say about an earlier failed attempt? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
