# ASTRA-061: Write an ADR for concurrent basket updates

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 11 — Design and delivery  
**Type:** Design decision · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-060](ASTRA-060.md), [ASTRA-030](ASTRA-030.md)  
**Read first:** [Stage lesson](../01-lessons/11-design-and-delivery.md)

## User story

As a shopper using two tabs, I want updates handled predictably so that one action does not silently erase another.

## Starting point and scope

Analyze RedisBasketRepository's whole-basket replacement and BasketState's read-modify-write flow. Produce a decision record before changing the protocol.

- [RedisBasketRepository.cs](../../src/Basket.API/Repositories/RedisBasketRepository.cs)
- [BasketState.cs](../../src/WebApp/Services/BasketState.cs)
- [basket.proto](../../src/Basket.API/Proto/basket.proto)

## Acceptance criteria

- [ ] Reproduce or model a two-tab lost-update interleaving with explicit values.
- [ ] Compare conditional versioned writes, server-side operations, and retaining the limitation.
- [ ] Specify conflict behavior visible to the client and a test strategy.
- [ ] Record a selected option, tradeoffs, and migration or compatibility implications.

## Suggested approach

1. Draw both callers reading the same initial basket.
2. Use the ADR template and compare at least two plausible implementations.
3. Ask a mentor to challenge the selected conflict policy.

## Verification and evidence

Submit the ADR and reproducible interleaving evidence. This is a decision story; do not claim the concurrency problem is fixed.

## Hints, in order

1. A local lock cannot coordinate multiple service instances.
2. A version field needs a policy for stale clients.

## Review conversation

Which tradeoff would make you choose a different design? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
