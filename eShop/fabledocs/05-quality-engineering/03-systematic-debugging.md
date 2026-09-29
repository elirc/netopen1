# Systematic Debugging

The method, always: **reproduce → narrow (bisect the system, not the code) → hypothesize → test the hypothesis cheaply → fix the root cause → add regression coverage.** Guessing-and-rerunning is the junior tell; narrowing by halves with cheap probes is the mid-level tell; choosing the *cheapest decisive probe* is the senior tell.

Tools of this repo: the **Aspire dashboard** (per-service logs + distributed traces — one checkout = one trace across HTTP *and* RabbitMQ), structured logs (every event handler logs event id + payload), `docker exec` into Postgres/Redis/RabbitMQ (`psql`, `redis-cli`, management UI), EF query logging (`Microsoft.EntityFrameworkCore.Database.Command` at Information), the `throw-fake-exception` chaos hook (`RabbitMQEventBus.cs:L163-L166`), and breakpoints in VS/VS Code attached to any of the seven processes.

---

## Scenario 1: "I placed an order and my basket didn't empty"

Reproduction: checkout; return to cart; items still there (sometimes).
First question: did the **event** fail, or the **direct delete** (`BasketState.cs:L108`), or did the UI just show stale state?
Narrowing path:
1. Redis truth first: `redis-cli GET /basket/<sub>`. Empty? → UI cache problem (`_cachedBasket` not invalidated after checkout — read `CheckoutAsync`: it calls `DeleteBasketAsync`… does anything null `_cachedBasket` or notify subscribers? Compare with `AddAsync` L53-L55. **There's the bug shape.**)
2. Not empty? → check Basket.API logs for `OrderStartedIntegrationEventHandler` (did the event arrive?).
3. No event? → outbox: `SELECT * FROM "IntegrationEventLog" WHERE "State" = 0` in orderingdb (NotPublished = stuck, R2 in the critique).
Useful probes: trace view in Aspire dashboard — the publish span should have a consume child span.
Likely root causes, ranked: UI cache invalidation gap; event lost to handler exception (acked anyway); outbox row orphaned by crash.
Regression test: UI-level — after `CheckoutAsync`, `GetBasketItemsAsync` returns empty without a page reload.
Senior lesson: three subsystems can each cause one symptom; check the *source of truth* (Redis) first, then walk outward. Interview version: narrate the ranked hypotheses *before* probing — that's what they're grading.

## Scenario 2: "Orders stuck in AwaitingValidation forever"

Reproduction: order placed; grace period passes; status moves to AwaitingValidation; never advances.
First question: did Catalog.API *receive* `OrderStatusChangedToAwaitingValidation`, and did it *publish* a stock result?
Narrowing path:
1. Catalog logs: handler entry line (`OrderStatusChangedToAwaitingValidation...Handler.cs:L11`). Absent → binding/queue problem (was Catalog running when the event fired? Queue is durable — `RabbitMQEventBus.cs:L258-L263` — so it should deliver on restart; check RabbitMQ management UI for the queue and its bindings).
2. Present but exception after it → **acked and lost** (L177-L180). Look for the warning "Error Processing message".
3. Handler succeeded → did Ordering receive StockConfirmed/StockRejected? Same check on Ordering's side.
Likely root causes: a product id in the order deleted from catalog (`Find` returns null → item *skipped* — L17-L18 — order of N items produces N-1 confirmations and... read L27-L29: does it still publish? Yes — skipped items just aren't checked. Different bug: order confirms despite a dead product).
Regression test: functional test publishing the event with an unknown product id, asserting the outcome you decide is correct.
Senior lesson: "stuck saga" debugging is queue-topology + logs at each hop; build the hop checklist before touching code.

## Scenario 3: "Checkout returns 200 but no order exists"

Reproduction: POST /api/orders with a card number of 5 digits → 200 OK, orders list empty.
First question: is this the known swallow (`IdentifiedCommandHandler.cs:L99-L102`)?
Narrowing path:
1. Ordering logs: "Validation errors" warning from `ValidatorBehavior.cs:L30`? → FluentValidation rejected it (card length 12–19, `CreateOrderCommandValidator.cs:L11`); exception swallowed; API returned Ok. Root cause confirmed, by design (R3).
2. No validation warning → check request id reuse: was this GUID used before? (`SELECT * FROM ordering."requests"` — duplicate → canned success, `CreateOrderCommandHandler.cs:L67-L70`.)
Regression test: exists only after fixing the contract (ticket 2); write it first, watch it fail — that's the point of tickets.
Senior lesson: "the API lied" bugs demand you distrust status codes and go to logs/DB; then fix the *contract*, not the caller.

## Scenario 4: "Product page images broken, everything else fine"

First question: which hop — browser → WebApp forwarder → Catalog file read?
Narrowing path:
1. DevTools network tab: `/product-images/99` status? 404 vs 502 vs 200-empty tell different stories.
2. 502/connection → the forwarder (`WebApp/Program.cs:L32`) can't resolve `catalog-api` (service discovery/env).
3. 404 → Catalog side: `GetItemPictureById` (`CatalogApi.cs:L205-L224`) returns NotFound when the item or `PictureFileName` is missing; else it builds a path under `Pics/` (`:L420-L421`) — file actually on disk in the container?
Useful probes: hit `catalog-api/api/catalog/items/99/pic` directly (bypass the forwarder) — the single probe that halves the search space. Choose it first.
Senior lesson: for any proxied resource, test both sides of the proxy before reading any code.

## Scenario 5: "After a deploy, Basket.API rejects every call as Unauthenticated"

Reproduction: all gRPC calls throw `Unauthenticated` (`BasketService.cs:L41,L72`).
First question: is the token missing, or rejected?
Narrowing path:
1. `GetUserIdentity()` reads the `sub` claim. Empty means: no token attached, or token valid but claim mapped away.
2. Check WebApp side: `.AddAuthToken()` on the gRPC client (`WebApp/Extensions.cs:L31-L32`) — still registered?
3. Token attached but no `sub` → the classic: `JsonWebTokenHandler.DefaultInboundClaimTypeMap.Remove("sub")` (`AuthenticationExtensions.cs:L31`) — if someone "cleaned up" that line, `sub` gets remapped to `nameidentifier` and vanishes. Realistic regression: it looks like dead code to a newcomer.
4. Token rejected entirely → issuer mismatch: `Identity__Url` env vs token issuer (AppHost wiring `eShop.AppHost/Program.cs:L33`).
Regression test: unit test asserting `GetUserIdentity()` returns the sub for a token minted with test claims.
Senior lesson: auth bugs are config-and-mapping bugs 90% of the time; know your claim pipeline cold. Interview version: this narration (missing vs rejected vs remapped) is precisely what an "auth debugging" round wants.

---

Drill: pick scenario 2, set `PaymentSucceeded=false` in PaymentProcessor's appsettings, run the system, and follow an order into cancellation using only the dashboard (no code reading). Time-box: 30 minutes.
Self-grade — Basic: found the failed-payment log lines. Solid: followed the full event chain in the trace view and saw `SetCancelledStatus`. Strong: also predicted, before looking, which services would log what — and were right.
