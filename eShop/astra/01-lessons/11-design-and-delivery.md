# Make a change that another developer can maintain

Learning goal: weigh alternatives, limit scope, and deliver evidence with the implementation.

## Separate a decision from an implementation

An architecture decision record is useful when a choice affects more than one local method. Use [the ADR template](../04-templates/architecture-decision.md) for a basket concurrency strategy, a message retry policy, or an API compatibility decision.

Describe the problem with a concrete example. Two tabs each read quantity 1; one adds product A and the other adds product B; replacing the entire basket may lose one update. Compare conditional writes, server-side operations, and accepting the current limitation. Name the consequences for callers and tests.

You do not need a new library to show design skill. A small experiment that disproves an approach is useful evidence.

## Refactor around a demonstrated pressure

A refactor preserves behavior while changing structure. First identify repetition, a hard-to-test boundary, or a confusing responsibility. Keep existing tests green and explain how the new structure reduces that problem.

For example, CatalogService contains query-string construction. Extracting a small URL-building function could support a new filter test. Introducing a generic repository across every service to do that would expand the change far beyond its purpose.

For a shared interface, search all implementers. [ICatalogService](../../src/WebAppComponents/Services/ICatalogService.cs) also connects to the hybrid app. A default parameter can preserve some call sites while still requiring implementers to update their signatures. Compile the web path and document any platform checks that remain unavailable.

## Read CI as executable documentation

[PR validation](../../.github/workflows/pr-validation.yml) builds the web filter and runs MTP tests. [Playwright validation](../../.github/workflows/playwright.yml) installs browser dependencies and configures sample credentials. [Markdown linting](../../.github/workflows/markdownlint.yml) runs separately.

New tests must be discoverable in the intended job. A file on disk is not enough. A new project outside the web filter or an unmatched Playwright filename can silently escape the normal checks.

Keep CI changes scoped. Demonstrate the command locally and explain workflow trigger behavior. Do not modify the mobile pipeline merely because your browser feature has a mobile-sounding name.

## Review in layers

1. Behavior: do the acceptance cases match the requirement?
2. Boundaries: is identity trusted, data validated, and failure meaning preserved?
3. Tests: do they exercise real behavior with controlled data?
4. Maintenance: are names, dependencies, and comments proportionate?
5. Delivery: can someone reproduce and reverse the change?

Use [the review template](../04-templates/review.md). A useful comment links a concern to a specific outcome and suggests a direction without unnecessarily prescribing every line.

## Release thinking in a local course

A deployment rehearsal here is a local procedure: build, apply any required local migration, start resources, smoke test, and describe rollback. Creating cloud resources is not required.

For a schema change, explain which rollback would lose newly stored data. For an event change, explain how mixed producer and consumer versions behave. For a UI/API feature, deploy order matters if one side depends on a new contract.

## Checkpoint

Present one ADR with two plausible options and measured evidence from a small prototype. Ask a mentor to challenge one assumption. Revise the decision and keep the experiment's limitations visible.
