# Choose the test boundary that can prove the change

Learning goal: build confidence with small, deterministic tests and honest limitations.

## The test inventory

| Existing project or suite | Framework / setup | Useful for | Cannot alone prove |
| --- | --- | --- | --- |
| [Ordering.UnitTests](../../tests/Ordering.UnitTests/Ordering.UnitTests.csproj) | MSTest, NSubstitute | Domain rules, command and API-method logic | HTTP middleware or PostgreSQL |
| [Basket.UnitTests](../../tests/Basket.UnitTests/Basket.UnitTests.csproj) | MSTest, NSubstitute | gRPC service logic with a fake context | Real tokens, network transport, Redis |
| [Catalog.FunctionalTests](../../tests/Catalog.FunctionalTests/Catalog.FunctionalTests.csproj) | xUnit v3, WebApplicationFactory, Aspire PostgreSQL | Routing, serialization, real catalog persistence | Full storefront behavior |
| [Ordering.FunctionalTests](../../tests/Ordering.FunctionalTests/Ordering.FunctionalTests.csproj) | xUnit v3, host fixture and database | Order HTTP behavior in its fixture | Production authentication flow |
| [e2e](../../e2e) | Playwright | Browser journeys through the app | Every domain edge case |
| [ClientApp.UnitTests](../../tests/ClientApp.UnitTests/ClientApp.UnitTests.csproj) | Separate mobile track | MAUI view models and services | WebApp components |

Read [tests/Directory.Build.props](../../tests/Directory.Build.props) and each project's global imports. The repository uses Microsoft.Testing.Platform; MSTest attributes do not belong in the xUnit functional project.

## A red-to-green experiment

1. Describe the bug with one input and one expected output.
2. Add the smallest test entering the layer that owns the behavior.
3. Run it against unchanged production code and confirm the failure is the intended assertion.
4. Fix the behavior.
5. Run the test project and relevant nearby checks.
6. Review whether the test would catch a plausible reintroduction of the bug.

A compile failure from a misspelled class name is not a useful red phase. A test that replaces the behavior under test with a mock proves the setup rather than the behavior.

## Use NSubstitute at a boundary

For an invalid basket update, substitute IBasketRepository and supply a real gRPC service instance and test context. Assert the RpcException status, then assert UpdateBasketAsync was not received. This proves that validation precedes persistence.

For a catalog SQL filter, a mocked IQueryable is not an adequate substitute for the PostgreSQL provider. Use the existing functional fixture and controlled data.

## Fixture isolation is part of correctness

CatalogApiTests contains a total-count expectation of 103 that explicitly depends on other tests adding rows. Such an assertion is fragile under reordering or a focused run. Tests also mutate seeded records. A passing full suite does not make that dependency safe.

Prefer a test-owned dataset, unique IDs or names, and cleanup or a fresh fixture boundary. If using a baseline count, ensure concurrent writes cannot change it between reads. “Disable parallelism” alone does not explain ownership or cleanup.

Read the Ordering fixture's [AutoAuthorizeMiddleware](../../tests/Ordering.FunctionalTests/AutoAuthorizeMiddleware.cs). A test helper that supplies identity can mask the real authentication path. Use controlled principals for ownership tests, and retain a separate real sign-in check for authentication.

## When a new test project is justified

The baseline has no dedicated Catalog.UnitTests or WebApp.UnitTests. Some course stories need pure catalog model tests or controlled BasketState tests. Before adding a project:

1. Explain why an existing suite cannot isolate the behavior cleanly.
2. Follow the repository's target framework, central package management, and MTP conventions.
3. Add the project to the intended solution and web filter if it belongs in the standard web checks.
4. Prove discovery with a meaningful test and a direct project run.
5. Keep any new seam narrow; do not refactor an entire service solely to satisfy mocking preferences.

A proposed path in a story is clearly labeled new. New UI tests can also extend Playwright where that is the appropriate evidence.

## Browser reliability

Use role and label locators, test-owned data, and assertions that wait for the intended state. Avoid fixed sleeps. Logged-in tests currently share a saved identity and run in parallel locally, so mutations can interfere. Isolation should come from identities or data ownership; a scoped serial group can be an explicitly documented temporary limitation.

Always inspect test discovery. The Playwright project names and explicit file matching are part of this repository's test contract.

## Record the result

Write command, outcome, relevant test count, and unresolved limitation in the PR. A blocked Docker-backed test is pending evidence. Do not substitute a unit test and describe the functional path as verified.
