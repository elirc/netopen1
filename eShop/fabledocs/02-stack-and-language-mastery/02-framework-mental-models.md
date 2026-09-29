# Framework Mental Models

Four frameworks, two ideas: **pipelines of decorators** (ASP.NET middleware, MediatR behaviors, HttpClient handlers) and **change-tracked object graphs** (EF Core, Blazor's render tree). Hold those two and everything below is a variation.

## ASP.NET Core Minimal APIs

Model: route table → endpoint delegate → typed result. No controllers; handlers are static methods with **parameter binding by convention**: route values, query, headers (`[FromHeader(Name = "x-requestid")]`, `OrdersApi.cs:L23`), body, DI services, and `[AsParameters]` bundles (`CatalogServices` at `CatalogApi.cs:L118` — a struct of dependencies, cutting parameter noise).
Where it's used well: versioned route groups (`CatalogApi.cs:L15-L18`), `TypedResults` unions as compile-checked contracts (Q6 in the deep-dive).
Sharp edges: binding failures produce automatic 400s you didn't write (surprise contract); static handlers mean no constructor injection — deps must be parameters, which is why `[AsParameters]` exists.
Pitfall checklist: does every endpoint declare all its status codes? Is auth applied per-group or forgotten per-endpoint (Catalog's write endpoints — R4)?
React/Express parallel: closest to Express routing, but with real DI and typed binding.

## Blazor Server

Model: components render **on the server**; a SignalR connection ("circuit") ships DOM diffs down and events up. State = server memory per circuit.
- Rendering: component → render tree → diff → patch. Same diffing idea as React's virtual DOM; the difference is *where* it runs and that the wire carries UI diffs, not data.
- State placement: `BasketState` is circuit-scoped DI (`WebApp/Extensions.cs:L23`) — the Blazor answer to React context + a client cache. Change notification is manual pub/sub (`NotifyOnChange`, `BasketState.cs:L26-L31`) — the repo hand-rolls what React gets from state setters.
- Forms: `EditForm` + `DataAnnotationsValidator` + `ValidationMessageStore` for custom errors (`Checkout.razor:L12-L13, L118-L126`); `[SupplyParameterFromForm]` (L68-L69) is SSR form binding — this page works as a *server-rendered post*, enhanced (`Enhance` attr, L12).
- Lifecycle: `OnInitialized` (L74-L83) runs on first render — the `Info is null` check exists because SSR + enhanced nav can re-enter.
Sharp edges: circuit loss = state loss (design for it); `StateHasChanged` needed when data changes outside an event handler (the order-status live updates do exactly this — bus event → component refresh, see `OrdersRefreshOnStatusChange.razor`); scoped ≠ singleton mistakes leak one user's state to all (imagine `BasketState` registered singleton — that's the horror story to tell).
Interview angle: even if the target shop uses React, "explain Blazor Server to a React dev" is a *great* answer to "teach me something" — render/commit split, reconciliation, and state placement are the same questions in both.

## MediatR (as used in Ordering)

Model: in-process message bus: `Send` one request → one handler, through ordered behaviors; `Publish` one notification → N handlers.
Used for: commands (`Ordering.API/Application/Commands/`), domain events (`MediatorExtension.cs`), pipeline concerns (`Behaviors/`).
Sharp edges: indirection tax — "who handles this?" needs tooling (grep `IRequestHandler<CreateOrderCommand`); behaviors' registration order is invisible at call sites; overuse turns simple method calls into ceremony (Catalog's plain services are the counter-example — see pattern card 5).

## EF Core

Model: `DbContext` = unit of work + identity map + change tracker; LINQ → expression tree → SQL.
Used well here: private-field collection mapping keeps the aggregate encapsulated (`Order.cs:L31-L33` + `EntityConfigurations/OrderEntityTypeConfiguration.cs`); owned types for `Address`; change tracking driving business logic (price-change detection, `CatalogApi.cs:L345-L347`); execution strategies + explicit transactions (`TransactionBehavior.cs:L32-L38`).
Sharp edges: N+1 via lazy navigation (this repo eager-loads with `Include`, `CatalogApi.cs:L183`); tracking overhead on read paths (no `AsNoTracking` — ticket 7); DbContext thread affinity (never share across parallel awaits); migrations at startup (R10).
Node parallel: Prisma/TypeORM are the same idea minus the change tracker; explain `IsModified` to a Prisma user and you understand it yourself.

Drill: for each framework, name its "unit of isolation" (request / circuit / handler scope / DbContext) and one bug that occurs when you confuse two of them. Self-grade — Strong: your bug examples are all real possibilities in this repo with anchors.
