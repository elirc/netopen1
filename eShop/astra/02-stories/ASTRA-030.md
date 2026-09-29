# ASTRA-030: Allow recovery after a failed basket load

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 5 — Basket and state  
**Type:** Async-state recovery · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-029](ASTRA-029.md)  
**Read first:** [Stage lesson](../01-lessons/05-basket-and-state.md)

## User story

As a shopper after a temporary service interruption, I want a later basket read to retry so that one failed load does not poison the cached state.

## Starting point and scope

BasketState caches a Task. Define failure invalidation without creating an automatic infinite retry loop or clearing a newer successful task.

- [BasketState.cs](../../src/WebApp/Services/BasketState.cs)
- [BasketService.cs](../../src/WebApp/Services/BasketService.cs)

## Acceptance criteria

- [ ] A failed initial fetch remains an observable failure.
- [ ] A subsequent explicit read can attempt a new fetch and succeed.
- [ ] Concurrent readers of the same in-flight request have documented sharing behavior.
- [ ] An older failed operation cannot overwrite or invalidate a newer successful cached result.

## Suggested approach

1. Use a controlled asynchronous test double rather than sleeps.
2. Reproduce a faulted cached Task followed by a healthy dependency.
3. Choose an identity-aware cache reset or equivalent narrow design.

## Verification and evidence

Use the new WebApp harness from ASTRA-028, with deterministic task completion. Include failure-then-success and overlapping-operation cases; run its direct test command.

## Hints, in order

1. Setting the cache to null in every catch can race with newer work.
2. Retry on a future user operation is different from looping inside the failed call.

## Review conversation

Which interleaving would break a naive catch-and-clear implementation? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
