# Domain Glossary

Product/domain nouns, where they live in code, and the near-synonyms that trip people up.

| Term | Meaning here | Code home |
| --- | --- | --- |
| **Catalog item** | A sellable product: name, price, brand, type, stock counters, picture, embedding | `src/Catalog.API/Model/CatalogItem.cs` |
| **Brand / Type** | Lookup dimensions for filtering | `CatalogBrand.cs`, `CatalogType.cs`; endpoints `CatalogApi.cs:L77-L90` |
| **AvailableStock / RestockThreshold / MaxStockThreshold** | Inventory counters on the item itself (no separate inventory service) | `CatalogItem.cs`; checked in `OrderStatusChangedToAwaitingValidationIntegrationEventHandler.cs:L20` |
| **Basket** | Per-user list of (ProductId, Quantity) in Redis, keyed by identity. No prices stored | `src/Basket.API/Model/CustomerBasket.cs`, `RedisBasketRepository.cs:L13-L16` |
| **BuyerId (basket)** | The JWT `sub` claim — a string user id | `BasketService.cs:L15` |
| **Buyer (ordering)** | An *aggregate* in Ordering with payment methods; created on first order via domain event | `src/Ordering.Domain/AggregatesModel/BuyerAggregate/` |
| **Order** | Aggregate root: address, items, status, buyer/payment links | `OrderAggregate/Order.cs` |
| **OrderItem** | Line inside an Order: snapshot of product name/price/discount at purchase time | `OrderAggregate/OrderItem.cs` |
| **OrderStatus** | Submitted → AwaitingValidation → StockConfirmed → Paid → Shipped; Cancelled | transitions in `Order.cs:L99-L168` |
| **Grace period** | Window after submission during which an order can be cancelled before processing begins | `OrderProcessor/Services/GracePeriodManagerService.cs`, `BackgroundTaskOptions.cs` |
| **Domain event** | In-process fact within Ordering, dispatched via MediatR before save | `Ordering.Domain/Events/`, dispatch `MediatorExtension.cs:L5-L20` |
| **Integration event** | Cross-service fact on RabbitMQ, JSON, routed by class name | `*/IntegrationEvents/Events/`, bus `RabbitMQEventBus.cs` |
| **Integration event log / outbox** | DB table recording events pending publication, same transaction as business data | `IntegrationEventLogEF/` |
| **IdentifiedCommand / ClientRequest** | Idempotency wrapper + the DB record of seen request ids | `IdentifiedCommand.cs`, `Ordering.Infrastructure/Idempotency/` |
| **Webhook** | Outbound HTTP callback to third-party subscribers on order events | `src/Webhooks.API/`, demo consumer `src/WebhookClient/` |
| **Embedding / semantic relevance** | pgvector similarity search over catalog items (optional AI feature) | `CatalogApi.cs:L237-L289`, `Catalog.API/Services/CatalogAI.cs` |

## Confusables

- **Basket vs Cart:** same thing. UI says "shopping bag" (`CartPage.razor`), services say Basket. Don't invent a third name.
- **Basket BuyerId (a string `sub`) vs Ordering BuyerId (an `int?` FK to the Buyer aggregate)** — `Order.cs:L14`. Same human, two representations, two services.
- **Order draft vs Order:** `CreateOrderDraftAsync` (`OrdersApi.cs:L106-L116`) computes totals without persisting; `Order.NewDraft()` (`Order.cs:L37-L44`) sets `_isDraft` which — per its own comment — is never checked. *Legacy-ish corner; don't build on it.*
- **Domain event vs integration event:** in-process + same transaction vs cross-service + after commit. The single most quoted distinction in eShop-derived interviews.
- **BasketItem (WebApp) vs BasketItem (proto) vs OrderItem:** three shapes for "a line item," deliberately different per boundary. The WebApp one carries price; the proto one doesn't; the domain one snapshots price forever.
- **`webapp` (OIDC client id) vs WebApp (project):** the string in `Identity.API/Configuration/Config.cs` must match `Extensions.cs:L77`. Renaming one without the other breaks login — config drift, not a compile error.

Transferable: every codebase has a glossary like this in the founders' heads. Building it explicitly — especially the *confusables* — is how you stop writing bugs caused by two things sharing one name.
