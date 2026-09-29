# ASTRA-048: Validate webhook subscription ownership locally

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 8 — Identity and defensive coding  
**Type:** Authorization review lab · **Estimate:** 4-7 hours  
**Prerequisites:** [ASTRA-047](ASTRA-047.md)  
**Read first:** [Stage lesson](../01-lessons/08-identity-and-security.md)

## User story

As a webhook subscriber, I want subscription operations tied to my identity so that another user cannot manage my destinations.

## Starting point and scope

Inspect Webhooks.API ownership behavior and add a two-user regression for one existing operation, fixing a reproduced gap only within that operation's agreed contract.

- [WebHooksApi.cs](../../src/Webhooks.API/Apis/WebHooksApi.cs)
- [WebhookSubscription.cs](../../src/Webhooks.API/Model/WebhookSubscription.cs)
- [WebhooksContext.cs](../../src/Webhooks.API/Infrastructure/WebhooksContext.cs)

## Acceptance criteria

- [ ] Identify identity sources and ownership predicates for create/list/delete or the equivalent current operations.
- [ ] Choose one operation and assert owner versus non-owner behavior.
- [ ] Denied access causes no persisted mutation.
- [ ] Use only a local synthetic callback destination; record broader outbound-URL validation as separate work.

## Suggested approach

1. Read the current routes and data model before selecting the operation.
2. Propose a new Webhooks test project if no existing suite can exercise the boundary.
3. Write the regression first and change production code only for demonstrated unmet policy.

## Verification and evidence

Record the new test project's setup, discovery, and direct command if one is introduced. Provide two-user HTTP evidence for the selected operation.

## Hints, in order

1. A subscription ID alone is not ownership.
2. Do not turn a local test into requests to arbitrary external webhook URLs.

## Review conversation

How does this ownership problem resemble and differ from order access? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
