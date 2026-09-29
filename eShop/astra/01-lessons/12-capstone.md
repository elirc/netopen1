# Capstone: let shoppers browse available products

Learning goal: deliver a small feature across an API, database query, shared client, Blazor UI, and tests.

## Product brief

A shopper wants to hide products whose AvailableStock is zero while browsing. Add an opt-in “In stock only” filter to the catalog. Existing browsing continues when the option is off. This is a proposed course feature; it does not exist as this filter in the baseline.

The display is advisory. Inventory can change between browsing and checkout. Do not promise reservation, guaranteed purchase, or a stock count synchronized across every page.

## Contract to settle in ASTRA-067

- Version 2 list API accepts optional boolean `inStockOnly`, default false.
- True selects AvailableStock > 0 before counting and pagination.
- Brand, type, and existing name behavior compose with the filter.
- Version 1 retains its previous semantics.
- An invalid boolean is a documented client error.
- UI query state survives pagination and refresh.
- Changing brand, type, or stock selection clears the current page while preserving the other active filters.
- An empty filtered result has a recovery action.
- Stable ordering and valid pagination still apply.

This feature needs no new stored field or migration: AvailableStock already exists. Stage 6's migration exercise is separate practice.

## Scope boundaries

Use the existing Catalog.API and WebApp. Update shared client contracts only as needed and inspect all ICatalogService implementations. Search and compile callers before calling the change complete.

Keep price sorting, stock reservations, saved user preferences, authentication redesign, and semantic-search redesign outside this capstone. They can be future proposals after the feature is reviewed.

## Six reviewable slices

| Story | Deliverable |
| --- | --- |
| ASTRA-067 | Contract, dependency map, acceptance matrix, and PR slices |
| ASTRA-068 | API filter with database-backed contract tests |
| ASTRA-069 | Shared client and query-driven UI toggle |
| ASTRA-070 | Discovered browser tests and compatibility coverage |
| ASTRA-071 | Performance and failure experiment with an honest report |
| ASTRA-072 | Final review, demo, local release rehearsal, and handoff |

All six slices are required for course completion. Keep commits small enough that a reviewer can understand each layer.

## Test dataset

Create controlled products with stock 0, 1, and a larger positive value; include shared brand/type combinations and tied names. Use test-owned data so earlier stock exercises cannot silently change expected results.

Test false/default, true, invalid input, combined filters, first and later pages, and empty results. Confirm count is computed after all filters, while Data contains only the requested page. Preserve version 1 expectations.

## Demonstration script

1. Open the unfiltered catalog and note the URL.
2. Enable the filter and show that an unavailable controlled product disappears.
3. Select a brand and type; show all selections remain in the URL.
4. Navigate to another page, refresh, and show retained state.
5. Choose a combination with no matches and use its recovery action.
6. Explain one trace and the query change.
7. Show automated evidence and describe a known limitation.

Use the [capstone rubric](../03-reference/assessment.md). A polished screenshot is not a substitute for the API and database evidence.
