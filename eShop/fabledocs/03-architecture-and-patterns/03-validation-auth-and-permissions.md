# Validation, Auth, and Permissions

## The four validation layers (checkout as the worked example)

| Layer | Where | Example | Job | If it's missing |
| --- | --- | --- | --- | --- |
| 1. UI form | `Checkout.razor:L12-L13` DataAnnotations + custom "cart not empty" (L118-L126) | required address fields | fast feedback; UX | server still safe — never rely on it |
| 2. Transport/model | route constraints `{id:int}` (`CatalogApi.cs:L36`), header GUID check (`OrdersApi.cs:L27-L30`, L132-L136), explicit `id <= 0` guard (`CatalogApi.cs:L176-L181`) | malformed input → 400 ProblemDetails | reject garbage before any work | handlers crash on nonsense |
| 3. Command validation | FluentValidation via `ValidatorBehavior.cs:L20-L34`; rules in `CreateOrderCommandValidator.cs:L6-L16` (card 12–19 digits, CVV length 3, non-empty items, expiry-in-future) | semantic validity of the *request* | business-shaped 4xx errors | invalid commands reach the domain |
| 4. Domain invariants | `OrderItem` ctor throws on negative units / discount exceeding total (proven by `OrderAggregateTest.cs:L31-L43`); status guards (`Order.cs:L99-L153`) | things that must *never* be false | the last line; protects data even from buggy internal callers | corrupt data, forever |

Transferable rule: layers 1–3 are *courtesy*; layer 4 is *law*. A senior asks of any write path: "what enforces this when the API is bypassed?" (e.g., an event handler calling `SetPaidStatus` — layer 4 still holds).

Note the failure shape of layer 3: `ValidatorBehavior` **throws** `OrderingDomainException`, and `IdentifiedCommandHandler.cs:L99-L102` catches everything and returns `default` → the API returns 200 with a warning log (`OrdersApi.cs:L157-L166`). Validation failures are thus *invisible to the client* on the create-order path. Confirmed by reading; a top-tier discussion finding.

## AuthN: who are you?

- **Identity.API** (Duende IdentityServer) is the single token issuer. Scopes: `orders`, `basket`, `webhooks` (`Identity.API/Configuration/Config.cs:L18-L24`); one client registration per app (L44+).
- **WebApp**: cookie session + OIDC code flow (`WebApp/Extensions.cs:L66-L87`), `SaveTokens=true`, then relays the access token to APIs via `.AddAuthToken()` (L32, L36, L40).
- **APIs**: JWT bearer via shared helper `AuthenticationExtensions.cs:L33-L50`. Identity = `sub` claim, preserved raw by `DefaultInboundClaimTypeMap.Remove("sub")` (L31 there; same in WebApp `Extensions.cs:L58`).
- **`ValidateAudience = false`** (`AuthenticationExtensions.cs:L49`) even though an audience is configured. Consequence: a token acquired for the basket scope validates at Ordering too. In this sample all clients get all scopes anyway; in a real system this flattens a security boundary. *Possible risk — flagged in the risk register.*

## AuthZ: what may you do?

The honest answer: **authorization here is thin** — mostly "authenticated or not", plus *isolation by construction*:

- Basket: the storage key IS the caller's `sub` (`BasketService.cs:L15`, `RedisBasketRepository.cs:L16`). You cannot name another user's basket — no check needed because no parameter exists. This is the strongest authZ style: make the violation *inexpressible*.
- Orders list: scoped by identity server-side (`OrdersApi.cs:L93-L98` — user id from token, not from the query).
- **Order detail: `GetOrderAsync(orderId)` (`OrdersApi.cs:L80-L91`) takes an integer id and does not verify ownership** in the endpoint. Whether `GetOrderAsync` filters by buyer internally — check `Application/Queries/OrderQueries.cs`. If it doesn't, any authenticated user can read any order by guessing sequential ints: textbook **IDOR** (Insecure Direct Object Reference). *Investigate before claiming — this is the module's homework.*
- **Catalog writes: no authorization at all** (`CatalogApi.cs:L93-L110` — create/update/delete are open). Fine inside a demo network; the #1 ticket in contribution practice.

## What a junior misses vs what a senior checks

Junior misses: that authN ≠ authZ; that `[Authorize]` on the Blazor page (`Checkout.razor:L6`) protects the *page*, not the API — the API must re-check (defense in depth: it does, via JWT).
Senior checks, in order: (1) every endpoint taking a resource id — is ownership enforced? (2) every write endpoint — is *any* auth enforced? (3) token validation params — issuer/audience/lifetime; (4) what's in the token (claims) vs what's looked up server-side.

Interview angle: "How would you prevent users reading each other's data?" Ranked answers: filter-by-owner-in-query (orders list) < explicit ownership check < *keying by identity so the question can't arise* (basket). Presenting all three from one codebase is a strong mid-level answer.

Drill: audit `GetOrderAsync` end to end (endpoint → `OrderQueries` → SQL). Verdict: IDOR or safe? Produce the one-paragraph finding with anchors, as if for a security review.
Self-grade — Basic: correct verdict with the query file cited. Solid: proposes the minimal fix (add `userId` parameter to the query's WHERE). Strong: also proposes the test proving it (two users, cross-fetch, expect 404-not-403 and explains why 404 leaks less).
