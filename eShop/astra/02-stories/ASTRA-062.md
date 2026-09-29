# ASTRA-062: Prototype one basket concurrency strategy

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 11 — Design and delivery  
**Type:** Design spike · **Estimate:** 6-10 hours  
**Prerequisites:** [ASTRA-061](ASTRA-061.md)  
**Read first:** [Stage lesson](../01-lessons/11-design-and-delivery.md)

## User story

As a maintainer, I want a small concurrency prototype so that I can test the ADR's assumptions before a broad implementation.

## Starting point and scope

Implement the narrow approach selected in ASTRA-061 on a practice branch. Any new protocol fields must preserve existing field numbers and have explicit compatibility behavior.

- [RedisBasketRepository.cs](../../src/Basket.API/Repositories/RedisBasketRepository.cs)
- [IBasketRepository.cs](../../src/Basket.API/Repositories/IBasketRepository.cs)
- [basket.proto](../../src/Basket.API/Proto/basket.proto)

## Acceptance criteria

- [ ] Two controlled writers produce the selected merge or conflict behavior.
- [ ] A stale operation does not silently overwrite a newer basket.
- [ ] Distinct users remain isolated.
- [ ] Failure, retry, and old-client limitations are demonstrated and documented.

## Suggested approach

1. Create a Redis-backed experiment with controlled synchronization.
2. Implement only the minimum repository/protocol/client slice needed.
3. Compare observed outcomes with the ADR and revise it.

## Verification and evidence

Provide a repeatable concurrent test using barriers or task coordination, not sleeps. Include Redis-backed evidence; a mock repository cannot prove atomic updates.

## Hints, in order

1. A check followed by an ordinary write is still a race.
2. If adding a version, its comparison and update must share the required atomic boundary.

## Review conversation

Which part of the prototype is still unsuitable for a normal release? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
