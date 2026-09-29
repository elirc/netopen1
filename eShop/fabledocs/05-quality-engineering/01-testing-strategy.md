# Testing Strategy

## The layers as they actually exist here

| Layer | Projects | Runs against | Speed | What belongs here |
| --- | --- | --- | --- | --- |
| Unit — domain | `tests/Ordering.UnitTests/Domain` (MSTest) | pure objects, zero mocks | ms | invariants: `OrderItem` rejects negative units (`OrderAggregateTest.cs:L31-L43`), status transitions, discount rules |
| Unit — application/service | `tests/Ordering.UnitTests/Application`, `tests/Basket.UnitTests` | handlers/gRPC service with substituted deps (`IBasketRepository` fake) | ms | orchestration decisions: "unauthenticated → RpcException", "duplicate request id → canned result" |
| Functional/integration | `tests/Catalog.FunctionalTests`, `tests/Ordering.FunctionalTests` (xUnit) | **real Postgres container** via Aspire fixture (`CatalogApiFixture.cs:L17-L25`) + `WebApplicationFactory` | seconds | HTTP contracts, EF mappings, migrations, pagination SQL |
| e2e | `e2e/*.spec.ts` (Playwright) | the whole running system | minutes | the 3 user journeys that pay the bills: browse, add-to-cart, (checkout — missing, ticket 8) |
| CI | `ci.yml:L44` | — | — | **build only.** No test execution in this public pipeline — a gap to know about before trusting a green badge |

What deliberately has *no* tests: the RabbitMQ bus internals, the workers, Identity's vendored UI, the Blazor components. What that costs: cross-service flows (Flow 4) are verified by no automated thing — only by running the system.

## The judgment calls (transferable)

- **Test the invariant, not the implementation.** `OrderAggregateTest` asserts behavior of the aggregate's public methods; it never inspects private state. When the internal list becomes a dictionary, tests survive.
- **Push tests down.** A rule enforceable in the domain (units > 0) is tested in milliseconds; testing it through HTTP costs 10,000× more per run and fails less legibly. The repo's shape agrees: richest tests where the richest logic lives.
- **Real DB over mocked DbContext.** The functional fixtures boot pgvector Postgres rather than mocking EF (mocked EF passes tests that in-SQL translation would fail). Cost: Docker required, seconds not ms. This is the correct trade and you should be able to argue it.
- **Isolation:** each functional fixture owns a fresh container/database — no shared state between test classes; unit tests share nothing by construction.
- **Time and randomness:** `Order.OrderDate = DateTime.UtcNow` (`Order.cs:L58`) is untestable-as-written for time-sensitive assertions; the grace-period logic depends on wall-clock — the repo dodges by testing neither. A `TimeProvider` (built into .NET 8+) is the modern fix; bringing that up is a strong PR conversation.
- **Flake prevention in e2e:** the login is a Playwright *setup project* (`e2e/login.setup.ts` — authenticate once, reuse state); assertions should target stable text/roles, and never sleep for bus-driven status changes (poll/await instead).

## What NOT to test (equally a skill)

Framework behavior (EF `Include` works; Microsoft tests it), the vendored Identity UI, mapping boilerplate with no branches (`BasketService.MapToCustomerBasket` — one branchless loop; a test would restate the code), and log message wording.

Interview angle: "How do you decide unit vs integration?" — answer with the *push-down rule* and the mocked-EF trap. "How do you test against a DB in CI?" — container-per-fixture, and name the tradeoff you accept (runtime). Both cards in [../08-interview-prep/03-api-and-data-modeling-questions.md](../08-interview-prep/03-api-and-data-modeling-questions.md).

Drill: classify these five hypothetical tests into layers (or "don't write it"): (a) "cancel a Shipped order throws"; (b) "GET /items?type=3 filters by type"; (c) "OrderStarted event empties basket"; (d) "RabbitMQ reconnects after broker restart"; (e) "checkout page shows validation summary".
Self-grade — reference: (a) domain unit; (b) functional; (c) cross-service — today only manual/e2e, say what you'd build (in-proc bus fake or a docker-composed integration suite); (d) don't write it (library + ops concern) or a smoke test at most; (e) e2e or Blazor component test (bUnit — not present; note the introduction cost).
