# Frontend Framework Questions — 10 Cards

The repo's UI is **Blazor Server**. Cards note the React translation where your interview may be React-flavored — the underlying concepts (rendering model, state placement, effects, stale closures) are the same questions in different syntax.

## Q1: Explain Blazor Server's rendering model. What travels over the wire?
Round: frontend.
Repo anchor: `WebApp/Program.cs:L8, L30` (`AddInteractiveServerComponents`, `AddInteractiveServerRenderMode`).
Junior: "the server renders HTML."
Mid: components produce a render tree; on state change the framework diffs old vs new tree and ships *DOM patches* over SignalR; events travel up the same connection. Latency therefore sits inside every interaction.
Senior: contrast with SSR+enhanced-nav (the checkout form works as a plain form post — `[SupplyParameterFromForm]`, `Checkout.razor:L68-L69`), circuit memory cost per user, and when you'd choose WASM/React instead (offline, latency-sensitive, public scale).
React translation: render tree ≈ virtual DOM; the diff is React reconciliation, run server-side.
Drill: 90 seconds aloud.

## Q2: Where should per-user UI state live, and how does this app do it?
Repo anchor: `BasketState` scoped registration (`WebApp/Extensions.cs:L23`) = per-circuit ≈ per-tab session.
Mid: enumerate the options — component parameters (props), scoped DI (context/store), URL, server persistence — and place basket state correctly: scoped DI + server source of truth (Redis), cached locally.
Senior: what dies with the circuit (and why that's acceptable *because* Redis is the truth); the singleton-registration horror story (review kata 8).
React translation: scoped DI ≈ context + React Query cache; the "who is the source of truth" question is identical.

## Q3: How does this app avoid refetching the basket on every render?
Repo anchor: `BasketState.cs:L15, L117-L119` — memoized `Task`.
Mid: caching the Task dedupes concurrent requests (two components asking simultaneously await one fetch); invalidation on mutation (L53).
Senior: the faulted-Task pitfall (a failed fetch is cached until next mutation — annotation drill 5); compare React Query's staleTime/retry machinery — this is a hand-rolled 10% of it, appropriate scale.

## Q4: Walk me through form validation on the checkout page.
Repo anchor: `Checkout.razor:L12-L13` (EditForm + DataAnnotationsValidator), L118-L126 (custom ValidationMessageStore for "cart is empty").
Mid: attribute-driven field validation + imperative custom messages + `editContext.Validate()` gate; and the mandatory line: *client validation is UX; the server revalidates* (FluentValidation layer — module 03/03).
Senior: cross-field/async validation placement, and where this page hardcodes (`CardTypeId = 1`, L113) — a form lying about completeness.
React translation: react-hook-form + zod resolver, same layering.

## Q5: How do live order-status updates reach the page?
Repo anchor: `WebApp/Extensions.cs:L43-L51` (bus subscriptions), `OrderStatusNotificationService`, `OrdersRefreshOnStatusChange.razor`.
Mid: server consumes RabbitMQ events → notifies the right user's circuit → component re-renders. No polling.
Senior: scaling problem (multi-node WebApp: which node holds the user's circuit? — ticket M10's spike), and the honest alternative ladder: polling < SSE/SignalR from the API < web tier on the bus.
React translation: the exact same architecture question as "WebSocket updates into a React app" — where does fan-out live?

## Q6: What is `@key` / list identity for, and where does this repo get it wrong-ish?
Repo anchor: `BasketItem.Id = Guid.NewGuid()` with a TODO (`BasketState.cs:L138`, ticket 5).
Mid: diffing needs stable identity to reuse DOM/preserve element state; a fresh GUID per fetch defeats reuse (rows rebuilt, focus/animation lost).
React translation: identical to `key={index}`/`key={Math.random()}` bugs. The strongest possible answer cites a *real TODO in a Microsoft repo* — memorable.

## Q7: Authentication in the UI: how does a component know who you are?
Repo anchor: `AuthenticationStateProvider` + cascading auth state (`WebApp/Extensions.cs:L90-L91`), `[Authorize]` on Checkout (`Checkout.razor:L6`), claims read at `Extensions.cs:L111-L123`.
Mid: cascading auth state ≈ auth context; `[Authorize]` gates the route; claims prefill the address form (`Checkout.razor:L85-L99`).
Senior: page-level authZ is not API authZ (defense in depth — the API re-checks); anti-forgery for the form posts (`WebApp/Program.cs:L24`).

## Q8: Why is there a `product-images` route on the web app instead of `<img src="http://catalog-api/...">`?
Repo anchor: `WebApp/Program.cs:L32` (`MapForwarder`).
Mid: the browser can't reach internal service names; the WebApp proxies. Also centralizes caching headers and hides topology.
Senior: this is a mini-BFF; at scale you'd push images to CDN/blob storage and this route becomes a redirect — a nice "evolve this design" mini-answer.

## Q9: Component communication: how does adding to cart update the header badge?
Repo anchor: `BasketState.NotifyOnChange` (`BasketState.cs:L26-L31`) — subscription with `IDisposable` cleanup; `Task.WhenAll` fan-out (L111-L112).
Mid: shared service + pub/sub beats parameter drilling for cross-cutting state; disposal prevents leaked subscriptions (the `Dispose` pattern at L151-L155).
React translation: context value change vs external store subscription (`useSyncExternalStore` — this IS that, hand-rolled).
Senior: what happens if a subscriber throws inside `WhenAll`? (One faulted callback fails the whole notify — does any caller handle it? Check. Good "read the edge" follow-up.)

## Q10: Accessibility and semantics — what would you audit first on this storefront?
Repo anchor: `Checkout.razor:L17-L51` (labels wrap inputs — good), the cart's quantity controls and `role="presentation"` on decorative images (L55).
Mid: labels/roles/focus order/validation-message association (`ValidationMessage` renders near the field — is it aria-linked? inspect).
Senior: a11y as acceptance criteria in the e2e layer (Playwright + axe) — one sentence that upgrades the whole answer.
Conceptual — thin repo anchor; be honest that this sample wasn't a11y-audited, and that *saying so* (evidence over vibes) is itself the senior behavior.
