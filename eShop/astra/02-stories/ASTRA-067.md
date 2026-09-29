# ASTRA-067: Define the availability-filter capstone

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 12 — Capstone: available products  
**Type:** Capstone planning · **Estimate:** 4-8 hours  
**Prerequisites:** [ASTRA-066](ASTRA-066.md)  
**Read first:** [Stage lesson](../01-lessons/12-capstone.md)

## User story

As a shopper, I want an opt-in in-stock filter so that I can focus browsing on products currently available.

## Starting point and scope

Use the capstone brief to specify version 2 inStockOnly behavior across API, query, shared client, and UI. No stock reservation or new schema is required.

- [CatalogApi.cs](../../src/Catalog.API/Apis/CatalogApi.cs)
- [CatalogItem.cs](../../src/Catalog.API/Model/CatalogItem.cs)
- [ICatalogService.cs](../../src/WebAppComponents/Services/ICatalogService.cs)
- [Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor)

## Acceptance criteria

- [ ] Approve a written acceptance matrix covering default/false, true, invalid input, combined filters, pagination, and empty results.
- [ ] State version 1 compatibility and advisory stock semantics.
- [ ] Map affected files and all ICatalogService implementers.
- [ ] Split implementation into the next five stories with test-owned data and evidence expectations.

## Suggested approach

1. Read the capstone lesson and trace AvailableStock's existing storage.
2. Identify prerequisite code changes to retain in the capstone branch.
3. Write the API and UI query-state contract before editing.

## Verification and evidence

Submit the contract, dependency map, and planned PR slices. Mentor review or the structured self-review route must settle ambiguous behavior before implementation.

## Hints, in order

1. AvailableStock already exists, so a migration is unnecessary.
2. Do not promise that a displayed product is reserved until checkout.

## Review conversation

How will you explain a product becoming unavailable after the page was rendered? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
