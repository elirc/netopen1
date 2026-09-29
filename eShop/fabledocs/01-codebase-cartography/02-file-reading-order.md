# File Reading Order

28 files. Read in order; each row says what to look for and what to skip. Junior path = rows marked J. Mid = J+M. Senior = all.

| # | Path | Why it matters / what to look for | Ignore |
| --- | --- | --- | --- |
| 1 J | `README.md` | Run instructions; what's optional (OpenAI, azd) | Azure deploy section |
| 2 J | `src/eShop.AppHost/Program.cs` | The system diagram in code. Note `WaitFor` ordering and the cyclic identity wiring (L96-L101) | OpenAI/Ollama blocks |
| 3 J | `src/eShop.ServiceDefaults/Extensions.cs` | What *every* service gets: OTel, health `/health` + `/alive`, service discovery, resilience handlers | fine details |
| 4 J | `src/Catalog.API/Program.cs` | How thin a service entrypoint is (25 lines) | — |
| 5 J | `src/Catalog.API/Apis/CatalogApi.cs` | Minimal APIs, versioned groups, `TypedResults`, pagination (L124-L159) | the image MIME switch |
| 6 J | `src/Catalog.API/Model/CatalogItem.cs` | The entity doubling as wire contract; stock fields; `Embedding` | — |
| 7 J | `src/Catalog.API/Extensions/Extensions.cs` | DI registration, pgvector, `AddMigration` auto-migate+seed (L23-L24) | AI config |
| 8 J | `src/WebApp/Program.cs` | Blazor Server startup; antiforgery; image forwarder (L32) | — |
| 9 J | `src/WebApp/Extensions/Extensions.cs` | Typed clients per backend; OIDC config; the WebApp's own event-bus subscriptions (L43-L51) | AI block |
| 10 J | `src/WebApp/Services/BasketState.cs` | Scoped state, cached-Task memoization (L117-L119), checkout orchestration | — |
| 11 J | `src/WebApp/Components/Pages/Checkout/Checkout.razor` | Blazor form validation; `[Authorize]`; SSR form binding | CSS |
| 12 J | `src/Basket.API/Proto/basket.proto` | A contract-first API; compare with REST | — |
| 13 J | `src/Basket.API/Grpc/BasketService.cs` | Auth at method level; proto↔model mapping | — |
| 14 J | `src/Basket.API/Repositories/RedisBasketRepository.cs` | Redis as document store; source-gen JSON (L51-L56) | UTF-8 key comment |
| 15 M | `src/Ordering.API/Apis/OrdersApi.cs` | `x-requestid`, command wrapping, CC masking (L140) | logging boilerplate |
| 16 M | `src/Ordering.API/Application/Behaviors/ValidatorBehavior.cs` + `TransactionBehavior.cs` | The MediatR pipeline = middleware for commands | LoggingBehavior |
| 17 M | `src/Ordering.API/Application/Commands/CreateOrderCommandHandler.cs` | Both halves: business handler + identified (idempotent) wrapper | — |
| 18 M | `src/Ordering.API/Application/Commands/IdentifiedCommandHandler.cs` | The idempotency mechanism; the catch-all at L99-L102 | switch block |
| 19 M | `src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs` | Aggregate root: encapsulated collection, guarded transitions, domain events | — |
| 20 M | `src/Ordering.Domain/SeedWork/Entity.cs` + `ValueObject.cs` | What "entity" and "value object" mean mechanically (identity vs structural equality) | — |
| 21 M | `src/Ordering.Infrastructure/OrderingContext.cs` | `SaveEntitiesAsync` dispatch-then-save (L47-L62); transaction API | Debug.WriteLine |
| 22 M | `src/EventBusRabbitMQ/RabbitMQEventBus.cs` | Publish path, consume path, ack-on-error (L177-L180), retry pipeline (L302-L320) | telemetry plumbing on first pass |
| 23 M | `src/IntegrationEventLogEF/Services/IntegrationEventLogService.cs` | The outbox table's lifecycle: NotPublished → InProgress → Published/Failed | reflection ctor |
| 24 M | `src/OrderProcessor/Services/GracePeriodManagerService.cs` | `BackgroundService` pattern; the raw-SQL boundary trespass | — |
| 25 S | `src/eShop.ServiceDefaults/AuthenticationExtensions.cs` | JWT config; `ValidateAudience=false` (L49); `sub` claim mapping removal | — |
| 26 S | `src/Identity.API/Configuration/Config.cs` | Client/scope registrations; which client gets which scope | Quickstart UI folder |
| 27 S | `tests/Catalog.FunctionalTests/CatalogApiFixture.cs` | Aspire-hosted integration testing — real Postgres container per fixture | — |
| 28 S | `src/eShop.AppHost/Extensions.cs` | YARP mobile-bff route table; OpenAI/Ollama resource wiring | — |

Deliberately excluded from teaching examples: `src/Identity.API/Quickstart/**` and `Views/**` (vendored Duende template code), `src/ClientApp/**` (MAUI, large and stylistically older), generated migrations under `src/Ordering.Infrastructure/Migrations/`.

Habit to build (transferable): for each file, before scrolling, predict *what you'll find* from the name and location; after reading, write one sentence you could say in a code review about it. Reading without prediction is just scrolling.
