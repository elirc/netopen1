# ASTRA-034: Measure a read-only order-query improvement

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 6 — Persistence and domain rules  
**Type:** Query experiment · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-033](ASTRA-033.md)  
**Read first:** [Stage lesson](../01-lessons/06-data-and-domain.md)

## User story

As a maintainer of order browsing, I want a measured read-query change so that performance work preserves the returned contract.

## Starting point and scope

Inspect OrderQueries' EF Core query shapes. Evaluate a narrow tracking or projection change on controlled local data; retain the existing ownership behavior until stage 8.

- [OrderQueries.cs](../../src/Ordering.API/Application/Queries/OrderQueries.cs)
- [OrderingContext.cs](../../src/Ordering.Infrastructure/OrderingContext.cs)
- [OrderingApiTests.cs](../../tests/Ordering.FunctionalTests/OrderingApiTests.cs)

## Acceptance criteria

- [ ] Record baseline query shape, returned fields, and dataset size.
- [ ] Choose one tracking or projection improvement with a stated reason.
- [ ] The same ordered or order-insensitive result contract is preserved as appropriate.
- [ ] Report repeated measurements and limitations rather than claiming an improvement from one request.

## Suggested approach

1. Determine whether entities are tracked or already projected.
2. Build a fixed local dataset and repeat the chosen query.
3. Implement only a justified change, or retain a documented no-change result.

## Verification and evidence

Run Ordering.FunctionalTests and a reproducible measurement procedure. A well-supported conclusion that no change is needed completes the experiment.

## Hints, in order

1. AsNoTracking is not automatically useful on every projection.
2. Do not compare a cold process against a warm process.

## Review conversation

What evidence would make you abandon the optimization? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
