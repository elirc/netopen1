# Trace Tables

Fill the table yourself first (columns: step, file:line, value/shape at this point, owner, transformation, risk). Then compare with the filled versions. The discipline is writing the **value shape** at each hop — that's where misunderstandings hide.

## Trace 1 (UI → API): "user clicks + on a cart line"

Fill in from `CartPage.razor` → `BasketState.SetQuantityAsync` → gRPC → Redis. Filled reference:

| Step | File | Value shape | Owner | Transformation | Risk |
| --- | --- | --- | --- | --- | --- |
| 1 | `WebApp/.../CartPage.razor` | click event, productId:int, newQty:int | UI | DOM event → C# call over circuit | circuit latency per click |
| 2 | `BasketState.cs:L58-L76` | `List<BasketItem>` (with prices) | WebApp | mutate row / remove if qty≤0; rebuild `List<BasketQuantity>` (prices dropped) | read-modify-write race |
| 3 | `BasketState.cs:L73` | `List<BasketQuantity>` | WebApp | → proto `UpdateBasketRequest` in `BasketService` (WebApp side) | full-basket replace |
| 4 | `Basket.API/Grpc/BasketService.cs:L36-L50` | `UpdateBasketRequest` | Basket.API | + userId from token → `CustomerBasket` | unauthenticated → RpcException |
| 5 | `RedisBasketRepository.cs:L36-L37` | UTF-8 JSON bytes | Basket.API | serialize; `SET /basket/{sub}` | last-writer-wins |
| 6 | `RedisBasketRepository.cs:L47` | `CustomerBasket` (re-read) | Basket.API | deserialize | extra round trip |

Question the table answers that prose hides: prices enter at step 2 and *leave* at step 3 — the server never sees them.

## Trace 2 (persistence): "CreateOrderCommand → rows in orderingdb"

Do it yourself from `TransactionBehavior.cs` inward. Key rows for the reference: transaction begins (`TransactionBehavior.cs:L38`); outbox row staged (`CreateOrderCommandHandler.cs:L32-L33` — shape: `IntegrationEventLogEntry` with serialized JSON + transactionId); aggregate built in memory (`Order.cs:L52-L65` — shape: Order{Submitted, events:[OrderStarted]}); domain events dispatched **pre-save** (`OrderingContext.cs:L55` — Buyer aggregate created/loaded by handlers, joins same change set); one `SaveChangesAsync` (L59) flushes orders+items+buyer+outbox; commit (`TransactionBehavior.cs:L47`); publish (L52 — shape: JSON bytes on the wire, routing key `"OrderStartedIntegrationEvent"`).
Risk column highlights: steps 3–5 all inside one transaction (good); step 7's failure leaves `NotPublished` rows (R2).

## Trace 3 (auth): "where does `sub` travel?"

| Step | File | Shape | Risk |
| --- | --- | --- | --- |
| 1 | Identity.API issues tokens | JWT: `sub`, `name`, scopes | — |
| 2 | Cookie stores tokens (`WebApp/Extensions.cs:L80`) | encrypted cookie | cookie size/lifetime |
| 3 | `GetBuyerIdAsync` (`Extensions.cs:L111-L116`) | `string?` sub | null if claim mapping altered |
| 4 | `.AddAuthToken()` handlers (L32-L40) | `Authorization: Bearer …` header | forgetting handler on new client → 401 |
| 5 | JWT middleware (`AuthenticationExtensions.cs:L33-L50`) | ClaimsPrincipal | audience not validated (R6) |
| 6 | `BasketService.cs:L15` / `OrdersApi.cs:L95` | userId string | identity becomes a *storage key* / query filter |

The senior observation to make: `sub` changes *meaning* at step 6 — from "claim" to "primary key." Everything downstream trusts that transformation.

## Trace 4 (error): "validation failure on create order"

Trace an invalid card (5 digits) from POST to response. Reference chain: `OrdersApi.cs:L146` → ValidatorBehavior throws `OrderingDomainException` (`ValidatorBehavior.cs:L28-L34`) → caught by… trace carefully: TransactionBehavior wraps ValidatorBehavior or vice versa? (Check registration order in `Ordering.API/Extensions/Extensions.cs` — the drill.) → `IdentifiedCommandHandler.cs:L99-L102` catch → `default(bool)` = false → `OrdersApi.cs:L157-L166` → **200 OK**. Value shapes: exception → false → Ok(). Each hop *loses information*. That's the table's lesson: draw where error detail dies.

## Trace 5 (async): "GracePeriodConfirmed → order AwaitingValidation"

Build it across four files: poller SQL (`GracePeriodManagerService.cs:L69-L74`, shape: `List<int>` order ids) → event publish (L53-L60, shape: `GracePeriodConfirmedIntegrationEvent{OrderId}`) → RabbitMQ (routing key = class name) → Ordering's handler (`GracePeriodConfirmedIntegrationEventHandler.cs`) → `SetAwaitingValidationOrderStatusCommand` → `Order.SetAwaitingValidationStatus` (`Order.cs:L99-L106`, guard: only-from-Submitted) → new outbox event `OrderStatusChangedToAwaitingValidation` → Catalog + WebApp consume.
Risk column: duplicate events every poll cycle (by design) absorbed at the guard; the WebApp consumer updates any open Orders page.

---

Transferable: trace tables are how you review PRs that "look fine" — you stop reading *code* and start reading *data*. Two of these five (Traces 2 and 4) become timed interview sims in module 08.
