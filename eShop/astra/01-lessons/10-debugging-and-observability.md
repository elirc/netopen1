# Explain failures with evidence

Learning goal: move from a symptom to a falsifiable explanation and a minimal fix.

## Use the existing telemetry

[ServiceDefaults](../../src/eShop.ServiceDefaults/Extensions.cs) configures logs, metrics, and tracing, with OTLP export when an endpoint is configured. The event bus has its own activity source and context propagation. AppHost provides a dashboard for the local application.

A log records an event. A trace relates operations across a request or message chain. A metric aggregates measurements over time. Use each for its purpose: a request ID is useful in a log but usually a poor metric label because it creates unbounded label values.

## Follow one operation

Place one synthetic order and record its request ID, order ID if available, and trace ID. Do not copy complete checkout payloads. Follow the HTTP call, transaction logs, publish activity, receive activity, and order status.

A missing span does not immediately prove a missing operation. Check instrumentation registration, sampling, exporter configuration, and whether a background operation has the expected parent context.

## Liveness and readiness

This checkout maps /alive and /health only in Development. /alive selects checks tagged live; /health runs all registered checks. The default self check proves responsiveness, while actual dependency checks depend on service registrations.

Do not claim /health always tests every infrastructure dependency. Read the resource's health registrations and compare observed results while a dependency is unavailable.

## A controlled incident exercise

1. Define the expected symptom and recovery before changing anything.
2. Use a local practice instance with no other learner depending on it.
3. Stop only the chosen resource, or use a test double to force a failure.
4. Trigger one operation and collect its output, trace, and relevant log.
5. Restore the dependency and verify a fresh operation.
6. Explain whether the failed original operation recovered, was retried, or needs intervention.

Do not delete all Docker volumes to simulate a network failure. Record the exact resource changed so the experiment can be reversed.

## Measure before optimizing

Choose one catalog request and a fixed dataset. Warm up once, record repeated timings, and separate application time from startup and image download. Keep result count and correctness identical when comparing a query change.

A single fast request does not prove an improvement. Report sample count, median, spread or tail, dataset size, environment, and limitations. Prefer a modest honest conclusion over an unsupported percentage.

## Make cancellation observable

Follow a CancellationToken from an HTTP handler or hosted service to the database or delay operation. Add token propagation only along a chosen path, and verify a pre-cancelled or controlled cancellation case. Never use a broad catch to report cancellation as a successful operation.

## Journal and handoff

Use [the debugging template](../04-templates/debugging-journal.md) for evidence and hypotheses. Use [the incident template](../04-templates/incident.md) for the user symptom, contributing factors, recovery, and one follow-up action. A useful report distinguishes facts, inference, and unanswered questions.
