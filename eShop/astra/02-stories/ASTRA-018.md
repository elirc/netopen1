# ASTRA-018: Normalize invalid UI page numbers

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 3 — Blazor and accessible UI  
**Type:** UI input handling · **Estimate:** 2-4 hours  
**Prerequisites:** [ASTRA-017](ASTRA-017.md)  
**Read first:** [Stage lesson](../01-lessons/03-blazor-and-browser.md)

## User story

As a shopper following a malformed catalog URL, I want a predictable first page so that invalid page numbers do not break browsing.

## Starting point and scope

Proposed UI policy: page values below 1 use page 1; valid positive values retain their meaning. API validation is a separate stage.

- [Catalog.razor](../../src/WebApp/Components/Pages/Catalog/Catalog.razor)
- [BrowseItemTest.spec.ts](../../e2e/BrowseItemTest.spec.ts)

## Acceptance criteria

- [ ] Page zero and a negative page display first-page results without sending a negative API offset.
- [ ] An omitted page still displays page 1.
- [ ] Page 2 still requests the second page.
- [ ] The active-page presentation agrees with the effective page; non-integer binding behavior is documented separately.

## Suggested approach

1. Reproduce page=0 and page=-1 on the baseline.
2. Normalize the effective numeric page at the UI boundary.
3. Test the rendered results and navigation state.

## Verification and evidence

Run the anonymous browser suite and build the web filter. Explain whether the URL is canonicalized or the value is normalized only for use.

## Hints, in order

1. GetValueOrDefault(1) does not clamp a provided zero.
2. Avoid silently clamping valid large pages to page 1.

## Review conversation

Where should a non-integer query be handled compared with a negative integer? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
