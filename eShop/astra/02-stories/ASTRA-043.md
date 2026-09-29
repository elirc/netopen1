# ASTRA-043: Build an order authorization matrix

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 8 — Identity and defensive coding  
**Type:** Security investigation · **Estimate:** 4-7 hours  
**Prerequisites:** [ASTRA-042](ASTRA-042.md)  
**Read first:** [Stage lesson](../01-lessons/08-identity-and-security.md)

## User story

As an order owner, I want the team to identify who can read or change my orders so that ownership gaps are explicit.

## Starting point and scope

Trace list, detail, create, cancel, and ship paths. Record existing checks and a proposed owner-only course policy without claiming every path is currently protected.

- [OrdersApi.cs](../../src/Ordering.API/Apis/OrdersApi.cs)
- [OrderQueries.cs](../../src/Ordering.API/Application/Queries/OrderQueries.cs)
- [CancelOrderCommandHandler.cs](../../src/Ordering.API/Application/Commands/CancelOrderCommandHandler.cs)
- [ShipOrderCommandHandler.cs](../../src/Ordering.API/Application/Commands/ShipOrderCommandHandler.cs)

## Acceptance criteria

- [ ] For each operation, identify trusted identity, caller-controlled identifiers, and existing ownership checks.
- [ ] Specify owner, non-owner, anonymous, and missing-order outcomes.
- [ ] Choose and document concealed 404 behavior for non-owner access in the course policy.
- [ ] Separate owner permission from domain state restrictions and any future admin capability.

## Suggested approach

1. Follow the actual query and command path for each route.
2. Use the controlled principals from ASTRA-041 for safe local observations.
3. Write the matrix and identify the exact check location for each proposed fix.

## Verification and evidence

Submit source references and local evidence using only synthetic test users/orders. Label unexecuted cases and avoid presenting an investigation as a completed fix.

## Hints, in order

1. RequireAuthorization is not a per-order ownership predicate.
2. Filtering the order list does not protect lookup by ID.

## Review conversation

Which caller-controlled value should never determine the acting user's identity? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
