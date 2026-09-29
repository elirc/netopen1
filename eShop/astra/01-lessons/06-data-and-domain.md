# Preserve database behavior and domain rules

Learning goal: distinguish data mapping, query behavior, and business invariants.

## Two different modeling styles

Catalog has a mutable [CatalogItem](../../src/Catalog.API/Model/CatalogItem.cs) and a [CatalogContext](../../src/Catalog.API/Infrastructure/CatalogContext.cs). Ordering has an aggregate root, [Order](../../src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs), which controls its item collection and status transitions.

An aggregate is a boundary for business consistency. Only Order.AddOrderItem changes its collection through the intended public API. A database entity configuration describes persistence, not every business rule. Read both the class and its entity configuration before changing a stored property.

## Stock behavior to predict

RemoveStock throws when stock is empty or the requested quantity is not positive. When the request exceeds available stock, it removes what exists and returns the amount actually removed. With available 3 and request 5, the result is 3 and remaining stock is 0.

AddStock caps the resulting amount at MaxStockThreshold, resets OnReorder, and returns the actual increment. It currently lacks an explicit negative-quantity guard. A story proposes rejecting negative input while allowing zero. Preserve the capacity cap and clarify the effect on OnReorder at zero.

The source comment mentions a restock request, but the method does not emit one. Read the executed code before describing it as a capability.

## Transaction and event timing

Read [OrderingContext](../../src/Ordering.Infrastructure/OrderingContext.cs), [TransactionBehavior](../../src/Ordering.API/Application/Behaviors/TransactionBehavior.cs), and [OrderingIntegrationEventService](../../src/Ordering.API/Application/IntegrationEvents/OrderingIntegrationEventService.cs).

A database transaction groups local database operations. It does not automatically include Redis, RabbitMQ, another database, or the user's browser. Integration-event log entries help retain publish intent with data changes. Delivery and retry still need separate reasoning.

Trace SaveEntitiesAsync and domain-event dispatch in the actual implementation rather than relying on historical comments about whether events run before or after a save.

## Query shape matters

[OrderQueries](../../src/Ordering.API/Application/Queries/OrderQueries.cs) uses EF Core in this checkout. Do not copy an older eShop tutorial describing this file as Dapper. List queries project summaries; detail queries include order items.

For read-only queries, consider whether tracking is needed. Measure before making a performance claim. A projection and AsNoTracking can solve different problems, and neither fixes a missing ownership predicate.

Pagination should filter and sort on the server before Skip and Take. Sorting only by a non-unique name needs a tie-breaker. Loading every row first may pass a small test and still be a poor query.

## A schema-change rehearsal

Use an optional nullable merchandising note as a practice field. Decide the maximum length, API exposure, and default for existing rows before generating a migration. Update the model, entity configuration, migration, snapshot, and any request mapping that intentionally exposes it.

Find any local dotnet-ef tool manifest before installing a tool. Select a version compatible with the repository's EF packages. Use an explicit project and startup project, and ensure the design-time context has local connection configuration. Do not invent a working migration command until you have inspected how this context is constructed.

Verify on a disposable local database: apply to an existing seeded schema, preserve existing rows, save and read the new value, and describe rollback data loss. Startup migrations in this sample are convenient for local learning; they are not evidence of a reviewed production migration process.

## State-machine lab

List all OrderStatus values. For each transition method, record valid starting states and whether an invalid call throws or leaves the state unchanged. These behaviors differ between methods. Use unit tests to preserve the observed contract before proposing a more uniform one.
