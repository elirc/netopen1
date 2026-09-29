# Good First Tickets — 16 Junior-Sized Contributions

Rules of the game: every ticket says why it's useful, why the blast radius is small, what pattern it follows, how it's tested, and what would make a maintainer reject it. Do them as *practice* even if you never open the PR — but several are genuinely upstreamable.

Template fields are compressed; expand any ticket into the full template from the module README before starting.

---

## Ticket 1: Add TTL to Redis baskets
Difficulty: Easy — 1-2 hrs. Skills: Redis, ops thinking.
Story: as an operator, I want abandoned baskets to expire so Redis doesn't grow unboundedly.
Anchors first: `src/Basket.API/Repositories/RedisBasketRepository.cs:L34-L48`.
Plan: pass `expiry:` to `StringSetAsync` (e.g. 90 days, from config via options pattern — follow `CatalogOptions` shape, `Catalog.API/Extensions/Extensions.cs:L35-L36`).
Tests: extend `tests/Basket.UnitTests` (repository is behind `IBasketRepository`; the TTL itself needs an integration test or manual `redis-cli TTL` check — say so in the PR).
Reject-risk: hardcoding the TTL; picking a TTL without justifying it; forgetting that *updates* must refresh the TTL.
Interview story potential: "Found and fixed an unbounded-growth risk in a cache layer, made it configurable."

## Ticket 2: Return 400 instead of 200 when create-order fails
Difficulty: Medium — half day. Skills: HTTP contracts, MediatR.
Story: as an API consumer, I need failures to be visible in the status code.
Anchors: `OrdersApi.cs:L157-L166`; root cause `IdentifiedCommandHandler.cs:L99-L102`.
Plan: minimally — check `result` at the API layer and return `TypedResults.Problem(...)` on false. (The deeper fix — stop swallowing exceptions — is a mid-level ticket; don't scope-creep.)
Tests: `tests/Ordering.FunctionalTests` — post an order with an invalid card length, assert non-2xx.
Reject-risk: this IS a contract change — flag it loudly in the PR; check `WebApp/Services/OrderingService.cs` (does it throw on non-success? then WebApp behavior changes too).
Interview story: "Changed an API that lied with 200s — and handled the consumer-compat fallout."

## Ticket 3: Require authorization on catalog write endpoints
Difficulty: Medium — half day. Skills: authN/authZ, minimal APIs.
Anchors: `CatalogApi.cs:L93-L110`; JWT setup `AuthenticationExtensions.cs`; Catalog.API currently calls neither `AddDefaultAuthentication` nor `UseAuthorization` — verify and wire it.
Plan: group the three mutation endpoints, `.RequireAuthorization()`; add the Identity section to Catalog's appsettings; AppHost env var like basket/ordering get (`eShop.AppHost/Program.cs:L33`).
Tests: functional test asserting 401 without token.
Reject-risk: breaking the seeding/dev flow or the `Program.Testing.cs` test host; not checking whether any internal caller (mobile-bff route?) does unauthenticated writes.
Interview story: "Closed an unauthenticated write surface across service + orchestrator + tests."

## Ticket 4: Fix double-registered route summary drift (v1/v2 UpdateItem docs)
Difficulty: Easy — 1 hr. Skills: OpenAPI hygiene.
Anchors: `CatalogApi.cs:L93-L102` — both versions say "Create or replace a catalog item"; v2's description at L326 says "The id of the catalog item to **delete**" on an *update* param.
Plan: correct the `[Description]` and summaries.
Tests: none needed; regenerate/inspect OpenAPI (`Catalog.API.json`).
Reject-risk: touching generated spec files by hand instead of regenerating.
Interview story: small, but demonstrates contract-doc care.

## Ticket 5: Meaningful basket item id
Anchors: `BasketState.cs:L138` — `Id = Guid.NewGuid().ToString()` with a `// TODO: this value is meaningless, use ProductId instead.`
Difficulty: Easy — 2 hrs. Plan: do what the TODO says; find every consumer of `BasketItem.Id` in WebApp/WebAppComponents first (grep) — that search IS the ticket.
Reject-risk: the Id is used as a Blazor `@key` somewhere and duplicate ProductIds can't occur… prove it.
Interview story: "Resolved a maintainer TODO touching UI list identity."

## Ticket 6: Log when a status transition is silently ignored
Difficulty: Easy-Medium — 2-3 hrs. Skills: domain events, observability.
Anchors: `Order.cs:L99-L128` — no-op guards hide misdelivered events (see pattern card 8).
Plan: domain layer must stay logger-free — so *return* a bool from the setters or raise a "transition rejected" domain event; log in the command handlers (`SetPaidOrderStatusCommandHandler.cs` etc.).
Reject-risk: injecting ILogger into the aggregate (breaks domain purity — instant rejection); changing the throwing guards' behavior.
Interview story: "Added observability to a state machine without polluting the domain layer."

## Ticket 7: Add `AsNoTracking` to catalog read queries
Difficulty: Easy — 1-2 hrs. Skills: EF performance.
Anchors: `CatalogApi.cs:L149-L156, L162-L167, L183`.
Plan: add `.AsNoTracking()` to read-only queries; measure (BenchmarkDotNet optional, honesty required).
Reject-risk: applying it to `UpdateItem`'s load (L330 — that one NEEDS tracking, `SetValues` depends on it). If your PR touches that line, you've failed the ticket.
Interview story: "Perf-tuned EF read paths and knew where NOT to."

## Ticket 8: Playwright e2e for checkout
Difficulty: Medium — 1 day. Skills: e2e, auth in tests.
Anchors: `e2e/AddItemTest.spec.ts`, `e2e/login.setup.ts`, `playwright.config.ts`.
Plan: follow the existing spec style: login (setup project exists), add item, checkout, assert order appears in `/user/orders`.
Reject-risk: flakiness — the order-status page updates via bus events; assert on "Submitted" presence, not on later statuses with fixed sleeps.
Interview story: "Closed the e2e gap on the money path" — also your best testing STAR story.

## Ticket 9: Health check for RabbitMQ consumer connectivity
Difficulty: Medium — half day+. Skills: health checks, hosted services.
Anchors: `RabbitMQEventBus.cs:L226-L295` (failure at startup only logs, `:L287-L290`).
Plan: expose connection state; register an `IHealthCheck` reporting Unhealthy when the consumer channel is closed; ServiceDefaults maps `/health` already.
Reject-risk: making the health check itself open connections (probe state, don't create it).
Interview story: "Made an invisible failure mode visible" — pairs with Q8 in the deep-dive.

## Ticket 10: Deduplicate `CreateOrderRequest`
Difficulty: Medium — half day. Skills: contracts, project structure.
Anchors: `BasketState.cs:L158-L172` vs `OrdersApi.cs:L171-L185` (14 fields, hand-synced).
Plan: options — shared contracts project vs generated client vs leave-but-test. Smallest honest step: a unit test in WebApp that asserts the serialized shape matches (field-name snapshot), documenting the duplication instead of removing it. Propose the shared project in the PR description as follow-up.
Reject-risk: creating a WebApp→Ordering.API project reference (couples deploys — the duplication exists to AVOID that; understand before "fixing").
Interview story: the best "I understood why the ugly thing was there before touching it" story in the repo.

## Ticket 11: Empty-GUID request id returns ProblemDetails, not plain string
Difficulty: Easy — 1 hr.
Anchors: `OrdersApi.cs:L27-L30` returns `BadRequest<string>`; the repo's own convention elsewhere is ProblemDetails (`CatalogApi.cs:L176-L181`).
Plan: align the three command endpoints on ProblemDetails.
Reject-risk: it's a wire-contract change (string body → JSON object); note it.

## Ticket 12: Guard `GetItemsByIds` against unbounded id lists
Difficulty: Easy — 2 hrs. Skills: input validation, defensive API design.
Anchors: `CatalogApi.cs:L162-L168` — `ids` array has no length cap; a 10k-id query string produces a giant `IN` clause.
Plan: cap (e.g., 100) → 400 ProblemDetails beyond it; document in OpenAPI description.
Reject-risk: breaking `BasketState.FetchBasketItemsAsync` (`BasketState.cs:L132`) — its basket sizes are small, but confirm.
Interview story: "Added a resource-exhaustion guard to a batch endpoint."

## Ticket 13: Order search by date range on "my orders"
Difficulty: Medium — 1 day. Skills: query side of CQRS.
Anchors: `OrdersApi.cs:L93-L98`, `Application/Queries/OrderQueries.cs`.
Plan: optional `from`/`to` query params → queries class → SQL/EF filter; keep the identity scoping intact.
Reject-risk: filtering in memory after fetching all orders; breaking the ownership filter.
Interview story: "Extended a CQRS read path end to end."

## Ticket 14: Surface stock-rejection reason in the UI
Difficulty: Medium — 1 day. Skills: full-stack trace.
Anchors: `Order.cs:L155-L168` writes rejected product names into `Description`; check the query DTO and `WebApp/Components/Pages/User/Orders.razor` — is Description shown?
Plan: expose Description on the order detail view if absent.
Reject-risk: leaking internal text to users unstyled; i18n concerns worth mentioning even if unresolved.

## Ticket 15: Configurable page size cap on catalog pagination
Difficulty: Easy — 2 hrs.
Anchors: `PaginationRequest` model (`Catalog.API/Model/`), used at `CatalogApi.cs:L131-L132`. Is there any max? If a caller passes pageSize=100000, what happens? (Check, then cap.)
Reject-risk: changing the default page size (visible UI change) when only the cap was asked.

## Ticket 16: Document the event catalog
Difficulty: Easy — half day, docs-only. Skills: the best "learn by writing" ticket.
Plan: a markdown table of every `*IntegrationEvent` class: publisher, subscribers, payload, trigger. Grep `AddSubscription` for the subscriber map (`Basket/Catalog/Ordering/WebApp/Webhooks` extensions files).
Reject-risk: letting it rot — propose placing it near the code and noting the "routing key = class name" invariant so renames update it.
Interview story: "Mapped an undocumented event-driven system for the next engineer."

---

Meta-drill: before opening any PR, answer the maintainer's five questions in writing — useful why? small blast radius why? which existing pattern followed? tested how? rejected why? If you can't answer the fifth, you haven't understood the codebase yet.
