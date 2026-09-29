# ASTRA-053: Observe failed-message acknowledgement and propose recovery

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 9 — Events and consistency  
**Type:** Broker reliability lab · **Estimate:** 6-10 hours  
**Prerequisites:** [ASTRA-052](ASTRA-052.md)  
**Read first:** [Stage lesson](../01-lessons/09-events-and-consistency.md)

## User story

As a service operator, I want failed deliveries retained for investigation so that a handler exception does not silently discard business work.

## Starting point and scope

Reproduce the current catch-then-ack behavior in an isolated local test queue. Design a bounded retry/dead-letter prototype; do not reconfigure unrelated running queues.

- [RabbitMQEventBus.cs](../../src/EventBusRabbitMQ/RabbitMQEventBus.cs)
- [EventBusOptions.cs](../../src/EventBusRabbitMQ/EventBusOptions.cs)
- [Program.cs](../../src/eShop.AppHost/Program.cs)

## Acceptance criteria

- [ ] Capture baseline evidence that the selected processing failure is followed by acknowledgement.
- [ ] Define transient versus poison-message treatment and a finite retry limit.
- [ ] A prototype routes exhausted failures to an inspectable local dead-letter destination.
- [ ] Success is acknowledged and poison input cannot create a tight requeue loop.

## Suggested approach

1. Choose a test-only consumer/queue boundary and synthetic event.
2. Document the broker/client versions and acknowledgement path.
3. Implement a small prototype and test success, transient failure, and exhausted failure.

## Verification and evidence

Provide broker-backed evidence of queue destination and delivery count, plus teardown of only the test-owned resources. Pure mocks cannot establish dead-letter routing.

## Hints, in order

1. Nack with requeue=false discards unless dead-letter routing is configured.
2. Publisher confirmation and consumer acknowledgement are different guarantees.

## Review conversation

How would an operator safely replay a dead-lettered message without repeating its effect? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
