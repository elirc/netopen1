# Verification Log

Running log of what was inspected while building this curriculum. Every code claim in these docs traces back to a file read listed here. Date: 2026-07-16.

## Conventions
- **Read (full)** — file opened and read end to end; line anchors written from that read.
- **Read (partial)** — only listed ranges inspected.
- **Listed** — directory contents enumerated, files not opened.
- **Not verified** — claim marked as *inferred* in the docs.

## Commands run

| Command | Result |
| --- | --- |
| `ls` of repo root, `cat eShop.slnx` | OK — 19 src projects, 5 test projects, slnx + slnf solution files |
| Directory listings of `src/*` and `tests/*` subfolders | OK |
| `grep -n` on validators, Identity `Config.cs`, PaymentProcessor handler | OK |
| `dotnet build` / `dotnet test` / `dotnet run` | **NOT run** — all build/run/test commands in these docs are marked *inferred* from README.md, ci.yml, and project files |

## Files read (full) — line anchors valid as of this log

- `src/eShop.AppHost/Program.cs` (116 lines) — Aspire orchestration, all resources and wiring
- `src/Catalog.API/Program.cs` (25), `src/Catalog.API/Apis/CatalogApi.cs` (423), `src/Catalog.API/Extensions/Extensions.cs` (52)
- `src/Basket.API/Program.cs` (15), `src/Basket.API/Grpc/BasketService.cs` (112), `src/Basket.API/Repositories/RedisBasketRepository.cs` (57), `src/Basket.API/Extensions/Extensions.cs` (29)
- `src/Ordering.API/Apis/OrdersApi.cs` (186)
- `src/Ordering.API/Application/Commands/CreateOrderCommandHandler.cs` (72), `IdentifiedCommandHandler.cs` (106)
- `src/Ordering.API/Application/Behaviors/TransactionBehavior.cs` (65), `ValidatorBehavior.cs` (38)
- `src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs` (187)
- `src/Ordering.Infrastructure/OrderingContext.cs` (116), `MediatorExtension.cs` (22)
- `src/EventBusRabbitMQ/RabbitMQEventBus.cs` (322)
- `src/IntegrationEventLogEF/Services/IntegrationEventLogService.cs` (92)
- `src/Basket.API/IntegrationEvents/EventHandling/OrderStartedIntegrationEventHandler.cs` (17)
- `src/Catalog.API/IntegrationEvents/EventHandling/OrderStatusChangedToAwaitingValidationIntegrationEventHandler.cs` (35)
- `src/OrderProcessor/Services/GracePeriodManagerService.cs` (96)
- `src/PaymentProcessor/IntegrationEvents/EventHandling/OrderStatusChangedToStockConfirmedIntegrationEventHandler.cs` (34, via grep -n full output)
- `src/WebApp/Program.cs` (35), `src/WebApp/Extensions/Extensions.cs` (125), `src/WebApp/Services/BasketState.cs` (173)
- `src/WebApp/Components/Pages/Checkout/Checkout.razor` (131)
- `src/eShop.ServiceDefaults/AuthenticationExtensions.cs` (57)
- `tests/Catalog.FunctionalTests/CatalogApiFixture.cs` (59)
- `README.md` (143), `ci.yml` (46), `package.json` (18)

## Files read (partial)

- `src/Ordering.API/Application/Validations/CreateOrderCommandValidator.cs` — RuleFor lines L6–L16 via grep
- `src/Identity.API/Configuration/Config.cs` — ApiScopes L18–L24, Client blocks at L44, L76, L112, L144, L159, L174 via grep
- `tests/Ordering.UnitTests/Domain/OrderAggregateTest.cs` — first 60 lines (MSTest attributes, OrderItem tests)

## Directories listed only (not opened)

- `src/Identity.API/Quickstart`, `src/Identity.API/Views` (Duende IdentityServer UI — treated as vendored/template code, excluded from teaching examples)
- `src/Webhooks.API`, `src/WebhookClient` (structure known from AppHost wiring only)
- `src/ClientApp`, `src/HybridApp` (MAUI clients — out of curriculum scope)
- `src/WebAppComponents`, `src/OrderProcessor/Extensions`, `src/Ordering.API/Application/Queries`, `src/Ordering.API/Application/DomainEventHandlers`, `src/Ordering.Infrastructure/Idempotency`, `src/Ordering.Infrastructure/Migrations`
- `e2e/` — Playwright spec filenames only (AddItemTest, BrowseItemTest, RemoveItemTest, login.setup)

## Addendum — 2026-07-16 (later session, ADR work in `fabledoc2/`)

- `src/Ordering.API/Extensions/Extensions.cs` (61 lines) — read full. Confirms MediatR behavior registration order Logging → Validator → Transaction (L39-L41), DbContext pooling disabled with explanatory comment (L12-L18), `AddMigration<OrderingContext, OrderingContextSeed>` (L21), event bus subscriptions (L53-L60).
- `src/Ordering.API/Application/Queries/OrderQueries.cs` (53 lines) — read full. **Resolves risk R5: `GetOrderAsync(int id)` has no user/ownership filter (L6-L14) — IDOR confirmed** (any authenticated caller can fetch any order by id via `OrdersApi.cs:L80-L91`). `GetOrdersFromUserAsync` does filter by `Buyer.IdentityGuid` (L40). Also confirms CQRS-lite: query side reuses the EF `OrderingContext` and hand-maps DTOs — no Dapper/separate read store.

## Known uncertainties / not covered

- **Runtime behavior not observed.** Nothing here was executed; all flow descriptions are static reads of code. Docker/Aspire startup, dashboard behavior, and seeding behavior are described from code + README, not observation.
- **Ordering domain event handlers** (`src/Ordering.API/Application/DomainEventHandlers/`) referenced by name from directory listing and from `Order.cs` event types; individual handler bodies not read. Claims about them are labeled *inferred*.
- **Webhooks flow** described from AppHost wiring and directory names only.
- **Identity.API** treated as mostly-vendored Duende IdentityServer; only `Configuration/Config.cs` grepped.
- **Migrations content** (`src/Ordering.Infrastructure/Migrations`, Catalog equivalents) not read.
- **`Program.Testing.cs`** files in Catalog.API and Ordering.API noted but not read (they exist to expose `Program` to WebApplicationFactory — *inferred*, standard pattern).
- Line numbers were confirmed at read time on 2026-07-16 against a clean working tree at commit `9b4f943`. If the repo has moved, re-verify before quoting.
