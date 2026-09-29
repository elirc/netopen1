# ASTRA-002: Launch and tour the local store

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 1 — Onboard and contribute  
**Type:** Guided runtime lab · **Estimate:** 1-2 hours  
**Prerequisites:** [ASTRA-001](ASTRA-001.md)  
**Read first:** [Stage lesson](../00-onboarding/04-first-contribution.md)

## User story

As a new developer, I want to start the store and identify its resources so that I can reproduce a user's journey locally.

## Starting point and scope

Use the existing AppHost with both optional AI flags disabled. This is a local browsing exercise, not a deployment.

- [Program.cs](../../src/eShop.AppHost/Program.cs)
- [launchSettings.json](../../src/eShop.AppHost/Properties/launchSettings.json)
- [Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor)

## Acceptance criteria

- [ ] Start AppHost and locate WebApp, Catalog, Identity, Redis, PostgreSQL, and RabbitMQ in its dashboard.
- [ ] Open the store, select a filter, and navigate to a product detail page.
- [ ] Record one healthy resource and the evidence you used to judge it.
- [ ] Stop and restart the host, then explain which resources use persistent lifetimes.

## Suggested approach

1. Follow the run-and-debug guide and leave AppHost's terminal open.
2. Use the current dashboard endpoint links rather than hard-coded ports.
3. Record the browse steps and one sanitized screenshot or textual resource report.

## Verification and evidence

A second person should be able to repeat your browse sequence. Include startup and restart outcomes; omit the dashboard login token from evidence.

## Hints, in order

1. Resource references and WaitFor calls serve different purposes.
2. The dashboard being visible does not imply every API is ready.

## Review conversation

If the store failed while the dashboard worked, which resource would you inspect first and why? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
