# Change a Blazor page with observable evidence

Learning goal: connect route parameters, component state, rendered HTML, and a user's action.

## Understand the rendering style first

[Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor) uses a page route, query-bound properties, dependency injection, and stream rendering. [CartPage](../../src/WebApp/Components/Pages/Cart/CartPage.razor) uses server-handled forms, named handlers, and antiforgery tokens. Do not assume a React-style client state model or an interactive Blazor circuit for every page.

Find the initial load, the form handler, and the variable used by markup. A UI change can affect server-rendered HTML, a full navigation, or an enhanced form response. Test the actual navigation rather than changing lifecycle methods by habit.

## Follow a filter

[CatalogSearch](../../src/WebAppComponents/Catalog/CatalogSearch.razor) builds query URLs through NavigationManager. Changing a brand preserves the current type and clears page. That reset matters: page 5 of the entire catalog may not exist inside the selected brand.

Before adding a new filter, specify what happens to every existing query parameter. This becomes part of the capstone contract.

## Distinguish loading, empty, and failed

The catalog currently displays “Loading...” while its result is null. A successful response containing no rows is a different state. A failed HTTP call is different again.

For the empty-state exercise, start with the existing successful result and inspect Data.Count or enumeration appropriately. Show a helpful message and a working way back to the catalog. Do not turn all exceptions into an empty result; that would conceal an outage as “no products.”

The item detail page already has a not-found branch. Read that branch before proposing a new one. The exercise adds recovery and verifies the existing 404 behavior rather than pretending it is absent.

## Make semantics useful

Product images already have product-name alternative text in [CatalogListItem](../../src/WebAppComponents/Catalog/CatalogListItem.razor). Avoid assigning that as a new feature. More useful work includes a pagination navigation label, a current-page indicator, and quantity controls whose accessible names distinguish products.

An HTML `min` attribute assists a user. Server validation is still required for forged form submissions and direct API calls.

Test with a keyboard: Tab to the relevant control, observe focus, activate it, and verify the resulting content. Browser automation checks one layer; a manual keyboard pass can catch awkward focus order.

## A browser assertion

Existing browser tests use Playwright and role-based locators:

```typescript
await page.goto('/');
await expect(
  page.getByRole('heading', { name: 'Ready for a new adventure?' })
).toBeVisible();
```

Use assertions that match the story's behavior. A pagination story should assert the resulting page, retained filters, and current-page state; merely checking that the home page loaded proves little.

The [Playwright config](../../playwright.config.ts) uses explicit testMatch lists. A new `.spec.ts` file is not automatically included in those projects. Either extend an appropriate existing file or deliberately update the matching project. Run `npx.cmd playwright test --list` to verify discovery before claiming coverage.

See [commands](../03-reference/commands.md) for local HTTP endpoints and sample login variables. The browser server option may reuse an existing server locally; ensure it is the correct eShop process before interpreting a green run.

## Lab

Choose a brand/type combination that returns no results in your own dataset. Capture the existing page, write the expected empty-state text and recovery action, implement the small branch, and validate both empty and populated pages. Describe why loading and errors retain separate meanings.
