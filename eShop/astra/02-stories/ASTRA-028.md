# ASTRA-028: Make successful basket deletion invalidate display state

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 5 — Basket and state  
**Type:** State correction · **Estimate:** 3-5 hours  
**Prerequisites:** [ASTRA-027](ASTRA-027.md)  
**Read first:** [Stage lesson](../01-lessons/05-basket-and-state.md)

## User story

As a shopper clearing my basket, I want the next read and subscribed display to reflect the deletion so that old items do not remain visible.

## Starting point and scope

BasketState.DeleteBasketAsync currently delegates directly. Align successful deletion with cache invalidation and notification, while specifying behavior on remote failure.

- [BasketState.cs](../../src/WebApp/Services/BasketState.cs)
- [IBasketState.cs](../../src/WebApp/Services/IBasketState.cs)
- [CartMenu.razor](../../src/WebApp/Components/Layout/CartMenu.razor)

## Acceptance criteria

- [ ] After a successful delete, the next basket read cannot return the old cached rows.
- [ ] Change subscribers receive the documented notification after successful deletion.
- [ ] A failed delete is observable and does not falsely notify success.
- [ ] The implementation retains user-scoped state and does not introduce a shared static cache.

## Suggested approach

1. Use the testing lesson to choose a browser scenario or propose a narrow new WebApp test harness.
2. Prime the cache before deleting so the regression is observable.
3. Invalidate and notify at a deliberate point in the operation.

## Verification and evidence

Provide an automated cache-priming regression test and relevant browser evidence. If adding a new WebApp test project, document it as new, wire discovery, and list its direct command.

## Hints, in order

1. A cached Task can return already-loaded rows even after storage changes.
2. A test that starts with an empty cache cannot detect stale cached data.

## Review conversation

What should remain visible when the remote deletion fails? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
