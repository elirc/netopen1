# Your first day

Your first job is to make the application explainable and repeatable. Do not begin by changing a service you cannot yet run or locate.

## The first 90 minutes

1. Open the directory containing `global.json`. Run `git rev-parse --show-toplevel` and `git status --short`. Record the current branch and any pre-existing changes. Those changes may belong to another person.
2. Read [CONTRIBUTING.md](../../CONTRIBUTING.md) and [CODE-OF-CONDUCT.md](../../CODE-OF-CONDUCT.md). Small corrections can go directly into a PR; larger upstream suggestions begin with a discussion.
3. Read [global.json](../../global.json), [eShop.Web.slnf](../../eShop.Web.slnf), and [AppHost Program.cs](../../src/eShop.AppHost/Program.cs). Find the SDK selector, the web project list, and the resource called `webapp`.
4. Follow [environment setup](02-environment.md). Record each command and its actual result, including failures.
5. Find the code for the home page and one existing test. Start with [Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor) and [BrowseItemTest.spec.ts](../../e2e/BrowseItemTest.spec.ts).

Your first note should answer: what does this application sell, which project shows the page, which project owns product data, and what infrastructure is needed to browse it?

## The rest of day one

Build the web solution filter. If the build succeeds, launch AppHost and follow the resource link to the online store. Browse a product, inspect its URL, and locate the matching Razor page. If startup fails, collect the first relevant resource error and use the troubleshooting guide. A setup failure is a useful finding when another developer can reproduce it.

Draw three boxes: browser, WebApp, Catalog.API. Add PostgreSQL underneath Catalog.API. Explain why a browser request to the home page does not require browser JavaScript to call every service directly: server-rendered components can call a service from the WebApp process.

By the end of the day, complete ASTRA-001 and begin ASTRA-002. If Docker is unavailable, continue with code reading and unit tests, and mark the runtime evidence pending. Do not mark startup verified because source inspection looks convincing.

## Your first week

| Day | Focus | Evidence |
| --- | --- | --- |
| 1 | Setup and first run | Version report, command outcomes, first page |
| 2 | Repository map | Project responsibilities and a request trace |
| 3 | Contribution workflow | Small branch, limited diff, draft PR text |
| 4 | Review and correction | One review response and a refined change |
| 5 | Explain and reflect | Five-minute demo and three learning gaps |

Use this structure flexibly; waiting for a download is not a reason to stop reading code.

## Ask questions that others can answer

A useful help request contains the task, exact command and working directory, observed error, expected result, and one attempted diagnosis. For example: “Building the web filter from the Git root fails during package restore. The SDK reports 10.0.302. The first NU1301 points to a feed in nuget.config. Docker is running, but I have not reached application startup.”

Keep one open question per paragraph. Explain what evidence would resolve it. Avoid posting entire console dumps containing dashboard login links or credentials.

## Check yourself

- Why are the parent workspace and Git root different here?
- Which file wins when README instructions and the selected SDK disagree?
- Can a green unit test prove that PostgreSQL migrations run?
- What is the smallest useful contribution you can explain today?

If the last answer is a documentation correction, that is an appropriate first contribution. Continue with [run and debug](03-run-and-debug.md) after setup.
