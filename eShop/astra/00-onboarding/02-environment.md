# Set up a reproducible environment

Run the commands below from the eShop Git root. PowerShell is the main shell used in this course; .NET and Git commands also work in other shells.

## Read configuration before installing tools

[global.json](../../global.json) requests SDK `10.0.100`, allows prereleases, and uses `latestFeature`. A compatible installed 10.0 feature band can be selected; a .NET runtime alone is insufficient. AppHost is pinned separately to Aspire SDK `13.2.0` in [its project](../../src/eShop.AppHost/eShop.AppHost.csproj). This is a project SDK dependency; do not assume an old instruction to install an Aspire workload applies.

Install a compatible .NET 10 SDK using the [official download page](https://dotnet.microsoft.com/en-us/download/dotnet/10.0). Use an editor or IDE that supports the selected SDK. The CLI is the baseline for this course. The [SDK selection documentation](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json) explains roll-forward behavior.

Also install Git and Docker Desktop, and start Docker with Linux containers available. Node and npm are needed when you reach browser tests and Markdown linting. Follow the checked-in lockfile for JavaScript dependencies. Mobile workloads are optional and are excluded from the main learning path.

## Inspect first

```powershell
git rev-parse --show-toplevel
git status --short
dotnet --list-sdks
dotnet --version
dotnet --info
docker version
docker info
node --version
npm.cmd --version
```

On Windows, `npm.cmd` avoids PowerShell script execution-policy issues. On macOS/Linux use `npm` and `npx` instead of the `.cmd` names.

Record versions and outcomes in a local copy of the [onboarding template](../04-templates/onboarding-log.md). Success means the SDK resolves inside the repository and Docker reports a working server. Seeing `docker.exe` in PATH only proves that its client is installed.

## Restore and build

```powershell
dotnet restore eShop.Web.slnf
dotnet build eShop.Web.slnf --no-restore
```

Restore downloads the dependencies described by project files, [Directory.Packages.props](../../Directory.Packages.props), and [nuget.config](../../nuget.config). Build compiles the selected web projects and tests. The full solution also includes mobile projects; start with the web filter to avoid unrelated platform workloads.

The root [Directory.Build.props](../../Directory.Build.props) enables warnings as errors. Tests have their own [build props](../../tests/Directory.Build.props), so inspect effective project settings rather than assuming identical inheritance; the authoring build retained package advisories as warnings in test projects. Do not turn off warning policies to finish onboarding. Capture the first actionable diagnostic and check whether it exists before your change.

Build output uses the artifacts layout configured in that same file. Do not assume every assembly lives under a project's conventional `bin/Debug` directory.

## Run a first focused test

```powershell
dotnet test --project tests/Ordering.UnitTests/Ordering.UnitTests.csproj
dotnet test --project tests/Basket.UnitTests/Basket.UnitTests.csproj
```

These projects use MSTest and NSubstitute. They are the first test layer to try without a running application. First-time restore and build still require their normal dependencies. The repository selects Microsoft.Testing.Platform, so use named `--project` and `--solution` options. Framework-specific filtering options differ; inspect help for the chosen project before adding filters. See [Microsoft's MTP command reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test-mtp).

Do not use `--no-build` after editing code unless you have already rebuilt the same configuration.

## HTTPS and application startup

```powershell
dotnet dev-certs https --check
dotnet dev-certs https --trust
dotnet run --project src/eShop.AppHost/eShop.AppHost.csproj
```

Trusting a development certificate can prompt your operating system. It is for local HTTPS. Follow the OS-specific message if trust is not automatic. Routine setup does not require cleaning all existing development certificates.

AppHost starts infrastructure and application resources. Leave its terminal running while browsing. The first run may need container image downloads and database initialization. Open the dashboard login URL printed by this process, then the `webapp` endpoint labeled Online Store. Dashboard ports and login tokens are runtime values, not constants to copy into documentation.

## What you can defer

Both optional AI flags are false in [AppHost Program.cs](../../src/eShop.AppHost/Program.cs). The main course does not require AI credentials, an AI provider, Azure deployment, or a MAUI emulator. Work locally with sample data.

For Playwright installation, environment variables, and individual test projects, use [the commands reference](../03-reference/commands.md) when you reach stage 3.

## Setup is complete when

- You can explain which SDK was selected and why.
- The web build and two unit test commands have recorded outcomes.
- AppHost and the store run, or a specific runtime blocker is documented separately.
- You can locate the home page, catalog endpoint, and a test without guessing.
