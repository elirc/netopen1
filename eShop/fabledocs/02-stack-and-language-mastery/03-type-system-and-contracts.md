# Types as Contracts

The theme: in a services system, types are not just compiler food — they are **promises between deployables**. C# gives you several precision dials; this repo uses most of them.

## The dials, with anchors

| Mechanism | Anchor | Contract it expresses |
| --- | --- | --- |
| `record` positional DTOs | `CreateOrderRequest` (`OrdersApi.cs:L171-L185`) | "this is data; equality is structural; shape is the API" |
| `Results<Ok<T>, NotFound, BadRequest<ProblemDetails>>` | `CatalogApi.cs:L171` | full HTTP response union, compile-checked (TS analogue: discriminated unions) |
| Route constraints | `{id:int}`, `{name:minlength(1)}` (`CatalogApi.cs:L36-L46`) | input domain narrowing before code runs |
| Nullable reference types | `int? BuyerId` (`Order.cs:L14`), `string?` claims (`WebApp/Extensions.cs:L111-L123`) | "absence is a legal state here" — and only here |
| `IReadOnlyCollection<T>` exposure | `Order.OrderItems` (`Order.cs:L33`) | "you may look, not touch" — encapsulation as a type |
| Value objects | `Address` via `ValueObject` (`SeedWork/ValueObject.cs`) | equality by content; no identity; immutable |
| Proto contracts | `Basket.API/Proto/basket.proto` | cross-language, versioned by field number |
| Generics with constraints | `IdentifiedCommandHandler<T, R> where T : IRequest<R>` (`IdentifiedCommandHandler.cs:L9-L10`) | "wrap any command, preserve its result type" — the decorator's type signature |
| Source-gen serializer contexts | `BasketSerializationContext` (`RedisBasketRepository.cs:L51-L56`) | serializable-type whitelist, enforced at compile time |

## Where the type system is *not* protecting you (learn to see gaps)

1. **Stringly-typed cross-service contracts.** Integration events serialize to JSON routed by class *name* (`RabbitMQEventBus.cs:L33`). The compiler checks nothing across services — rename `OrderStartedIntegrationEvent` in one service only, and delivery silently stops. Convention, not types, holds the system together at its widest boundary. (TS folks: same as REST between two TS apps without a shared types package.)
2. **The duplicated `CreateOrderRequest`** (`BasketState.cs:L158-L172` vs `OrdersApi.cs:L171-L185`) — two structurally identical records, no shared type, drift caught only at runtime deserialization (missing fields become defaults — *silently*).
3. **Primitive obsession at boundaries:** user ids, product ids, request ids are `string`/`int`/`Guid` everywhere. A `BuyerId` and a `ProductName` can't be swapped, but two `int` ids can. Strongly-typed IDs are the standard remedy; discuss cost/benefit rather than cargo-culting.
4. **`CatalogItem` as both entity and wire type** — one type serving two masters means neither contract is explicit (boundary leak #2).

## Nullability discipline

`#nullable enable` appears explicitly at `OrderingContext.cs:L115` (bottom of file — meaning the file *above* it predates NRT; check `Directory.Build.props` for the global setting). The takeaway skill: read a codebase's nullability *era* — annotations you can trust vs legacy `null` folklore — before trusting any `?`.

Interview angle: "How do you keep two services' contracts in sync?" — ranked answers: shared package (couples deploys) / codegen from OpenAPI-proto (this repo does it for gRPC only) / consumer-driven contract tests (Pact-style; absent here) / discipline + duplication (what Catalog↔WebApp actually does). Knowing all four with this repo's choices mapped = strong mid-level.

Drill: introduce (on paper) a `ProductId` strong type in Basket.API only. List every signature that changes, where the boundary forces a conversion, and whether the proto changes (it must not — why?).
Self-grade — Strong: you identified that the proto is a *frozen* contract and conversions belong at the mapping layer (`BasketService.cs:L77-L110`).
