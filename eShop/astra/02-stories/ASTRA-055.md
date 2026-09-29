# ASTRA-055: Produce a cross-service diagnostic trace

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 10 — Diagnosis and operations  
**Type:** Observability lab · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-054](ASTRA-054.md)  
**Read first:** [Stage lesson](../01-lessons/10-debugging-and-observability.md)

## User story

As a developer handling a slow order report, I want correlated evidence so that I can locate time spent across services.

## Starting point and scope

Use existing telemetry for one browse and one synthetic checkout. Do not add full-body logging to obtain correlation.

- [Extensions.cs](../../src/eShop.ServiceDefaults/Extensions.cs)
- [RabbitMQTelemetry.cs](../../src/EventBusRabbitMQ/RabbitMQTelemetry.cs)
- [RabbitMQEventBus.cs](../../src/EventBusRabbitMQ/RabbitMQEventBus.cs)
- [OrderingApiTrace.cs](../../src/Ordering.API/Extensions/OrderingApiTrace.cs)

## Acceptance criteria

- [ ] Record one HTTP trace and one event-related operation with process and duration.
- [ ] Connect safe request/order/event identifiers where available.
- [ ] Explain a missing span by inspecting instrumentation and export configuration before assuming missing work.
- [ ] Separate synchronous response time from eventual order completion.

## Suggested approach

1. Start an isolated local AppHost session.
2. Trigger the two operations and follow their dashboard traces.
3. Annotate a sanitized timeline with observed and inferred relationships.

## Verification and evidence

Submit the timeline and source links. Include an explicit note for any broken or absent propagation found in the actual run.

## Hints, in order

1. A background event may not share the browser request's lifetime.
2. Development sampling and an OTLP endpoint affect what you see.

## Review conversation

Which trace segment would you inspect first for a slow catalog page? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
