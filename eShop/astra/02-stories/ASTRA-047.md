# ASTRA-047: Keep checkout secrets out of every log path

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 8 — Identity and defensive coding  
**Type:** Sensitive-output correction · **Estimate:** 4-7 hours  
**Prerequisites:** [ASTRA-046](ASTRA-046.md)  
**Read first:** [Stage lesson](../01-lessons/08-identity-and-security.md)

## User story

As a shopper using checkout, I want sensitive request fields excluded from diagnostics so that debugging does not expose them.

## Starting point and scope

Audit invalid request-ID logging, command logging, transaction logging, and event payload paths. Use synthetic markers; do not assume masking the normal card number covers all fields.

- [OrdersApi.cs](../../src/Ordering.API/Apis/OrdersApi.cs)
- [LoggingBehavior.cs](../../src/Ordering.API/Application/Behaviors/LoggingBehavior.cs)
- [TransactionBehavior.cs](../../src/Ordering.API/Application/Behaviors/TransactionBehavior.cs)
- [IdentifiedCommandHandler.cs](../../src/Ordering.API/Application/Commands/IdentifiedCommandHandler.cs)

## Acceptance criteria

- [ ] Synthetic card number and security-code markers do not appear in structured state or rendered logs on the selected success and failure paths.
- [ ] Safe request/correlation identifiers remain available for diagnosis.
- [ ] Request and command destructuring is replaced with deliberate safe fields where needed.
- [ ] Tests include an invalid request ID and an exception path, not only normal checkout.

## Suggested approach

1. Trace every selected logger call before editing.
2. Use a capturing logger or narrow test provider to inspect fields and text.
3. Change logging consistently across the audited paths and document remaining scope.

## Verification and evidence

Run relevant Ordering tests and search captured output for unique synthetic markers. Record the precise paths audited; do not claim a repository-wide audit if only checkout was tested.

## Hints, in order

1. A logger mock verifying a message template can miss sensitive structured arguments.
2. Exception messages or event bodies can create another output path.

## Review conversation

Which identifiers give diagnostic value without copying the request payload? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
