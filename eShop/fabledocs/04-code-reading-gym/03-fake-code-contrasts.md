# Fake-Code Contrasts

Ten pairs. Every snippet below is **fake** (labeled per house rules); each pair is tied to a real pattern in this repo. Read the bad one, articulate the smell *before* reading the better one.

---

## 1. Coupling UI shape to DB shape

```csharp
// Illustrative fake code: not from this repo
app.MapGet("/items/{id}", (AppDb db, int id) => db.Items.Find(id)); // returns entity w/ CostPrice, SupplierId...
```

```csharp
// Illustrative fake code: not from this repo
app.MapGet("/items/{id}", async (AppDb db, int id) =>
    await db.Items.Where(i => i.Id == id)
        .Select(i => new ItemDto(i.Id, i.Name, i.Price)) // explicit contract
        .SingleOrDefaultAsync() is { } dto ? Results.Ok(dto) : Results.NotFound());
```

Repo tie: Catalog returns entities directly (`CatalogApi.cs:L158`) — works because `CatalogItem` has no secret fields *today*. The bad version is that same choice after someone adds `CostPrice`.

## 2. Missing permission filter (IDOR)

```csharp
// Illustrative fake code: not from this repo
app.MapGet("/orders/{id}", (OrderDb db, int id) => db.Orders.Find(id)); // any user, any order
```

```csharp
// Illustrative fake code: not from this repo
app.MapGet("/orders/{id}", (OrderDb db, ClaimsPrincipal user, int id) =>
    db.Orders.SingleOrDefault(o => o.Id == id && o.BuyerSub == user.FindFirstValue("sub"))
        is { } o ? Results.Ok(o) : Results.NotFound()); // 404, not 403: don't confirm existence
```

Repo tie: the open question on `OrdersApi.cs:L80-L91` (R5). Contrast with basket's key-by-identity which makes the bug inexpressible.

## 3. N+1 query

```csharp
// Illustrative fake code: not from this repo
var orders = await db.Orders.ToListAsync();
foreach (var o in orders)
    o.Buyer = await db.Buyers.FindAsync(o.BuyerId); // 1 + N round trips
```

```csharp
// Illustrative fake code: not from this repo
var orders = await db.Orders.Include(o => o.Buyer).ToListAsync(); // 1 query (join)
```

Repo tie: `CatalogApi.cs:L183` (`Include`) and the WebApp's batch endpoint usage — `GetCatalogItems(productIds)` (`BasketState.cs:L132`) hitting `items/by?ids=` (`CatalogApi.cs:L162-L168`) instead of one call per basket line. The batch endpoint is the *cross-service* N+1 fix; know both radii.

## 4. Client-trusted price

```csharp
// Illustrative fake code: not from this repo
public record AddToCartRequest(int ProductId, int Qty, decimal Price); // client says what it costs
order.AddItem(req.ProductId, req.Price, req.Qty);
```

```csharp
// Illustrative fake code: not from this repo
var product = await catalog.GetItem(req.ProductId);      // server resolves price
order.AddItem(product.Id, product.Price, req.Qty);
```

Repo tie: proto `BasketItem` carries no price (`BasketService.cs:L83-L87`); prices re-fetched in `BasketState.cs:L132-L141`. (Nuance to discuss: WebApp *is* a server — its resolved prices going into `CreateOrderRequest` are trusted by Ordering. Is the WebApp inside the trust boundary? Here, yes. Say why.)

## 5. Dual write (no outbox)

```csharp
// Illustrative fake code: not from this repo
await db.SaveChangesAsync();          // committed
await bus.PublishAsync(evt);          // process dies here → world never learns
```

```csharp
// Illustrative fake code: not from this repo
await eventLog.SaveEventAsync(evt, tx);   // same transaction as data
await tx.CommitAsync();
await outboxPublisher.PublishPending(tx.Id); // safe to retry; consumers idempotent
```

Repo tie: `CatalogApi.cs:L350-L356`, `TransactionBehavior.cs:L38-L52`.

## 6. Swallowed errors

```csharp
// Illustrative fake code: not from this repo
try { return await ProcessAsync(cmd); }
catch { return default; }             // caller sees "false", logs see nothing
```

```csharp
// Illustrative fake code: not from this repo
try { return await ProcessAsync(cmd); }
catch (ValidationException ex) { throw; }              // expected: let middleware map to 400
catch (Exception ex) { logger.LogError(ex, "…{CommandId}", cmd.Id); throw; } // bugs: visible, 500
```

Repo tie: this bad shape is **real** at `IdentifiedCommandHandler.cs:L99-L102` (R3). Being able to say "the reference app itself does this, and here's the blast radius" is the whole point of this gym.

## 7. Side effect inside the transaction

```csharp
// Illustrative fake code: not from this repo
using var tx = await db.BeginTransactionAsync();
await db.SaveChangesAsync();
await emailClient.SendReceiptAsync(order);  // 3rd-party call inside DB transaction
await tx.CommitAsync();                     // email sent even if commit fails; tx held open for seconds
```

```csharp
// Illustrative fake code: not from this repo
// inside tx: save order + outbox row "SendReceipt"
// after commit: worker consumes outbox → sends email → marks done
```

Repo tie: domain event handlers run pre-commit (`OrderingContext.cs:L47-L62`) — safe only while they stay DB-only. The bad version is what happens when someone "just adds" an email there.

## 8. Stale cached state / missing invalidation

```csharp
// Illustrative fake code: not from this repo
private IReadOnlyCollection<BasketItem>? _items;
public async Task Checkout() { await ordering.CreateOrder(...); await basket.Delete(); }
// _items still shows the old basket; header badge stays "3"
```

```csharp
// Illustrative fake code: not from this repo
public async Task Checkout() { await ordering.CreateOrder(...); await basket.Delete();
    _items = null; await NotifySubscribersAsync(); }
```

Repo tie: `BasketState.AddAsync` does invalidate+notify (`BasketState.cs:L53-L55`); `CheckoutAsync` (L78-L109)… check whether it does. (It calls `DeleteBasketAsync` at L108 — find the invalidation. This contrast is drawn from scenario 1 in systematic debugging.)

## 9. `any`-equivalent: losing the type at the boundary

```csharp
// Illustrative fake code: not from this repo
var evt = JsonSerializer.Deserialize<object>(message);   // now what?
dynamic e = evt; Process(e.OrderId);                       // runtime roulette
```

```csharp
// Illustrative fake code: not from this repo
if (!subscriptions.TryGetValue(eventName, out var eventType)) { log; return; }
var evt = (IntegrationEvent?)JsonSerializer.Deserialize(message, eventType, options);
```

Repo tie: the good shape is literally `RabbitMQEventBus.ProcessEvent` (`:L192-L207`) — unknown event names logged and skipped, known ones deserialized to their real type.

## 10. Casual public-contract change

```csharp
// Illustrative fake code: not from this repo
// PR title: "cleanup: rename PaginatedItems.Data to Items" — merged Friday
public record PaginatedItems<T>(int PageIndex, int PageSize, long Count, IEnumerable<T> Items);
```

```csharp
// Illustrative fake code: not from this repo
// v2 group gets the new shape; v1 keeps the old one until consumers migrate
v2.MapGet("/items", GetAllItemsV2Shape);
```

Repo tie: the v1/v2 machinery exists for exactly this (`CatalogApi.cs:L15-L30`); the mobile BFF and MAUI apps are the consumers you'd break. "Which of my types are wire types?" is the pre-merge question — in Catalog the answer is "the entities too," which is why contrast #1 matters.

---

Drill: for each pair, write the one-sentence review comment you'd leave on the bad version — specific, kind, actionable (see [../07-career-and-collaboration/01-code-review-mindset.md](../07-career-and-collaboration/01-code-review-mindset.md)). Self-grade: your comment names the failure scenario, not just the rule.
