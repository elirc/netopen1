# ASTRA-016: Give cart quantity controls distinct labels

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 3 — Blazor and accessible UI  
**Type:** Accessible forms · **Estimate:** 2-4 hours  
**Prerequisites:** [ASTRA-015](ASTRA-015.md)  
**Read first:** [Stage lesson](../01-lessons/03-blazor-and-browser.md)

## User story

As a shopper with several products in my bag, I want quantity controls identified by product so that I update the intended row.

## Starting point and scope

CartPage currently repeats the generic product quantity label. Improve accessible names while retaining named form handlers and antiforgery protection.

- [CartPage.razor](../../src/WebApp/Components/Pages/Cart/CartPage.razor)
- [AddItemTest.spec.ts](../../e2e/AddItemTest.spec.ts)
- [RemoveItemTest.spec.ts](../../e2e/RemoveItemTest.spec.ts)

## Acceptance criteria

- [ ] Two different cart rows expose distinct quantity names containing their product names.
- [ ] Updating the second product changes only its quantity and recalculates totals.
- [ ] Setting quantity to zero retains the existing removal behavior.
- [ ] The form handler and antiforgery token remain functional.

## Suggested approach

1. Create a two-product local basket and inspect labels.
2. Update the control naming in the repeated row.
3. Use the new accessible names in a logged-in browser assertion.

## Verification and evidence

Run the logged-in Playwright project with controlled basket setup and cleanup. Include a keyboard interaction and a two-row assertion.

## Hints, in order

1. A shared input name can be required for server binding even when its accessible label differs.
2. Select the intended row by user-visible product information.

## Review conversation

How does your test detect changing the wrong product? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
