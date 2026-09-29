# Code Review Mindset

## The five layers (review in this order, stop escalating when one fails)

1. **Does it work?** — happy path, obvious errors.
2. **Is it correct?** — edge cases, concurrency, failure modes. (The gym's katas live here: transaction purity, thread-safety, idempotency.)
3. **Will it stay correct?** — tests pin the invariant? next editor misled by anything?
4. **Does it fit?** — this repo's patterns: does a new event use the outbox? does a new endpoint use TypedResults + ProblemDetails? does domain code stay framework-free?
5. **Is it kind to future maintainers?** — names, size, docs where non-obvious.

Junior reviewers start at 5 (style). Review value is concentrated in 2 and 4.

## Repo-specific checklist

- New integration event? → outbox used if a DB write coexists; subscribers registered in every consuming service's Extensions; class name = routing key, so name it like a *fact*, past tense.
- New command? → validator exists; goes through `IdentifiedCommand` if client-retryable; returns honest status codes (post-R3 world).
- Touching `Ordering.Domain`? → no framework references, no logger, invariants in aggregate methods, events raised not handled.
- New endpoint? → auth story explicit (even if "public — because X"); response types complete; version group correct (v1 untouched!).
- Touching `BasketState`/UI state? → invalidation + `NotifyChangeSubscribersAsync` on every mutation path.
- New config? → options pattern; monitor vs snapshot justified; AppHost wiring updated.
- Anything on the bus consumer path? → idempotent under redelivery; cheap before I/O; exceptions understood to be *fatal for the message* (until DLX ships).

## Example comments (calibrated tone)

Blocking, kind, specific:
> "This handler runs inside the EF transaction (see `OrderingContext.SaveEntitiesAsync` — dispatch happens before save), so the SMTP call here will fire even when the order rolls back, and it holds the transaction open for the SMTP round-trip. Could we emit an integration event and send from a consumer instead? The outbox wiring in `CatalogIntegrationEventService` is a good template."

Important, non-blocking:
> "Works as-is — one concern for a follow-up: `ids` is uncapped, and `BasketState` is not the only possible caller. A length cap with a ProblemDetails 400 would match how `GetItemById` handles bad input."

Question-first (when you might be wrong):
> "Is it intentional that duplicates return `true` here rather than the original command's actual result? If a client retries a *failed* create, they'd get success. If that's a known tradeoff, a comment would save the next reader this question."

That last shape — *ask, don't accuse, and leave a trail* — resolves 90% of review friction. Note it's a real question about `IdentifiedCommandHandler.cs:L41-L45`; you know the answer from the pattern catalog. Asking it well anyway is the skill.

Drill: review your own last PR (any repo) against the five layers and rewrite your two weakest comments using the shapes above.
