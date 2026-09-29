# Runtime & Tooling Map

## Toolchain

| Concern | Tool | Where configured |
| --- | --- | --- |
| SDK version | .NET 9 (pinned) | `global.json` |
| Package versions | Central Package Management | `Directory.Packages.props` (one version list for all projects) |
| Shared build props | `Directory.Build.props` / `.targets` | repo root |
| Solution | `eShop.slnx` (full), `eShop.Web.slnf` (web filter, used by CI — `ci.yml:L44`) | root |
| Orchestration | .NET Aspire AppHost | `src/eShop.AppHost/` |
| e2e | Playwright (TypeScript) | `playwright.config.ts`, `e2e/`, deps in `package.json` |
| CI | Azure Pipelines 1ES template; **build only, no tests in CI** (`ci.yml`) | `ci.yml` |

Commands (all **inferred** — see verification log):

```
dotnet run --project src/eShop.AppHost/eShop.AppHost.csproj   # run everything (Docker required)
dotnet build eShop.Web.slnf                                    # what CI does
dotnet test tests/Ordering.UnitTests/Ordering.UnitTests.csproj # fast, no containers
dotnet test tests/Catalog.FunctionalTests/...                  # spins real Postgres via Aspire
npm install && npx playwright test                             # e2e (system must be running; see playwright.config.ts)
```

## Runtime boundaries

| Boundary | Runs where | Consequences |
| --- | --- | --- |
| Blazor **Server** components | on the server; browser holds a SignalR connection ("circuit") | UI state like `BasketState` is *server memory per circuit* (`WebApp/Extensions.cs:L23` — scoped). A dropped connection = lost unsent state. No API keys ever reach the browser. |
| APIs | Kestrel, containerized by Aspire in dev | service-to-service URLs are logical names (`https+http://catalog-api`) resolved by service discovery |
| Workers | headless hosts (`OrderProcessor`, `PaymentProcessor`) | no HTTP surface except health; all input via RabbitMQ or DB polling |
| Infra | Docker containers (Postgres w/ pgvector image, Redis, RabbitMQ — `eShop.AppHost/Program.cs:L7-L13`) | `ContainerLifetime.Persistent` keeps data between runs |
| MAUI clients | device; talk to `mobile-bff` YARP proxy (`Program.cs:L60-L62`) | mobile never talks to services directly |

## Configuration surfaces (no secrets here — sample app)

- Aspire injects connection strings and service URLs as env vars via `WithReference(...)` — you will find almost no hardcoded URLs in service code.
- `Identity__Url` env var (`AppHost/Program.cs:L33,L44,L57`) → consumed by `AuthenticationExtensions.cs:L22-L35`.
- Per-service `appsettings.json` for options like `CatalogOptions`, `BackgroundTaskOptions` (grace period seconds), `PaymentOptions.PaymentSucceeded` (the payment simulator switch).
- `ESHOP_USE_HTTP_ENDPOINTS=1` forces HTTP everywhere for Playwright CI (`AppHost/Program.cs:L108-L115`).
- Known hardcoded sample values to *not* imitate: OIDC `ClientSecret = "secret"` (`WebApp/Extensions.cs:L78`), test card data (`BasketState.cs:L100-L103`).

## Health & observability defaults

Every service calls `AddServiceDefaults()` / `MapDefaultEndpoints()` (see any `Program.cs`), which wires OpenTelemetry traces/metrics/logs, `/health` and `/alive` endpoints, service discovery, and standard HTTP resilience. The event bus adds message-level tracing with W3C context propagation through RabbitMQ headers (`RabbitMQEventBus.cs:L86`, `:L144-L146`) — so a checkout trace continues *across the queue*. This is the part of eShop most worth stealing for any real system.

Interview angle: "How would you trace a request across services and a message queue?" — describe exactly this: inject trace context into message headers on publish, extract and continue the activity on consume.
