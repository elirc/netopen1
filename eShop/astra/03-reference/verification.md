# Sources, baseline, and verification

This course was authored against the local eShop checkout at commit `9b4f943`, titled “Update to Asp.Versioning to v10-preview2 (#980)”, on 2026-09-04. Story briefs describe either observed source behavior or explicitly proposed practice requirements. They are not upstream issues or completed implementations.

## Source-of-truth hierarchy

1. Checked-in project, runner, build, and workflow configuration for this checkout.
2. Executed source and tests for current behavior.
3. The repository README and contribution guide for intent and process, checked against configuration.
4. Official external references for general tool behavior.

The README still says .NET 9, while global.json selects .NET 10 and the web projects target net10.0. This course follows the configuration. Future learners should repeat the baseline inspection if the checkout changes.

## Local checks performed during authoring

| Check | Observed result | What it proves |
| --- | --- | --- |
| Git root and baseline | eShop is the Git repository inside netopen1; baseline 9b4f943 | Where commands and source links resolve |
| SDK selection | dotnet --version: 10.0.302 | A compatible SDK resolved from this repository |
| Docker server | docker info reported server 29.2.1 | The Docker server responded |
| JavaScript tools | Node v22.16.0; npm 10.9.2 | Tools were available |
| Web build | dotnet build eShop.Web.slnf --nologo -v minimal: passed, 0 errors | The unmodified web source built in this environment |
| Build diagnostics | 44 warning instances concerning MessagePack 2.5.192 advisories in functional-test dependencies | Baseline warnings remain; no dependency update was part of this task |
| Ordering unit tests | dotnet test --project tests/Ordering.UnitTests/Ordering.UnitTests.csproj --no-build --no-progress: 41 passed, 0 failed/skipped | The existing Ordering unit suite ran |
| Basket unit tests | dotnet test --project tests/Basket.UnitTests/Basket.UnitTests.csproj --no-build --no-progress: 3 passed, 0 failed/skipped | The existing Basket unit suite ran |

The unit checks followed the successful matching build. Build-time Catalog OpenAPI generation touched two tracked JSON files; those authoring-generated changes were restored. The delivered course belongs entirely under astra.

## Documentation checks

The course includes [check_course.py](../tools/check_course.py) to validate local links, story numbering and required sections, earlier prerequisites, and index/tracker coverage. The exact commands are in [commands.md](commands.md).

- Course structure/link checker: passed for 106 Markdown files, all 72 stories, and 1,125 local links. Story structure, prerequisite ordering, index coverage, and tracker coverage passed. Two incorrect migration-directory links were corrected before the passing run.
- Markdown lint against repository configuration: `npx.cmd --yes markdownlint-cli@0.45.0 "astra/**/*.md"` passed with exit code 0 and no lint findings. The one-off npm install emitted an engine advisory for a transitive package and a glob deprecation notice; these did not prevent this run, but the same tool installation may need a newer Node version elsewhere.
- Change scope: the authored files are under astra. The two generated Catalog JSON files were restored. The pre-existing untracked fabledocs and fabledoc2 folders were left intact.

## Checks not performed during authoring

The full AppHost/store journey, database-backed functional tests, Playwright journeys, mobile builds, schema exercises, concurrency spikes, and broker failure experiments were not executed as part of writing the course. Their steps are curriculum instructions, not claimed successes. No exercise implementation was added to production source.

This distinction matters: the build and 44 existing unit tests cannot prove runtime sign-in, database fixture stability, broker delivery guarantees, or the behavior proposed by the 72 assignments.

## Primary source entry points

| Claim or teaching area | Source |
| --- | --- |
| SDK and test runner | [global.json](../../global.json) |
| Aspire AppHost SDK and target framework | [AppHost project](../../src/eShop.AppHost/eShop.AppHost.csproj) |
| Resource names and optional AI flags | [AppHost composition](../../src/eShop.AppHost/Program.cs) |
| Package versions and build settings | [Directory.Packages.props](../../Directory.Packages.props), [root build props](../../Directory.Build.props), [test build props](../../tests/Directory.Build.props) |
| Web validation command | [PR workflow](../../.github/workflows/pr-validation.yml) |
| Browser projects and HTTP setup | [Playwright config](../../playwright.config.ts), [browser workflow](../../.github/workflows/playwright.yml) |
| Test frameworks and database fixture | [Basket test project](../../tests/Basket.UnitTests/Basket.UnitTests.csproj), [Catalog fixture](../../tests/Catalog.FunctionalTests/CatalogApiFixture.cs) |
| Catalog paging and filters | [CatalogApi](../../src/Catalog.API/Apis/CatalogApi.cs), [PaginationRequest](../../src/Catalog.API/Model/PaginationRequest.cs) |
| Basket enrichment and cached tasks | [BasketState](../../src/WebApp/Services/BasketState.cs) |
| Order ownership and error mapping | [OrdersApi](../../src/Ordering.API/Apis/OrdersApi.cs), [OrderQueries](../../src/Ordering.API/Application/Queries/OrderQueries.cs) |
| Domain transitions and transaction timing | [Order](../../src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs), [OrderingContext](../../src/Ordering.Infrastructure/OrderingContext.cs) |
| Failed-message acknowledgement | [RabbitMQEventBus](../../src/EventBusRabbitMQ/RabbitMQEventBus.cs) |
| Event-log state transitions | [IntegrationEventLogService](../../src/IntegrationEventLogEF/Services/IntegrationEventLogService.cs) |
| Existing test isolation concern | [CatalogApiTests](../../tests/Catalog.FunctionalTests/CatalogApiTests.cs) |

The tests directory contains its own Directory.Build.props. MSBuild's nearest-file discovery is a reason to inspect project-specific effective settings, rather than assume every project inherits every root property. The observed build emits source artifacts under artifacts and test outputs under the tests projects' bin directories.

## Official external references checked

- [Microsoft: global.json](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json) for SDK selection and roll-forward.
- [Microsoft: dotnet test with MTP](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test-mtp) for named project/solution selection.
- [Playwright: web-server setup](https://playwright.dev/docs/test-webserver) for test server launch and reuse.
- [RabbitMQ: acknowledgements and confirms](https://www.rabbitmq.com/docs/confirms) for delivery acknowledgement concepts.
- [RabbitMQ: dead-letter exchanges](https://www.rabbitmq.com/docs/dlx) for the broker failure-recovery design exercise.

External documentation can evolve independently of this repository's pinned dependencies. Use the source's actual APIs when implementing a story; the links supplement, rather than replace, source inspection.

## Keeping the course current

After updating the repository, recheck the baseline, SDK, project targets, test runner, explicit browser matching, and source links. Reproduce behaviors before retaining a “current limitation” claim. If a feature has already been implemented, turn its story into a characterization, review, or extension task with an equally explicit contract.
