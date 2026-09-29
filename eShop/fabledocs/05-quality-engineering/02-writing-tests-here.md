# Writing Tests Here — Six Recipes

Each recipe: what you're pinning, which real helpers to use, the command (**inferred** unless noted), and the trap.

## Recipe 1: Domain invariant (happy + violation)

Pin: `Order.SetCancelledStatus` throws only from Paid/Shipped (`Order.cs:L142-L153`).
Helpers: none needed — pure objects; use the existing builders (`tests/Ordering.UnitTests/Builders.cs`) to construct an order in a given state; follow MSTest house style (`[TestClass]/[TestMethod]`, `Assert.ThrowsExactly<OrderingDomainException>` as at `OrderAggregateTest.cs:L42`).
Command: `dotnet test tests/Ordering.UnitTests/Ordering.UnitTests.csproj`
Trap: don't reach into private state to force a status — drive it through the public transitions (Submitted→AwaitingValidation→StockConfirmed→Paid). If that's painful, that pain is *information* about the API.

## Recipe 2: Validation failure at the command layer

Pin: card number shorter than 12 fails `CreateOrderCommandValidator` (`CreateOrderCommandValidator.cs:L11`).
Shape: instantiate the validator directly, `validator.Validate(command)`, assert the failing property. No mediator, no pipeline.
Trap: testing through the full pipeline here buys nothing and marries the test to `ValidatorBehavior`'s exception wrapping (which the critique wants to change — R3!). Test the rule, not the plumbing.

## Recipe 3: Permission/authentication failure (gRPC)

Pin: `UpdateBasket` without an authenticated user throws `RpcException(Unauthenticated)` (`BasketService.cs:L38-L41`).
Helpers: `tests/Basket.UnitTests` already builds a `ServerCallContext` with/without a user — copy the existing arrangement in `BasketServiceTests.cs` + `Helpers/`.
Trap: assert on `StatusCode.Unauthenticated`, not the message string (messages aren't contracts).

## Recipe 4: HTTP contract (functional, real DB)

Pin: `GET /api/catalog/items/{id}` returns 400 ProblemDetails for id ≤ 0 (`CatalogApi.cs:L176-L181`) and 404 for missing.
Helpers: `CatalogApiFixture` (real pgvector Postgres) + `CreateClient()`; follow existing `CatalogApiTests.cs` style, including the API-version header/query the client needs.
Command: `dotnet test tests/Catalog.FunctionalTests/Catalog.FunctionalTests.csproj` (Docker running!)
Trap: seed data comes from `Setup/catalog.json` via the startup migrator — don't assume item ids; query the list first or assert shape not identity.

## Recipe 5: Idempotency (async side effect dedup)

Pin: two `IdentifiedCommand`s with the same GUID create one order (`IdentifiedCommandHandler.cs:L41-L48`).
Shape: unit-level with a fake `IRequestManager` (exists-returns-true on second call) asserting mediator `Send` happened once; or functional-level POSTing twice with one `x-requestid` and asserting one order via GET.
Trap: at the functional level, remember the API returns 200 both times *by design* — asserting status codes proves nothing; assert the *count of orders*. (Behavioral assertions beat status assertions — the theme of kata 7.)

## Recipe 6: Cache/state invalidation in the UI layer

Pin: after `BasketState.AddAsync`, subscribers are notified and the next read refetches (`BasketState.cs:L53-L55`).
Shape: `BasketState` takes concrete service classes (not interfaces) — so either extract interfaces (a real, justifiable refactor PR) or test through a fake `HttpMessageHandler`/in-memory gRPC — honest but heavier. Write the test plan *before* the refactor and let the test difficulty argue for the interface extraction in your PR description.
Trap: this recipe's real lesson is that **testability pressure is design feedback** — bring that sentence to interviews.

## Migration behavior (bonus recipe)

Pin: schema at head migration matches the model (`dotnet ef migrations has-pending-model-changes`, EF 9 — **inferred**) — catches "edited the entity, forgot the migration" at CI time instead of at startup-crash time. Cheap, high-value, and absent here; good mid-level ticket.

Fixture-cost warning: each functional-test fixture boots containers — keep functional test *classes* few and their test methods many (xUnit shares the fixture per class via `IAsyncLifetime`/class fixtures).
