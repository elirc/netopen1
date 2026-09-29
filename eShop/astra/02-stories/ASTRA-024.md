# ASTRA-024: Validate short checkout input before masking

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 4 — HTTP and API contracts  
**Type:** Defensive API coding · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-023](ASTRA-023.md)  
**Read first:** [Stage lesson](../01-lessons/04-http-and-contracts.md)

## User story

As a checkout client, I want malformed sample payment input rejected as a client error so that it cannot crash string processing.

## Starting point and scope

CreateOrderAsync slices the card string before command validation. Add minimal request-boundary validation with a documented invalid-input response; this is not a payment-processing implementation.

- [OrdersApi.cs](../../src/Ordering.API/Apis/OrdersApi.cs)
- [CreateOrderCommandValidator.cs](../../src/Ordering.API/Application/Validations/CreateOrderCommandValidator.cs)
- [OrdersWebApiTest.cs](../../tests/Ordering.UnitTests/Application/OrdersWebApiTest.cs)

## Acceptance criteria

- [ ] Null, empty, and fewer-than-four-character sample card strings do not throw slicing exceptions.
- [ ] Invalid input is rejected before mediator mutation.
- [ ] A valid synthetic request still follows the existing masking and command path.
- [ ] Normal and invalid request-ID behavior remains covered without adding sensitive logs.

## Suggested approach

1. Reproduce the failure through a direct API-method test.
2. Decide how boundary validation aligns with the command's stricter length rules.
3. Update typed result behavior and add valid-path regression coverage.

## Verification and evidence

Run Ordering.UnitTests and add functional evidence for any new HTTP contract. Use synthetic marker values, never real card data.

## Hints, in order

1. A FluentValidation rule cannot protect code that executes before the command exists.
2. Choose the complete permitted length policy rather than validating only enough characters to avoid Substring.

## Review conversation

Which layer owns input safety here, and which layer still owns business validity? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
