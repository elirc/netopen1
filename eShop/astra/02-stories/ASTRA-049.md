# ASTRA-049: Trace checkout to its eventual order status

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 9 — Events and consistency  
**Type:** Distributed code reading · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-048](ASTRA-048.md)  
**Read first:** [Stage lesson](../01-lessons/09-events-and-consistency.md)

## User story

As a junior diagnosing checkout, I want to follow the asynchronous order lifecycle so that I know what an accepted HTTP request actually means.

## Starting point and scope

Trace the existing grace-period, stock, and simulated payment flow. Use source evidence first and one local synthetic order if runtime is available.

- [CreateOrderCommandHandler.cs](../../src/Ordering.API/Application/Commands/CreateOrderCommandHandler.cs)
- [GracePeriodManagerService.cs](../../src/OrderProcessor/Services/GracePeriodManagerService.cs)
- [OrderStatusChangedToAwaitingValidationIntegrationEventHandler.cs](../../src/Catalog.API/IntegrationEvents/EventHandling/OrderStatusChangedToAwaitingValidationIntegrationEventHandler.cs)
- [OrderStatusChangedToStockConfirmedIntegrationEventHandler.cs](../../src/PaymentProcessor/IntegrationEvents/EventHandling/OrderStatusChangedToStockConfirmedIntegrationEventHandler.cs)

## Acceptance criteria

- [ ] Map each stage's publisher, event type, subscription, handler, and next state.
- [ ] Distinguish domain events from serialized integration events.
- [ ] Identify where a response can be complete while business processing continues.
- [ ] Record a success path and at least one rejection or failure branch.

## Suggested approach

1. Follow one event name across src using rg.
2. Build a sequence diagram with storage and process boundaries.
3. Compare one runtime trace with the diagram, marking unobserved branches.

## Verification and evidence

Submit the diagram with source links and any local order/trace identifiers sanitized. Explain which parts are source-verified and which were executed.

## Hints, in order

1. Type names influence RabbitMQ routing in this implementation.
2. The payment processor is a simulation.

## Review conversation

What would you inspect if an order stayed Submitted after checkout returned? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
