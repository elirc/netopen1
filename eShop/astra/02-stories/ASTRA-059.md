# ASTRA-059: Make webhook HTTP failures observable

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 10 — Diagnosis and operations  
**Type:** HTTP reliability feature · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-058](ASTRA-058.md), [ASTRA-048](ASTRA-048.md)  
**Read first:** [Stage lesson](../01-lessons/10-debugging-and-observability.md)

## User story

As a webhook maintainer, I want unsuccessful destination responses recorded as failures so that completed HTTP tasks are not mistaken for successful delivery.

## Starting point and scope

WebhooksSender currently returns SendAsync tasks without checking response status. Use a local fake handler or receiver and keep retry/durable delivery outside this slice.

- [WebhooksSender.cs](../../src/Webhooks.API/Services/WebhooksSender.cs)
- [IWebhooksSender.cs](../../src/Webhooks.API/Services/IWebhooksSender.cs)

## Acceptance criteria

- [ ] A non-success HTTP response produces a deliberate failure outcome or safe log with subscription context.
- [ ] A success response remains successful.
- [ ] Request and response resources are disposed through the chosen design.
- [ ] Tests use a local fake transport and avoid logging destination tokens or sensitive payloads.

## Suggested approach

1. Read SendAll and OnSendData and define how one destination failure affects the aggregate result.
2. Use a controlled HttpMessageHandler in the Webhooks harness introduced earlier.
3. Handle response status and resource lifetime explicitly.

## Verification and evidence

Run focused tests for success, 500, and transport exception. Explain whether other destinations still complete and why that policy was chosen.

## Hints, in order

1. SendAsync completes for ordinary HTTP error status responses.
2. Task.WhenAll alone does not inspect HTTP status codes.

## Review conversation

What must change before this can claim durable webhook delivery? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
