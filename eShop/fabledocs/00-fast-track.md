# Fast Track — One Weekend in eShop

Goal: by Sunday night you can run the system, trace two flows end-to-end, make one safe change, run one test suite, and explain the checkout flow aloud like an interview candidate.

## 1. Install and run (~45 min, mostly waiting)

Prerequisites: .NET 9 SDK, Docker Desktop **running** (Postgres, Redis, RabbitMQ all run as containers).

| Command | Status |
| --- | --- |
| `dotnet run --project src/eShop.AppHost/eShop.AppHost.csproj` | **inferred** (from `README.md:L73-L80`; not executed while writing these docs) |
| Open the Aspire dashboard URL printed as `Login to the dashboard at: http://localhost:19888/login?t=...` | **inferred** (README) |
| `dotnet build eShop.Web.slnf` | **inferred** (this is exactly what CI runs — `ci.yml:L44`) |
| `dotnet test tests/Ordering.UnitTests/Ordering.UnitTests.csproj` | **inferred** (standard; unit tests have no container dependencies) |

The AppHost is the only thing you start. It starts everything else — read `src/eShop.AppHost/Program.cs:L7-L18` and watch the dashboard fill in: one Postgres server with **four databases** (catalogdb, identitydb, orderingdb, webhooksdb), Redis, RabbitMQ, seven .NET services, and a YARP proxy for mobile.

From the dashboard, open the resource named **webapp** ("Online Store"). Log in with the seeded test user — check `src/Identity.API/UsersSeed.cs` for credentials (commonly `alice`/`bob` with password `Pass123$` in this family of samples — verify in that file).

## 2. First 10 files to open, in order

| # | File | Why |
| --- | --- | --- |
| 1 | `src/eShop.AppHost/Program.cs` | The whole system on one page. Every service, dependency, and env var. |
| 2 | `src/WebApp/Program.cs` | Blazor Server storefront startup; note `MapForwarder` for product images at L32. |
| 3 | `src/WebApp/Extensions/Extensions.cs` | How the UI reaches every backend: gRPC client (L31-L32), typed HTTP clients (L34-L40), OIDC login (L53-L92). |
| 4 | `src/WebApp/Services/BasketState.cs` | The UI's per-circuit state holder. Checkout lives here (L78-L109). |
| 5 | `src/Catalog.API/Apis/CatalogApi.cs` | Minimal API endpoint catalog; pagination + filtering at L124-L159. |
| 6 | `src/Basket.API/Grpc/BasketService.cs` | gRPC service; identity extraction and auth boundary (L13-L19). |
| 7 | `src/Ordering.API/Apis/OrdersApi.cs` | Commands enter here; note the `x-requestid` idempotency header (L119). |
| 8 | `src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs` | The richest domain object in the repo: state machine + domain events. |
| 9 | `src/Ordering.API/Application/Behaviors/TransactionBehavior.cs` | Where "save to DB" and "publish events" are made atomic. |
| 10 | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | How every integration event physically moves. |

## 3. Trace two flows (pen and paper)

**Flow A — browse the catalog:** Browser → `src/WebApp/Components/Pages/Catalog/Catalog.razor` → `CatalogService` typed HttpClient (`src/WebApp/Extensions/Extensions.cs:L34-L36`) → `GET api/catalog/items` (`src/Catalog.API/Apis/CatalogApi.cs:L26-L30` → handler L124-L159) → EF Core → Postgres. Write down: where does paging happen? (Answer: `Skip/Take` at L152-L156 — in the database, not in memory.)

**Flow B — checkout:** `Checkout.razor:L111-L116` → `BasketState.CheckoutAsync` (`src/WebApp/Services/BasketState.cs:L78-L109`) → `OrderingService` POST with `x-requestid` → `OrdersApi.CreateOrderAsync` (`src/Ordering.API/Apis/OrdersApi.cs:L118-L168`) → MediatR pipeline (validate → transaction → handler) → `Order` aggregate ctor raises domain events → outbox saves `OrderStartedIntegrationEvent` → RabbitMQ → Basket.API deletes the basket (`src/Basket.API/IntegrationEvents/EventHandling/OrderStartedIntegrationEventHandler.cs:L10-L15`). The full trace with a step table is in [01-codebase-cartography/05-key-flows.md](01-codebase-cartography/05-key-flows.md).

Pause-and-predict before you look: *when you place an order, who empties your basket — the WebApp or the Basket service?* (Both try. `BasketState.CheckoutAsync:L108` calls delete directly, AND the integration event handler deletes it. Ask yourself why both exist — that's a real interview question about at-least-once delivery.)

## 4. One small safe change

Change the catalog page size default. Find `PaginationRequest` (in `src/Catalog.API/Model/`) and change the default page size (e.g., 10 → 12), or simply change a `WithSummary` string in `src/Catalog.API/Apis/CatalogApi.cs:L23`. Rebuild, refresh, observe. Then revert with `git checkout -- .`. The point is proving to yourself that the loop *edit → run → observe* works before attempting anything real.

## 5. One test to run

`dotnet test tests/Ordering.UnitTests/Ordering.UnitTests.csproj` (**inferred**). Then open `tests/Ordering.UnitTests/Domain/OrderAggregateTest.cs` and read the first three tests — they exercise `OrderItem` invariants (negative units throw an `OrderingDomainException`). Find the production code that throws (in `OrderItem.cs` next to `Order.cs`).

## 6. Teach-back (the interview rep)

Stand up, no notes, 3 minutes: *"Walk me through what happens when a user clicks Place Order in eShop."* You must mention: the request-id header (idempotency), the MediatR pipeline (validation, transaction), the aggregate raising domain events, the outbox (why events and DB writes must commit together), RabbitMQ fan-out, and at least one consumer (basket deletion or stock validation). Record yourself. If you said "and then it just publishes an event" without saying *why the outbox exists*, do it again.

## What the fast path skips

Identity/OIDC internals, the mobile YARP proxy, Webhooks.API and WebhookClient, the MAUI apps (`ClientApp`, `HybridApp`), AI semantic search, the order state machine's later stages (stock confirmation → payment → paid), and all testing infrastructure. All covered in the numbered modules.

**Next:** [01-codebase-cartography/05-key-flows.md](01-codebase-cartography/05-key-flows.md) — or if you have an interview looming, [08-interview-prep/07-two-week-cram-plan.md](08-interview-prep/07-two-week-cram-plan.md).
