# Boundaries and Layers

A **boundary** is a line where you can change one side without asking the other side's permission — as long as you honor the **contract** at the line. Layers are boundaries stacked vertically inside one service.

## The two boundary kinds in eShop

**Service boundaries (horizontal):** WebApp | Catalog | Basket | Ordering | Identity | Webhooks | workers. Contracts: REST routes, `basket.proto`, integration event classes, OIDC scopes. Enforced by: separate processes, separate databases.

**Layer boundaries (vertical, strongest in Ordering):**

| Layer | Project | Owns | Must not own | Evidence it's enforced |
| --- | --- | --- | --- | --- |
| API | `Ordering.API/Apis` | HTTP shapes, headers, status codes | business rules | `OrdersApi.cs` only builds commands and reads results |
| Application | `Ordering.API/Application` | orchestration, validation, transactions, event translation | domain invariants | handlers call aggregate methods, never set status fields |
| Domain | `Ordering.Domain` | invariants, state machine, domain events | HTTP/EF/RabbitMQ | its `.csproj` references neither EF nor ASP.NET (check it) |
| Infrastructure | `Ordering.Infrastructure` | EF mappings, repositories, idempotency store | deciding anything | `OrderingContext` + `EntityConfigurations/` |

## Boundaries done well (steal these)

1. **Domain purity.** `Ordering.Domain` compiles without EF Core. Persistence adapts to the domain via `EntityConfigurations/` (private field mapping for `_orderItems`), not vice versa. This is the Dependency Inversion everyone claims and few ship.
2. **Prices never trusted from the client.** Basket stores only (ProductId, Quantity) (`BasketService.cs:L93-L110`); the WebApp re-fetches prices from Catalog (`BasketState.cs:L117-L149`); the Order snapshots price at creation (`OrderItem`). Three boundaries each doing their part of one security property.
3. **Async-first coupling.** Ordering never calls Catalog. Stock validation happens via events (Flow 4). If Catalog is down, orders queue up in AwaitingValidation instead of checkout throwing 500s.
4. **ServiceDefaults as a shared kernel with discipline** — only cross-cutting infra (OTel, health, auth defaults), no business types (`src/eShop.ServiceDefaults/`).

## Boundary leaks (real, findable, discussable)

1. **OrderProcessor reads Ordering's database with raw SQL** — `GracePeriodManagerService.cs:L69-L74` queries `ordering.orders` directly, including string-matching the status `'Submitted'`. If Ordering renames a column or changes the enum-to-string conversion, OrderProcessor breaks *at runtime*. Tradeoff taken: avoids adding a "list stale orders" API. Verdict: deliberate, documented-by-code, still a leak. Interview gold.
2. **EF entities as wire contracts in Catalog** — `CatalogApi.cs:L158` returns `CatalogItem` (with stock thresholds, embedding metadata) straight to any caller. UI shape = DB shape: adding a column leaks it to the world by default.
3. **WebApp knows Ordering's request record shape** — `CreateOrderRequest` is *duplicated* in `WebApp/Services/BasketState.cs:L158-L172` and `Ordering.API/Apis/OrdersApi.cs:L171-L185`. Two copies of one contract, kept in sync by hand. Classic drift risk (count the fields in both — 14 today).
4. **The WebApp subscribes to the message bus** (`WebApp/Extensions.cs:L43-L51`). Pragmatic for live order-status UI, but it makes a *frontend* a bus consumer with a durable queue — deployment and scaling now care.

## What a junior misses vs what a senior checks

Junior: "the folders are organized nicely." Senior: opens the `.csproj` files and checks the *reference graph* (does Domain reference Infrastructure? — here, no), then greps for the duplicated contract shapes (leak #3), then asks who else touches each database (leak #1).

Interview angle: "Tell me about a well-drawn boundary and a leaky one in a system you know." You now have two of each with file:line evidence. That answer, with anchors, is a mid-to-senior differentiator.

Drill: draw the allowed-dependency graph for Ordering's four layers, then verify it against the actual `<ProjectReference>` entries in the four `.csproj` files.
Self-grade — Basic: graph matches references. Solid: you caught that Ordering.API references Infrastructure (composition root has to). Strong: you can explain *why* the composition root is the one place allowed to see everything.
