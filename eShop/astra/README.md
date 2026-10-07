# Astra: a junior developer bootcamp inside eShop

Learn to join a team, understand an unfamiliar application, make small contributions, and gradually own a feature across services. This course uses the code in this checkout: AdventureWorks/eShop, a C# application with Blazor, ASP.NET Core, Aspire, PostgreSQL, Redis, and RabbitMQ.

Start with [your first day](00-onboarding/01-first-day.md). You do not need to understand microservices before beginning.

## What you will produce

- A reproducible workstation and a map of the application.
- Small documentation, UI, API, and domain contributions with review evidence.
- Tests for normal behavior, invalid input, ownership, and failure paths.
- A debugging journal, an architecture decision, and a local incident report.
- A final availability-filter feature with a reviewable pull request package.

There are **72 user stories in 12 stages**, plus onboarding tutorials, worked examples, review rubrics, and reusable templates. Every story is a practice assignment, not an upstream issue or a claim that a maintainer has requested the feature. The curriculum does not implement the exercises for you.

## Follow this route

1. Read [first day](00-onboarding/01-first-day.md), [environment setup](00-onboarding/02-environment.md), and [run and debug](00-onboarding/03-run-and-debug.md).
2. Learn [how to contribute](00-onboarding/04-first-contribution.md), then complete stories ASTRA-001 through ASTRA-006.
3. Follow the [curriculum](CURRICULUM.md), reading each stage's lesson before its stories.
4. Record results in the [progress tracker](PROGRESS.md). Use the [story index](02-stories/README.md) to pick the next dependency-ready assignment.
5. Pass each [stage gate](03-reference/assessment.md) before advancing. Bring evidence to a mentor, or use the self-review route.

## Pace and prerequisites

Assume basic computer use, a little programming, and willingness to read unfamiliar code. If methods, loops, and classes are new, spend an extra week on the C# lesson and ask a mentor to pair on stage 2. No prior distributed-systems experience is assumed.

Allow roughly 300-450 hours including reading, retries, and review. At 12-15 hours per week this is about 24-36 weeks; experience and setup friction will change that. Story estimates are planning ranges, not deadlines. Stages 1-8 form the junior contribution path. Stages 9-11 are a supported stretch into distributed systems. Stage 12 joins those skills in one capstone. Stay longer at a gate when you cannot explain the result yet.

For each session: read for 20 minutes, predict behavior, run one experiment, make one small change, verify it, and write down what surprised you. A completed checkbox requires observable evidence.

## How to use the repository

All commands in this course run from the **eShop Git root**, the directory containing `global.json` and `eShop.Web.slnf`. In the supplied workspace that is `netopen1/eShop`. *Note (2026-10-06):* in the `elirc/netopen1` repository the Git root is one level higher (`eShop/` is a subfolder) and history is a single snapshot commit, so run commands from `eShop/`, the folder containing `global.json`, and treat "Git root" in later pages as that folder. Course material lives in `astra`; exercise implementations eventually modify `src`, `tests`, or `e2e` on your practice branches.

Keep personal work under an optional `astra/workbook/` directory, using [the templates](04-templates/README.md). That directory is not created or ignored for you; decide what belongs in a reviewed practice commit. Never put tokens, authentication state, or copied customer data in a workbook.

The existing `fabledocs` and `fabledoc2` folders are separate material. This course stands alone and does not require them.

## What is true of this checkout

The source baseline is commit `9b4f943` (`Update to Asp.Versioning to v10-preview2 (#980)`). [global.json](../global.json) selects .NET SDK `10.0.100` with `latestFeature` roll-forward and Microsoft.Testing.Platform; the web projects target `net10.0`. The [AppHost project](../src/eShop.AppHost/eShop.AppHost.csproj) uses Aspire AppHost SDK `13.2.0`. The top-level README still describes .NET 9. Follow the configuration and the [verification notes](03-reference/verification.md) when they disagree.

Some lessons intentionally examine sample limitations: unchecked basket quantities, order ownership boundaries, broad exception handling, and acknowledging failed messages. Reproduce behavior before treating a suspicion as a bug. Proposed course policies are labeled explicitly; they are not silently presented as existing functionality.

## Reference shelf

- [System map and reading route](01-lessons/01-codebase-map.md)
- [Commands and test project choices](03-reference/commands.md)
- [Troubleshooting](03-reference/troubleshooting.md)
- [Glossary](03-reference/glossary.md)
- [Assessment and mentor guide](03-reference/assessment.md)
- [Sources and verification limits](03-reference/verification.md)
- [Templates](04-templates/README.md)
