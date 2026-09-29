# Design an API contract before changing the handler

Learning goal: separate routing, binding, validation, business behavior, and response shape.

## Read the actual route

[CatalogApi](../../src/Catalog.API/Apis/CatalogApi.cs) has versioned route groups. V1 and V2 list handlers differ, and V1 update uses PUT /items while V2 uses PUT /items/{id}. [WebApp client registration](../../src/WebApp/Extensions/Extensions.cs) selects version 2 for catalog calls. Existing functional tests exercise both versions.

A contract contains the method, path, version, parameter names, valid values, response status, and body shape. Changing one can break a caller even if the C# method compiles.

Create a table for one endpoint before editing:

| Input | Present behavior to observe | Proposed rule |
| --- | --- | --- |
| Valid positive item ID | 200 and item | Preserve |
| Positive ID not found | 404 | Preserve |
| Zero ID | 400 in GetItemById | Preserve |
| Non-integer path segment | Routing outcome | Document actual behavior |

Route matching occurs before the handler. Calling GetItemById directly in a unit test cannot prove routing or parameter binding.

## Typed results and metadata

A signature such as `Results<Ok<CatalogItem>, NotFound, BadRequest<ProblemDetails>>` describes allowed result types. If you add a 400 path to a method currently returning only Ok, update the type and affected wrappers as well as the implementation.

Attributes describing responses document intent. They are not proof that every described invalid request is rejected. [PaginationRequest](../../src/Catalog.API/Model/PaginationRequest.cs) has defaults and descriptions, but no declared bounds.

The course pagination policy is new work: pageIndex >= 0, pageSize between 1 and 100, and an offset that cannot overflow the chosen integer calculation. Validate before database execution. State which list routes the change covers; shared types may also affect semantic-search handlers.

## Boundary tests

For pagination use default values, -1, 0, 1, 100, 101, a huge page index, and a non-integer value. Verify both status and response semantics. An empty valid page is a successful result, not an invalid request.

If two products have the same name, ordering only by Name leaves the tie unspecified. A secondary stable key, such as Id, makes adjacent pages easier to reason about. Stable ordering does not make offset pagination a snapshot under concurrent writes; explain that limitation.

## Failures should retain meaning

[OrdersApi.GetOrderAsync](../../src/Ordering.API/Apis/OrdersApi.cs) catches all exceptions and returns NotFound. A missing row and a database failure therefore look the same at that boundary. A later story narrows the missing-data case and verifies unexpected errors remain observable failures.

Do not blanket-catch exceptions merely to return a pleasant status. Decide what the client can correct and what needs operator investigation.

## A contract change checklist

1. Identify producers and callers using symbol search.
2. Write normal, invalid, and boundary cases.
3. Update the smallest shared contract needed.
4. Preserve existing version behavior unless the story explicitly changes it.
5. Run functional tests that cross HTTP binding and serialization.
6. Inspect generated OpenAPI through the app's configured OpenAPI support if metadata changed.

Course exercises involving new input bounds or user-visible behavior are proposed specifications. Include that distinction in your practice PR.

## Lab

Complete the response-matrix story before pagination validation. Try the inputs against the current local API, then compare them with the source. If your expectation differs, save the evidence and revise the specification before coding.
