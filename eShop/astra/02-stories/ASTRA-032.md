# ASTRA-032: Reject negative restocking without changing state

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 6 — Persistence and domain rules  
**Type:** Domain correction · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-031](ASTRA-031.md)  
**Read first:** [Stage lesson](../01-lessons/06-data-and-domain.md)

## User story

As an inventory maintainer, I want negative restock requests rejected so that an operation called AddStock cannot silently remove inventory.

## Starting point and scope

Proposed policy: reject negative quantities with CatalogDomainException, allow zero as a no-op for stock, and preserve the existing capacity cap. Explicitly decide whether zero resets OnReorder.

- [CatalogItem.cs](../../src/Catalog.API/Model/CatalogItem.cs)

## Acceptance criteria

- [ ] Negative input throws before stock or OnReorder changes.
- [ ] Zero leaves the quantity unchanged with a documented OnReorder policy.
- [ ] Valid additions and capacity-limited additions retain the expected actual increment.
- [ ] Boundary tests include a nearly full item and an already full item.

## Suggested approach

1. Add a regression test in the catalog model harness from ASTRA-031.
2. Place validation before state mutation.
3. Update misleading comments only where necessary to describe the resulting policy.

## Verification and evidence

Run the catalog model tests and related catalog functional tests if this path is exercised there. Include prior and final state in the negative-input assertion.

## Hints, in order

1. The method currently resets OnReorder after arithmetic.
2. An exception raised after changing state violates the intended rejection behavior.

## Review conversation

How did you choose and document zero-quantity semantics? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
