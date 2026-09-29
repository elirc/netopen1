# ASTRA-012: Trace async completion and cancellation

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 2 — C# and focused tests  
**Type:** Async characterization · **Estimate:** 1-3 hours  
**Prerequisites:** [ASTRA-011](ASTRA-011.md)  
**Read first:** [Stage lesson](../01-lessons/02-csharp-and-testing-basics.md)

## User story

As a developer maintaining commands, I want to understand task completion and cancellation so that I do not mistake failure for successful work.

## Starting point and scope

Inspect IdentifiedCommandHandler and add a characterization of token forwarding on its successful path. Record the broad-catch limitation for the later reliability stage.

- [IdentifiedCommandHandler.cs](../../src/Ordering.API/Application/Commands/IdentifiedCommandHandler.cs)
- [IdentifiedCommandHandlerTest.cs](../../tests/Ordering.UnitTests/Application/IdentifiedCommandHandlerTest.cs)

## Acceptance criteria

- [ ] A non-duplicate command forwards the supplied cancellation token to the mediator.
- [ ] The test awaits the handler and observes its returned value.
- [ ] The duplicate path is explained separately from the normal path.
- [ ] The evidence describes what currently happens when the inner command throws, including cancellation.

## Suggested approach

1. Adapt the existing concrete handler test setup.
2. Configure the substitute to return a distinctive value and capture the token.
3. Draw the awaits and exception boundary in the method.

## Verification and evidence

Run Ordering.UnitTests. Show a token-forwarding assertion and a short explanation of the current catch behavior; do not claim cancellation correctness for the entire request pipeline.

## Hints, in order

1. Returning default from a catch can conceal the reason work stopped.
2. A pre-cancelled token alone does not force a substitute to throw.

## Review conversation

What does this test prove about cancellation, and what remains unproven? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
