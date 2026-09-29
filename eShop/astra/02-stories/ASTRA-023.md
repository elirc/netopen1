# ASTRA-023: Preserve missing-order and service-failure meanings

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 4 — HTTP and API contracts  
**Type:** Error handling correction · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-022](ASTRA-022.md)  
**Read first:** [Stage lesson](../01-lessons/04-http-and-contracts.md)

## User story

As an order API consumer, I want missing orders distinguished from service failures so that I can respond appropriately.

## Starting point and scope

OrdersApi.GetOrderAsync currently maps every exception to NotFound. Narrow the missing-data handling; ownership changes are assigned later.

- [OrdersApi.cs](../../src/Ordering.API/Apis/OrdersApi.cs)
- [OrderQueries.cs](../../src/Ordering.API/Application/Queries/OrderQueries.cs)
- [OrdersWebApiTest.cs](../../tests/Ordering.UnitTests/Application/OrdersWebApiTest.cs)

## Acceptance criteria

- [ ] A missing query result represented by the current missing-data exception returns 404.
- [ ] A successful query returns its order.
- [ ] An unexpected query failure is not converted to 404.
- [ ] The HTTP failure behavior is observed or explicitly left pending for the functional layer.

## Suggested approach

1. Add API-method tests for success, missing data, and an unexpected exception.
2. Narrow exception handling to the intended missing-data case.
3. Inspect the host error path before describing the HTTP response.

## Verification and evidence

Run Ordering.UnitTests. Use Ordering.FunctionalTests for any claimed HTTP status/body guarantee; direct method tests only prove exception propagation at that method.

## Hints, in order

1. The query currently throws KeyNotFoundException for a missing row.
2. Returning 500 from a unit test helper is not proof of host middleware behavior.

## Review conversation

Why does a broad catch make both client behavior and diagnosis worse? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
