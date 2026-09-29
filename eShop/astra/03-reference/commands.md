# Commands and verification choices

Run from the **eShop Git root**, containing global.json. PowerShell examples use npm.cmd/npx.cmd; use npm/npx in other shells. Commands below are recipes; [verification.md](verification.md) records which were actually run when the course was authored.

## Find your bearings

```powershell
git rev-parse --show-toplevel
git status --short
git branch --show-current
git log -1 --oneline
rg --files src tests
rg -n 'GetAllItems|GetCatalogItems' src tests
```

Read status before editing. Use symbol search to find callers rather than guessing filenames.

## Build and start the web application

```powershell
dotnet --version
dotnet --list-sdks
docker info
dotnet restore eShop.Web.slnf
dotnet build eShop.Web.slnf --no-restore
dotnet run --project src/eShop.AppHost/eShop.AppHost.csproj
```

Ctrl+C stops the host process. Inspect persistent resources separately. The AppHost dashboard prints its current login URL; open the webapp resource from there.

## Choose a test project

```powershell
dotnet test --project tests/Ordering.UnitTests/Ordering.UnitTests.csproj
dotnet test --project tests/Basket.UnitTests/Basket.UnitTests.csproj
```

These are the first focused unit checks. For functional checks, start Docker first:

```powershell
dotnet test --project tests/Catalog.FunctionalTests/Catalog.FunctionalTests.csproj
dotnet test --project tests/Ordering.FunctionalTests/Ordering.FunctionalTests.csproj
```

For the web suite matching PR validation, build first and then run:

```powershell
dotnet build eShop.Web.slnf
dotnet test --solution eShop.Web.slnf --no-build --no-progress --output detailed
```

This repository chooses Microsoft.Testing.Platform in global.json. Do not copy VSTest positional project arguments or framework-specific filter syntax blindly. Inspect the selected runner's help:

```powershell
dotnet test --project tests/Ordering.UnitTests/Ordering.UnitTests.csproj --help
dotnet test --project tests/Catalog.FunctionalTests/Catalog.FunctionalTests.csproj --help
```

Use the actual supported filtering option for a focused run and record the discovered test count. The baseline web filter includes four test projects, not the mobile test project. A course-added project needs deliberate solution/filter registration.

## Browser dependencies and anonymous tests

```powershell
npm.cmd ci
npx.cmd playwright install chromium
$env:ESHOP_USE_HTTP_ENDPOINTS = '1'
npx.cmd playwright test --list
npx.cmd playwright test --project 'e2e tests without logged in'
```

The config's baseURL and webServer readiness URL are http://localhost:5045. ESHOP_USE_HTTP_ENDPOINTS=1 selects the local HTTP launch path in AppHost. The config starts AppHost when needed and may reuse an existing local server. If you already launched a conflicting HTTPS instance, stop that course instance before using this test mode.

The [Playwright web-server documentation](https://playwright.dev/docs/test-webserver) describes startup and reuse behavior. Configuration in this checkout remains the source for the actual port, timeout, and command.

## Logged-in browser tests

The following sample identity is used by the checked-in Playwright workflow for this local sample:

```powershell
$env:ESHOP_USE_HTTP_ENDPOINTS = '1'
$env:USERNAME1 = 'bob'
$env:PASSWORD = 'Pass123$'
npx.cmd playwright test --project 'e2e tests logged in'
```

Use only sample accounts in the local course instance. The setup project writes playwright/.auth/user.json; do not commit it. New specs must match a configured project or they will not run. Shared server-side basket state requires isolation even when browser contexts are separate.

To run the full configured browser suite and inspect its report:

```powershell
npx.cmd playwright test
npx.cmd playwright show-report
```

In PowerShell, clear course-specific variables when you finish:

```powershell
Remove-Item Env:ESHOP_USE_HTTP_ENDPOINTS -ErrorAction SilentlyContinue
Remove-Item Env:USERNAME1 -ErrorAction SilentlyContinue
Remove-Item Env:PASSWORD -ErrorAction SilentlyContinue
```

## Documentation and diff checks

From the repo root, use the checked-in Markdown configuration and a pinned one-off CLI so this check does not edit package.json:

```powershell
npx.cmd --yes markdownlint-cli@0.45.0 "astra/**/*.md"
python astra/tools/check_course.py
git diff --check
git status --short
```

The Python checker verifies this course's local links, story structure, IDs, prerequisite ordering, and index/tracker completeness. It does not replace Markdown lint or validate code examples by compiling them. Python is optional for reading the course and needed only for that checker.

For a contribution elsewhere, lint its actual Markdown path. The repository's Markdown workflow uses its own CLI installation; do not assume a passing course-only check validates unrelated pre-existing documents.

## Keep commands honest

A passed build is not a runtime smoke test. A passed unit project is not a functional test. A test file discovered by --list has not yet executed. Include exact command, working directory, result, and any relevant test count in your evidence.
