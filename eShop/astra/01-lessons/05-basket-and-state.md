# Understand the basket across its boundaries

Learning goal: distinguish protocol validation, persistence, UI state, and catalog enrichment.

## Follow the data

1. [ItemPage](../../src/WebApp/Components/Pages/Item/ItemPage.razor) submits an add action.
2. [BasketState](../../src/WebApp/Services/BasketState.cs) fetches quantities, increments an existing product or adds a row, and calls the basket client.
3. [WebApp BasketService](../../src/WebApp/Services/BasketService.cs) constructs a protobuf request.
4. [gRPC BasketService](../../src/Basket.API/Grpc/BasketService.cs) obtains the user identity from the call context and maps the request.
5. [RedisBasketRepository](../../src/Basket.API/Repositories/RedisBasketRepository.cs) replaces the serialized basket under a user-specific key.

The [proto file](../../src/Basket.API/Proto/basket.proto) is the wire contract. Product ID is field 2 and quantity is field 6. Those numbers are identifiers, not positions to tidy up. Changing an existing field number can break serialized compatibility.

## Ownership belongs to the caller's identity

GetBasket permits an anonymous call and returns an empty response when no user is present. Update and delete throw an Unauthenticated gRPC status when identity is absent. Tests need to construct the expected user context rather than placing a buyer ID into a request body.

A direct service unit test exercises these checks and mapping. It does not prove authentication middleware accepts or rejects real tokens.

## Validation belongs before mutation

The service currently maps update rows without quantity or product-ID bounds. Stage 5 proposes positive IDs, quantities from 1 to 99, and rejection of duplicate product IDs within a single update. A valid empty item list remains a supported way to represent an empty basket.

Zero quantity in the UI has another meaning: BasketState removes the row before sending the replacement list. Do not accidentally break that behavior by assuming the gRPC request contains a zero-quantity row.

Validate the whole request before calling the repository. Otherwise an invalid second row could produce a partial mutation. An important test asserts that invalid input causes no repository write.

## A cache of a Task is still a cache

BasketState stores `Task<IReadOnlyCollection<BasketItem>>?`. It reuses work during its lifetime, including a failed task if the failure remains cached. AddAsync and SetQuantityAsync invalidate the cache. DeleteBasketAsync currently delegates to the service without the same invalidation and notification.

A cache fix needs at least three observations: the state before mutation, the successful operation, and the subsequent read or subscriber notification. Decide what happens if the remote operation fails before clearing useful state.

Do not infer cross-request lifetime from the field alone. Inspect its scoped DI registration and the actual rendering mode.

## Missing catalog rows

The basket stores references to products. FetchCoreAsync fetches catalog items, creates a dictionary, and indexes it by each basket product ID. If a referenced product disappeared, that indexing can fail.

The course's proposed behavior is to explain unavailable products and allow removal while keeping purchasable rows usable. Define whether the unavailable row contributes to the total and whether checkout is blocked until it is removed. Do not silently turn a missing product into a free item.

## Concurrency is a later concern

Two tabs can each read an old basket and replace it with different updates. Fixing a local cache does not solve that lost update. Stage 11 asks for a design experiment around conditional writes or server-side operations. Keep early validation stories separate from that redesign.

For tests of WebApp BasketState, no dedicated WebApp unit-test project exists in this baseline. The testing lesson explains how to propose a small test seam or use a browser test without pretending that harness already exists.
