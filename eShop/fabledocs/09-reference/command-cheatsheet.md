# Command Cheatsheet

Status legend: **verified** = executed while writing these docs; **inferred** = derived from README/CI/config, not executed. (Per the verification log, no build/run/test command was executed in the authoring session — treat every runnable line below as inferred and promote to verified yourself.)

| Task | Command | Status |
| --- | --- | --- |
| Run everything (Docker must be running) | `dotnet run --project src/eShop.AppHost/eShop.AppHost.csproj` | inferred (README.md:L73-L80) |
| Aspire dashboard | URL printed at startup: `http://localhost:19888/login?t=…` | inferred (README) |
| Build (what CI builds) | `dotnet build eShop.Web.slnf` | inferred (ci.yml:L44) |
| Full solution build | `dotnet build eShop.slnx` | inferred (needs MAUI workloads for client apps — expect failures without them; prefer the slnf) |
| Unit tests (fast, no Docker) | `dotnet test tests/Ordering.UnitTests/Ordering.UnitTests.csproj` / `tests/Basket.UnitTests/...` | inferred |
| Functional tests (needs Docker) | `dotnet test tests/Catalog.FunctionalTests/Catalog.FunctionalTests.csproj` / `tests/Ordering.FunctionalTests/...` | inferred |
| Single test by name | `dotnet test <proj> --filter "FullyQualifiedName~Invalid_number_of_units"` | inferred (MTP/MSTest filter syntax — verify flag against the runner) |
| e2e deps | `npm install` | inferred (package.json) |
| e2e run (system must be up; HTTP mode helps) | `$env:ESHOP_USE_HTTP_ENDPOINTS=1` then run AppHost; `npx playwright test` | inferred (AppHost Program.cs:L108-L115, playwright.config.ts) |
| Add ordering migration | `dotnet ef migrations add <Name> --startup-project Ordering.API --context OrderingContext` (from `src/Ordering.Infrastructure/`) | verified-as-documented (comment at OrderingContext.cs:L5-L9) — not executed |
| Inspect Redis basket | `docker exec -it <redis> redis-cli` → `KEYS /basket/*` / `GET /basket/<sub>` | inferred |
| Inspect ordering DB | `docker exec -it <postgres> psql -U postgres -d orderingdb` → `SELECT "Id","OrderStatus" FROM ordering.orders;` | inferred (schema from OrderingContext.cs:L37, grace SQL) |
| Outbox backlog check | `SELECT "EventId","State","TimesSent" FROM "IntegrationEventLog" WHERE "State" <> 2;` (in catalogdb/orderingdb) | inferred (EventStateEnum ordering — verify enum values first) |
| Format | `dotnet format` | inferred (standard; .editorconfig present) |
| Chaos: poison a message | publish any subscribed event whose JSON contains `throw-fake-exception` | verified-in-code hook (RabbitMQEventBus.cs:L163-L166) |

Container names: find them via `docker ps` — Aspire generates suffixed names; don't hardcode.

Maintenance note: when you *run* one of these successfully, edit this file and flip its status to verified with the date. The cheatsheet is a living document; its value is the honesty of the status column.
