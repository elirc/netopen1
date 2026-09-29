# ASTRA-014: Make pagination understandable to assistive technology

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 3 — Blazor and accessible UI  
**Type:** Accessibility improvement · **Estimate:** 2-4 hours  
**Prerequisites:** [ASTRA-013](ASTRA-013.md)  
**Read first:** [Stage lesson](../01-lessons/03-blazor-and-browser.md)

## User story

As a shopper navigating by keyboard or screen reader, I want clearly identified page links so that I know where I am in the catalog.

## Starting point and scope

Improve existing catalog pagination semantics while retaining its URLs and page calculation.

- [Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor)
- [BrowseItemTest.spec.ts](../../e2e/BrowseItemTest.spec.ts)

## Acceptance criteria

- [ ] Page links sit inside a navigation region with a descriptive accessible name.
- [ ] Exactly one visible current-page link is identified when multiple pages exist.
- [ ] Keyboard activation navigates to the intended page and retains active filters.
- [ ] Zero results do not produce a misleading current-page control.

## Suggested approach

1. Inspect rendered HTML and existing NavLink active behavior.
2. Add appropriate navigation and current-page semantics.
3. Add browser assertions for the region and resulting query state.

## Verification and evidence

Run the anonymous browser suite and document a manual Tab/Enter check on the first and second pages. Assert behavior rather than CSS class names alone.

## Hints, in order

1. The browser page number is one-based.
2. Do not assume NavLink's active class also supplies all needed accessibility semantics.

## Review conversation

How did you verify the accessible state rather than only the visual style? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
