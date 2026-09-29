# ASTRA-054: Test an additive event-contract change

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 9 — Events and consistency  
**Type:** Compatibility lab · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-053](ASTRA-053.md)  
**Read first:** [Stage lesson](../01-lessons/09-events-and-consistency.md)

## User story

As a service maintainer deploying independently, I want optional event fields handled compatibly so that mixed service versions can exchange messages.

## Starting point and scope

Choose one existing integration event and add a proposed optional diagnostic field in a practice branch. Preserve the event's routing name and existing fields.

- [IntegrationEvent.cs](../../src/EventBus/Events/IntegrationEvent.cs)
- [RabbitMQEventBus.cs](../../src/EventBusRabbitMQ/RabbitMQEventBus.cs)
- [OrderStatusChangedToPaidIntegrationEvent.cs](../../src/Catalog.API/IntegrationEvents/Events/OrderStatusChangedToPaidIntegrationEvent.cs)

## Acceptance criteria

- [ ] An older serialized fixture remains readable by the new contract with a defined missing-field default.
- [ ] A new serialized fixture is accepted by an older-shape reader that ignores the optional field.
- [ ] The event type/routing key and existing field meaning remain stable.
- [ ] Any source-generation registration needed by the selected consumer is inspected and updated.

## Suggested approach

1. Choose publisher and consumer copies of the same wire event.
2. Create old/new JSON fixtures with synthetic values.
3. Add serialization compatibility tests using the actual configured serializer behavior.

## Verification and evidence

Run the focused contract tests and relevant builds. State that serializer compatibility does not prove business semantic compatibility under every mixed deployment.

## Hints, in order

1. A renamed C# event type can also rename the RabbitMQ routing key.
2. Default values need a meaning, not merely successful deserialization.

## Review conversation

Which kind of event change would require a more deliberate versioning strategy? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
