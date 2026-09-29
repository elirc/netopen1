# Tooling & Build System

## The reproducibility stack

| Layer | File | What it pins |
| --- | --- | --- |
| SDK | `global.json` | exact .NET SDK band — everyone (and CI) builds with the same compiler |
| Packages | `Directory.Packages.props` | **central package management**: one `<PackageVersion>` list; project files say `<PackageReference Include="X" />` with no version. Kills version skew across 19 projects |
| Build props | `Directory.Build.props` / `.targets` | shared MSBuild settings (TFM, nullable, analyzers) inherited by every project |
| Feeds | `nuget.config` | package sources (this repo pulls preview feeds for Aspire — check it before wondering why a restore fails outside) |
| JS deps | `package.json` + `package-lock.json` | Playwright toolchain only |

Transferable: every ecosystem has these five layers (Node: `.nvmrc` / lockfile / workspaces root / `.npmrc`). When a build works on one machine and not another, walk this table top to bottom.

## Aspire as the dev tool

`dotnet run --project src/eShop.AppHost/eShop.AppHost.csproj` replaces: docker-compose file, 7 terminal windows, connection-string sharing, and "which service do I start first" (`WaitFor` chains, `eShop.AppHost/Program.cs:L32-L49`). The dashboard gives logs/traces/metrics per resource. Container lifetimes are `Persistent` for stateful infra (L9, L13) so your data survives restarts.

Two files worth knowing exist: `Program.Testing.cs` in Catalog.API and Ordering.API — partial `Program` classes making the app visible to `WebApplicationFactory` (*inferred* — standard pattern; verify). And `eShop.Web.slnf` — a solution *filter*; CI builds only the web slice (`ci.yml:L44`), excluding MAUI apps that need mobile workloads.

## Test toolchain

- Mixed frameworks by history: **MSTest** in Ordering.UnitTests (`[TestClass]`, `OrderAggregateTest.cs:L6`), **xUnit** in Catalog.FunctionalTests (`IAsyncLifetime`, `CatalogApiFixture.cs:L10`). Recent commit "Use latest xUnit, MSTest + move to MTP" (git log) — MTP = Microsoft.Testing.Platform, the new runner. Lesson: real repos are heterogeneous; match the *local* convention when adding tests.
- Functional tests boot **real infrastructure**: the fixture builds a mini Aspire app with a real pgvector Postgres container (`CatalogApiFixture.cs:L17-L25`), then points `WebApplicationFactory` at it (L27-L37). No mocked DB. Slower, honest.
- e2e: Playwright TS. `playwright.config.ts` at root; `ESHOP_USE_HTTP_ENDPOINTS=1` (`eShop.AppHost/Program.cs:L108-L115`) exists purely to make CI's Playwright life easier — an example of *test hooks living in production composition code*, a tradeoff worth an opinion.

## Commands (status per verification log)

```
dotnet build eShop.Web.slnf              # inferred; what CI runs
dotnet test tests/<Project>/<Project>.csproj   # inferred; functional tests need Docker
dotnet ef migrations add <Name> --startup-project Ordering.API --context OrderingContext
                                         # verified-as-documented: comment at OrderingContext.cs:L5-L9
npm i && npx playwright test             # inferred; app must be running
```

Interview angle: "How do you keep 19 projects' dependencies consistent?" (CPM), "How do you test against a real database in CI?" (containers-per-fixture — compare Testcontainers), "What's in your local dev loop?" (Aspire story). All three come up in .NET loops; all three now have concrete answers.

Drill: open `Directory.Packages.props` and find the version of MediatR, EF Core, and the RabbitMQ client. Then open one `.csproj` and confirm the version-less reference style. Two minutes; you now understand CPM better than by reading any blog post.
