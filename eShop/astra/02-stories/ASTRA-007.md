# ASTRA-007: Explain the C# shapes used by this app

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 2 — C# and focused tests  
**Type:** Language lab · **Estimate:** 1-3 hours  
**Prerequisites:** [ASTRA-006](ASTRA-006.md)  
**Read first:** [Stage lesson](../01-lessons/02-csharp-and-testing-basics.md)

## User story

As a junior reading unfamiliar C#, I want concrete examples of its type features so that I can follow the code without treating syntax as magic.

## Starting point and scope

Use examples from OrderItem, BasketQuantity, PaginationRequest, and Catalog.razor. This is a reading and prediction exercise, not a refactor.

- [OrderItem.cs](../../src/Ordering.Domain/AggregatesModel/OrderAggregate/OrderItem.cs)
- [BasketService.cs](../../src/WebApp/Services/BasketService.cs)
- [PaginationRequest.cs](../../src/Catalog.API/Model/PaginationRequest.cs)

## Acceptance criteria

- [ ] Explain a class, record, nullable value, collection interface, and async return type with one source example each.
- [ ] Predict the result of a record with-expression and the meaning of a private setter.
- [ ] Distinguish an absent value from zero and the null-forgiving operator from validation.
- [ ] Write five small input/output predictions and check them against source or a scratch experiment.

## Suggested approach

1. Read the C# lesson and annotate only the selected types.
2. Translate one method into plain-language steps.
3. Discuss one prediction that was incorrect and revise it.

## Verification and evidence

Submit the annotated examples and corrected predictions. Keep scratch code separate from production changes and record any command used to run it.

## Hints, in order

1. IReadOnlyCollection does not make the elements immutable.
2. A Task represents completion; it is not necessarily a separate thread.

## Review conversation

Why is a private setter helpful for OrderItem.Units? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
