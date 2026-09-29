# Learn C# by predicting this code

Learning goal: explain state changes, write a focused test, and read asynchronous code without guessing.

## Objects and invariants

Read [OrderItem](../../src/Ordering.Domain/AggregatesModel/OrderAggregate/OrderItem.cs). Its public properties mostly have private setters. Callers construct an item and use methods such as AddUnits; they cannot freely assign Units.

An invariant is a condition the object must preserve. The constructor rejects units less than or equal to zero. AddUnits rejects negative increments, but currently permits zero. Those are different contracts. Write the input and expected state for each before running anything.

Given unit price 12, quantity 3, and discount 0, Order.GetTotal currently contributes 36. It sums Units times UnitPrice and does not subtract Discount. Do not “correct” pricing based only on the property name; a change to discount semantics requires a product decision and updates to every affected total.

## Classes, records, collections, and null

Compare the OrderItem class with the `BasketQuantity` record in [BasketService](../../src/WebApp/Services/BasketService.cs). A record supports value-oriented equality and a `with` expression that makes a copy with selected changes. BasketState uses that expression to increase quantity.

`IReadOnlyCollection<T>` restricts the collection interface; it does not make every item immutable. A nullable type such as `int?` represents a value that may be absent. The null-forgiving operator `!` suppresses a compiler warning; it does not add a runtime check.

Read `CurrentOrPendingQuantity` in [CartPage](../../src/WebApp/Components/Pages/Cart/CartPage.razor). Determine when a form parameter is assumed to exist. A browser input constraint is useful feedback but cannot guarantee all requests satisfy the assumption.

## A worked characterization test

A characterization test records existing behavior. Adapt this example into the existing OrderAggregateTest class, using that project's imports:

```csharp
[TestMethod]
public void Adding_zero_units_preserves_existing_quantity()
{
    var item = new OrderItem(7, "Practice item", 12m, 0m, "practice.png", 3);

    item.AddUnits(0);

    Assert.AreEqual(3, item.Units);
}
```

This example illustrates the current zero-increment contract; it is not a request to change it. Run the Ordering.UnitTests project, temporarily change the expected value to 4, and verify that the test fails on the quantity assertion. Restore 3 before committing.

Arrange constructs a meaningful starting state. Act invokes one behavior. Assert observes the result. Tests that only assert an object is non-null miss most business errors.

## LINQ: describe versus execute

In [CatalogApi](../../src/Catalog.API/Apis/CatalogApi.cs), `Where` adds predicates to an IQueryable. `OrderBy`, `Skip`, and `Take` describe ordering and pagination. `ToListAsync` asks the provider to execute the query.

In Order.GetTotal, the same LINQ style operates on an in-memory collection. Similar syntax does not imply identical performance or database translation. Materializing every row before filtering changes the amount of data transferred.

Predict a page: names A, B, C, D; page size 2; page index 1. After ordering and skipping two items, the result is C, D. Total count still means all four matching rows, not the two returned.

## Async and cancellation

`Task<T>` represents eventual completion with a T. `await` observes that completion without synchronously blocking the caller's thread. It does not automatically start another thread or make shared state safe.

A CancellationToken is a cooperative signal. It helps only if callers pass it and downstream operations observe it. Do not catch OperationCanceledException and turn it into a successful response.

Inspect `IdentifiedCommandHandler.Handle`: the mediator receives a token, but a broad catch returns default after exceptions. This is a later reliability investigation, not a reason to replace the entire command layer now.

## Practice

Make a table for OrderItem constructor, AddUnits, and SetNewDiscount with boundary values -1, 0, and a valid positive value. Use the source to distinguish present behavior from your proposed policy. Complete stage 2 stories with MSTest and NSubstitute; use [the testing lesson](07-testing-strategy.md) before adding a new test project.
