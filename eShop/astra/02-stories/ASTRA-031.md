# ASTRA-031: Characterize catalog stock arithmetic

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 6 — Persistence and domain rules  
**Type:** Domain testing · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-030](ASTRA-030.md)  
**Read first:** [Stage lesson](../01-lessons/06-data-and-domain.md)

## User story

As an inventory maintainer, I want executable examples of stock behavior so that later fixes preserve capacity and removal rules.

## Starting point and scope

No dedicated Catalog.UnitTests project exists. Propose a small MSTest project following the testing lesson, or justify an existing compatible test location without starting a database for pure model tests.

- [CatalogItem.cs](../../src/Catalog.API/Model/CatalogItem.cs)
- [Directory.Build.props](../../tests/Directory.Build.props)
- [Ordering.UnitTests.csproj](../../tests/Ordering.UnitTests/Ordering.UnitTests.csproj)
- [eShop.Web.slnf](../../eShop.Web.slnf)

## Acceptance criteria

- [ ] Removing fewer than available units returns the request and updates stock.
- [ ] Removing more than available returns only the available amount.
- [ ] Empty stock and non-positive removal follow current exception behavior.
- [ ] Adding beyond capacity returns only the actual increment and preserves the maximum.

## Suggested approach

1. Write a stock input/output table including 3 available and 5 requested.
2. Create the smallest justified discoverable unit-test setup.
3. Assert returned values and resulting stock independently.

## Verification and evidence

Run the chosen pure test project and confirm the web solution discovers any new project. Do not claim these tests exercise the paid-order handler or database concurrency.

## Hints, in order

1. The return value is actual movement, not remaining stock.
2. Model comments can describe behavior that the method does not implement.

## Review conversation

Why is a database unnecessary for these cases? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
