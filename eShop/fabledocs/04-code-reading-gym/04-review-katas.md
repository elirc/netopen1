# Review Katas

Eight fake PRs against this codebase. For each: read the intent and diff summary, list findings graded **Blocking / Important / Optional**, then compare. Write your comments as you would post them — specific, kind, with a suggested path.

Grading yourself: Basic = caught the planted Blocking issue. Solid = caught it *and* graded severities sensibly (didn't block on style). Strong = also caught the subtle second issue and your comments propose fixes, not just complaints.

---

## Kata 1: "Add email notification when order ships"
Author intent: send email on shipment.
Fake diff: adds `SmtpClient.SendAsync(...)` inside `OrderShippedDomainEvent` handler (`Ordering.API/Application/DomainEventHandlers/`).
Files this resembles: `OrderingContext.cs:L47-L62` (handlers run pre-commit).
Expected findings — **Blocking:** network I/O inside the DB transaction (email sends even on rollback; transaction held open across SMTP latency) — belongs in an integration-event consumer. **Important:** no retry story; secrets in config? **Optional:** template wording.
Good comment: > "Domain event handlers here run inside the transaction (`OrderingContext.SaveEntitiesAsync` dispatches before save) — an SMTP call in this scope sends mail for orders that then fail to commit. Could we publish an `OrderShipped` integration event instead and send from a consumer? Happy to pair on the outbox wiring."

## Kata 2: "Perf: parallelize event handlers"
Author intent: speed up message processing.
Fake diff: `RabbitMQEventBus.ProcessEvent` foreach → `Task.WhenAll(handlers.Select(h => h.Handle(evt)))`.
Files: `RabbitMQEventBus.cs:L204-L207` (the `// REVIEW` comment tempts exactly this).
Expected — **Blocking:** handlers resolved from one scope may share scoped services (DbContext is not thread-safe) → intermittent `InvalidOperationException` under load, worst kind of bug. **Important:** no benchmark provided for a perf PR. **Optional:** if pursued, scope-per-handler is the safe shape.

## Kata 3: "Cleanup: remove weird 'sub' line"
Author intent: delete `JsonWebTokenHandler.DefaultInboundClaimTypeMap.Remove("sub");` as dead code.
Files: `AuthenticationExtensions.cs:L31`, `WebApp/Extensions.cs:L58`, consumers `BasketService.cs:L15`.
Expected — **Blocking:** every identity lookup reads the raw `sub` claim; removal remaps it to the long XML claim type and all lookups return null → all users effectively logged out of APIs (see debugging scenario 5). **Important:** absence of tests that would have caught it — ask for one. **Optional:** add a comment explaining the line (the real fix for "looks like dead code").

## Kata 4: "Add DeleteBasket REST endpoint for admin support"
Author intent: support tooling wants to clear a user's basket by id.
Fake diff: new minimal API in Basket.API: `DELETE /baskets/{userId}` calling `repository.DeleteBasketAsync(userId)`, no auth attribute.
Files: `BasketService.cs:L59-L69` (existing delete requires the *caller's own* identity).
Expected — **Blocking:** breaks the isolation-by-construction model — introduces the first endpoint where a caller names another user's key, with no authZ. Needs an admin policy/scope at minimum. **Important:** REST endpoint on a gRPC-only service doubles the surface (ops, auth config); is support tooling inside the trust boundary? **Optional:** audit logging for admin mutations (arguably Important).

## Kata 5: "Fix: retry failed messages"
Author intent: stop losing messages on handler exceptions.
Fake diff: in `OnMessageReceived` catch block, replace ack with `BasicNackAsync(..., requeue: true)`.
Files: `RabbitMQEventBus.cs:L170-L180`.
Expected — **Blocking:** requeue-forever turns one poison message into an infinite hot loop (redelivered to head of queue, fails, repeats — the queue never drains). Needs DLX or retry-count cap. **Important:** the intent is right (current ack-on-error loses messages, R1) — say so explicitly; steer, don't reject the goal. **Optional:** metrics on redelivery count.

## Kata 6: "Add CreatedAt to CatalogItem"
Author intent: show "new arrivals."
Fake diff: adds property + migration with `DefaultValue(DateTime.UtcNow)` in the model, renames `PaginatedItems.Count` → `Total` "while here."
Expected — **Blocking:** the rename is a **public wire-contract change** smuggled into an unrelated PR (breaks WebApp deserialization and mobile clients; see contrast #10). **Important:** `DefaultValue(DateTime.UtcNow)` bakes *build-time* constant into the migration (classic EF trap) — want `HasDefaultValueSql("now()")`. **Optional:** index on CreatedAt if queried.

## Kata 7: "Test: assert checkout returns 200"
Author intent: add coverage for order creation.
Fake diff: functional test posting a valid order, asserting `HttpStatusCode.OK` only.
Expected — **Important:** asserting the *known-lying* status code (R3) pins the wrong behavior into the test suite — assert the order exists via GET (behavioral outcome), or better, drive the contract fix first. **Important:** no negative case (invalid card). **Optional:** test data builder reuse (`tests/Ordering.UnitTests/Builders.cs` exists — match local conventions). Nothing Blocking — merging a weak test is better than no test; grade accordingly. (Katas that contain *no* blocking finding are part of the training.)

## Kata 8: "Refactor: BasketState singleton for performance"
Author intent: fewer allocations; registers `BasketState` as singleton.
Files: `WebApp/Extensions.cs:L23`.
Expected — **Blocking:** `BasketState` holds *a specific user's* basket cache and subscriptions; singleton = every visitor shares one basket. Security bug dressed as perf. **Important:** the perf claim is unmeasured. **Optional:** if allocation pressure were real, the fix is caching in `BasketService` (already singleton, stateless) keyed by user.

---

Meta-pattern across all eight: the Blocking findings are never style — they are **broken invariants** (transaction purity, thread affinity, claim mapping, isolation-by-identity, queue liveness, wire contracts, test honesty, state ownership). Review = invariant checking. Take that sentence to [../08-interview-prep/05-debugging-and-code-review-rounds.md](../08-interview-prep/05-debugging-and-code-review-rounds.md).
