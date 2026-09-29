# Run, observe, and debug a request

A distributed application has several processes. A successful AppHost launch does not mean every dependency or API is healthy. Diagnose the resource that failed.

## A guided browsing experiment

1. Start AppHost using the setup guide. In the dashboard, locate `postgres`, `redis`, `eventbus`, `catalog-api`, `identity-api`, `ordering-api`, and `webapp`.
2. Open the store through `webapp`. Select a brand, then a product.
3. Write down the browser URLs. A query parameter such as `page=2` belongs to the UI; the catalog API uses a zero-based `pageIndex`.
4. Open [Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor). Its page size is 9, and it subtracts one from the displayed page before asking the service for items.
5. Follow [CatalogService](../../src/WebAppComponents/Services/CatalogService.cs) to the URL it builds. Its client registration in [WebApp Extensions](../../src/WebApp/Extensions/Extensions.cs) supplies a logical service address and API version 2.
6. Find `GetAllItems` in [CatalogApi](../../src/Catalog.API/Apis/CatalogApi.cs). Follow the query to its count, ordering, skip, take, and database execution.

Write a trace table:

| Step | Process | Input | Result |
| --- | --- | --- | --- |
| Home page | WebApp | UI page and filter parameters | Razor page model |
| Catalog client | WebApp | Zero-based page, brand, type | HTTP request |
| GetAllItems | Catalog.API | Bound request parameters | Filtered query |
| ToListAsync | Catalog.API / PostgreSQL | Ordered, bounded query | Rows |
| Render | WebApp | CatalogResult | HTML cards and page links |

Fill in actual values from your run. Notice that the browser network panel can show the page request without showing the server's downstream HTTP call. Use the dashboard trace to see that second hop.

## Put a breakpoint in the right process

Use your IDE's attach-to-process feature to attach to the running WebApp or Catalog.API process. Put a breakpoint in `GetAllItems`, trigger a page request, and inspect `PageIndex`, `PageSize`, and filters. If your IDE launches services directly, retain the AppHost-provided configuration; a standalone API can be missing its connection strings and discovery endpoints.

Predict the values before continuing. Step over query construction, then step over `ToListAsync`. The `IQueryable` object describes a query; it is not already a loaded list of products.

An alternative without a debugger is to inspect existing structured logs and traces and write down the same inputs and outputs. Do not add broad request-body logging to see what is happening.

## Inspect one API directly

Copy the catalog API base endpoint from the dashboard, without a trailing slash, and set it locally:

```powershell
$catalogBase = 'PASTE_THE_LOCAL_CATALOG_ENDPOINT'
Invoke-RestMethod "$catalogBase/api/catalog/items?api-version=2.0&pageIndex=0&pageSize=3"
```

Replace the placeholder before running. Expect a paginated JSON response; inspect its actual field names. Try a positive ID from the returned data, then a positive ID that does not exist. Record the status codes separately from the response bodies.

Only make catalog write requests against your local sample instance. Many later stories intentionally change stock, prices, or test records.

## Use a hypothesis, not a random edit

Suppose a filter returns no cards. Possible explanations include no matching data, a page offset beyond the filtered results, a failed API call, or stale UI state. Test one explanation at a time:

- Record the browser query.
- Replay the corresponding API query with pageIndex 0.
- Compare count and data length.
- Check the resource error and trace if the request failed.
- Reproduce from a fresh navigation before changing lifecycle code.

A successful diagnosis explains both the broken case and a nearby working case.

## Stop and resume

Use Ctrl+C in the AppHost terminal. Some resources use persistent container lifetimes in this checkout; inspect Docker before assuming everything stopped. Restart AppHost and check its current endpoints. Avoid deleting shared Docker volumes or pruning all containers as a troubleshooting shortcut.

Record your experiment in [the debugging journal](../04-templates/debugging-journal.md), then move to [your first contribution](04-first-contribution.md).
