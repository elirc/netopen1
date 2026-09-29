# C#/.NET Deep-Dive — 14 Question Cards

(The curriculum template calls this the "JS/TS/Node deep-dive"; adapted for this stack. If your loop includes Node, the crossover notes on cards 1, 2, and 5 map each concept to its JS equivalent.)

---

## Q1: Explain async/await in .NET. What actually happens at an `await`?
Round: deep-dive.
What it's really testing: do you know it's about *freeing threads*, not parallelism.
Repo anchor: `src/Catalog.API/Apis/CatalogApi.cs:L149-L156` — two sequential awaits (count, then page); the request thread is released to the pool during each DB round trip.
Junior answer sounds like: "await waits for the task to finish."
Mid-level adds: the method is split into a continuation; the thread returns to the thread pool; in ASP.NET Core there's no `SynchronizationContext`, so continuations run on any pool thread — this is why one server handles thousands of concurrent requests with dozens of threads.
Senior includes: sync-over-async (`.Result`) as the thread-pool-starvation classic; when awaits should be serial (here: count must precede paging? actually independent — could run concurrently, but EF's DbContext is not thread-safe, so serial is *required* — that's the invariant); `ConfigureAwait(false)` being a library-code concern.
Node crossover: same idea as the event loop freeing the single thread, except .NET has many threads.
Likely follow-ups: "Why is `async void` dangerous?" "What's `ValueTask`?" (see `GracePeriodManagerService.cs:L63` returning `ValueTask<List<int>>`).
Practice drill: explain aloud why `BasketState._cachedBasket` caches a `Task` rather than the result (`BasketState.cs:L117-L119`) — concurrent callers await the *same* in-flight fetch. 90 seconds.

## Q2: DI lifetimes — singleton, scoped, transient. Give a real bug each can cause.
Round: deep-dive.
Repo anchor: `src/WebApp/Extensions/Extensions.cs:L23-L27` — `BasketState` **scoped** (per Blazor circuit = per user session!), `BasketService` **singleton**, `IIntegrationEventLogService` **transient** (`Catalog.API/Extensions/Extensions.cs:L27`).
Junior: recites definitions.
Mid: names the classic bug — captive dependency: a singleton capturing a scoped service (e.g., a singleton holding a DbContext) reuses one context forever: stale data, threading errors. Notes the Blazor twist: "scoped" in Blazor Server means the circuit's lifetime, minutes not milliseconds — which is exactly why per-user basket state can live in a scoped service.
Senior: why `RabbitMQEventBus` (singleton, `IHostedService`) creates a DI **scope per message** (`RabbitMQEventBus.cs:L190`) to resolve scoped handlers — the standard pattern for background consumers; keyed services for handler registration (`:L204`).
Follow-ups: "How would you inject a DbContext into a singleton hosted service?" (IServiceScopeFactory, or `NpgsqlDataSource` like `GracePeriodManagerService` does — no EF at all).
Drill: grep three `AddScoped/AddSingleton/AddTransient` registrations and justify each aloud.

## Q3: What's the difference between `IQueryable` and `IEnumerable`, and why does it matter?
Round: deep-dive / practical coding.
Repo anchor: `CatalogApi.cs:L134-L156` — filters composed on `IQueryable` become SQL WHERE clauses; `Skip/Take` become LIMIT/OFFSET.
Junior: "IQueryable is for databases."
Mid: expression trees vs delegates; the composition at L136-L147 executes as *one* SQL statement at `ToListAsync`; inserting `.AsEnumerable()` before the filters would pull the whole table into memory and filter in C#.
Senior: what can't translate (calling your own C# method in a Where) throws at runtime, not compile time; `LongCountAsync` + page = 2 queries and when that's worth collapsing; deferred execution as both a feature and a foot-gun (a leaked IQueryable executing after the context is disposed).
Drill: predict the SQL for `GetAllItems` with all three filters set, then say where a `maxPrice` filter would land.

## Q4: Records vs classes — when and why?
Round: deep-dive.
Repo anchor: `CreateOrderRequest` record (`OrdersApi.cs:L171-L185`) vs the `Order` entity class (`Order.cs`).
Junior: "records are immutable classes."
Mid: value-based equality + `with` expressions; DTOs/contracts as records (compare-by-content is what you want), entities as classes (identity-based equality — two Orders with equal fields are NOT the same order). Bonus anchor: `items[i] = existing with { Quantity = existing.Quantity + 1 }` (`BasketState.cs:L42`).
Senior: records in EF (possible but fights change tracking); positional records and binder/serializer interplay; `ValueObject` base class (`Ordering.Domain/SeedWork/ValueObject.cs`) as the pre-records way to get structural equality — this repo shows both generations.
Drill: explain why `Address` is a ValueObject subclass and whether a record could replace it.

## Q5: How does exception handling shape an API's contract? When is catching everything wrong?
Round: deep-dive / code review.
Repo anchor: two confirmed real cases — `IdentifiedCommandHandler.cs:L99-L102` (catch-all → `default` → client gets 200 on failure) and `OrdersApi.cs:L82-L90` (`catch` → 404 for *any* error, including DB down).
Junior: "use try/catch and log."
Mid: exceptions vs result types; catch-all at boundaries only, rethrow or translate; these two anchors as anti-examples — swallowing turned a validation failure into a silent success (the ProblemDetails middleware never saw it).
Senior: exception filters, `ProblemDetails` as the RFC 7807 contract (`Catalog.API/Program.cs:L5`), the difference between *expected* failures (model as results/typed responses — `Results<Ok, NotFound>`, see `CatalogApi.cs:L171`) and *bugs* (let them escape to middleware and a 500 + alert).
Node crossover: same debate as returning `null` vs throwing in Express handlers.
Drill: rewrite (aloud) `GetOrderAsync`'s error handling: which exceptions merit 404 vs 500?

## Q6: What is `TypedResults` / `Results<T1,T2>` and why prefer it over `IActionResult`?
Round: deep-dive (.NET-specific).
Repo anchor: `CatalogApi.cs:L171` — `Results<Ok<CatalogItem>, NotFound, BadRequest<ProblemDetails>>`.
Junior: "it returns results."
Mid: the union type makes the endpoint's full response contract *compile-checked* and drives OpenAPI generation — return an undeclared status and it won't compile. Contract-as-types.
Senior: this is the minimal-API analogue of making illegal states unrepresentable; compare TS discriminated unions; note where the repo still lies (the checkout 200-on-failure, R3 in the critique — types can't save you from swallowed exceptions).
Drill: read any endpoint signature and recite its possible HTTP responses without reading the body.

## Q7: How does EF Core change tracking work, and what's it doing in the price-change endpoint?
Round: deep-dive.
Repo anchor: `CatalogApi.cs:L340-L357` — `SetValues`, then `priceEntry.IsModified` decides whether to publish an event; `OriginalValue` supplies the old price at L350.
Junior: "EF saves your changes."
Mid: snapshot tracking — original vs current values per property; `SetValues` marks only actually-changed props; that's what lets business logic hang off "did the price change" without a manual comparison.
Senior: `AsNoTracking` for read paths (missing on Catalog reads — cheap win); attach vs query-then-update; concurrency tokens (absent here — two admins updating one product = last-writer-wins, worth flagging).
Drill: what happens if two concurrent UpdateItem calls race? Walk the tracker state.

## Q8: Explain `IHostedService`/`BackgroundService`. What are the failure modes?
Round: deep-dive.
Repo anchor: `GracePeriodManagerService.cs:L16-L42`; also `RabbitMQEventBus` as an `IHostedService` (`RabbitMQEventBus.cs:L226-L295`) doing its startup on a background thread so it doesn't block app boot.
Junior: "it runs background tasks."
Mid: ExecuteAsync + CancellationToken; an unhandled exception kills the *loop* silently (host keeps running by default) — this repo guards the DB call (`:L87-L92`) so the loop survives.
Senior: scale-out duplication (no leader election — see pattern card 12), graceful shutdown, and why the bus starts consuming on a fire-and-forget `Task.Factory.StartNew` (`:L229`) — startup ordering vs error visibility tradeoff (a connection failure at L289 only logs; the service *appears* healthy — observability gap).
Drill: describe what health check you'd add to detect "consumer never connected."

## Q9: Value types vs reference types; why does `decimal` matter for money?
Round: screen.
Repo anchor: `Order.GetTotal()` (`Order.cs:L185`) — `decimal` arithmetic; `CatalogItem.Price`.
Junior: stack vs heap (mostly wrong framing).
Mid: `decimal` = base-10 floating point, exact for money; `double` accumulates binary rounding errors (0.1 + 0.2 problem — same as JS, which has *only* doubles, hence money-in-cents-as-integers in Node).
Senior: rounding policy (MidpointRounding), where totals should be computed (this repo: on the aggregate; DB can disagree if computed there too), currency as a missing concept here.
Drill: 30-second version aloud.

## Q10: What are source generators doing in this repo's serialization?
Round: deep-dive (senior-flavored).
Repo anchor: `RedisBasketRepository.cs:L51-L56` — `BasketSerializationContext : JsonSerializerContext`; also `Basket.API/Extensions/Extensions.cs:L24-L28` for the event context.
Junior: (usually blank — fine, say what it is.)
Mid: compile-time generated serializers: no reflection, AOT/trimming-safe, faster startup; the `[JsonSerializable(typeof(CustomerBasket))]` attribute drives it.
Senior: the tradeoff — every serializable type must be declared; the event bus keeps a resolver *chain* so each service adds its event types (`ConfigureJsonOptions ... TypeInfoResolverChain`); relate to the `UnconditionalSuppressMessage` trimming annotations in `RabbitMQEventBus.cs:L210-L224`.
Drill: add (on paper) a new event type to Basket's subscriptions — which two places change?

## Q11: `Task.WhenAll` vs awaiting in a loop — when is each right?
Round: screen / practical.
Repo anchor: `ValidatorBehavior.cs:L20-L21` runs all validators concurrently with WhenAll; `BasketState.NotifyChangeSubscribersAsync` (`BasketState.cs:L111-L112`) fans out UI callbacks; but `RabbitMQEventBus.ProcessEvent` loops handlers serially (`:L204-L207` — with a `// REVIEW: This could be done in parallel` comment!).
Mid: parallel when independent + thread-safe; serial when handlers share state (DbContext!) or order matters.
Senior: the REVIEW comment is a trap — handlers resolved from one scope may share a scoped DbContext; parallelizing them is a latent bug. Recognizing *why the easy optimization is wrong* is the senior move.
Drill: defend the serial loop in two sentences.

## Q12: How do you handle configuration and secrets in .NET?
Round: deep-dive.
Repo anchor: options pattern (`Catalog.API/Extensions/Extensions.cs:L35-L36`), `IOptionsMonitor` in PaymentProcessor (live-flippable `PaymentSucceeded`), Aspire injecting connection strings via `WithReference` (`eShop.AppHost/Program.cs:L30-L44`), and the anti-example: `ClientSecret = "secret"` hardcoded (`WebApp/Extensions.cs:L78`).
Mid: configuration providers layering (json < env < user-secrets); typed options with validation.
Senior: secret rotation implications of `IOptions` vs `IOptionsMonitor`; dev/prod parity via Aspire → azd; "no secret ever in the repo — this sample violates that deliberately, here's the fix" (user-secrets/KeyVault).
Drill: locate every hardcoded credential in the repo (there are at least two) and state the production replacement.

## Q13: What is gRPC and why did this repo choose it for exactly one service?
Round: deep-dive / API design.
Repo anchor: `basket.proto`, `BasketService.cs`, client at `WebApp/Extensions.cs:L31-L32`.
Mid: HTTP/2, binary protobuf, contract-first, streaming; chosen for the chattiest internal hop; REST kept where humans/partners consume (catalog, orders).
Senior: proto evolution rules (field numbers, never reuse), the mapping tax (proto BasketItem has no price — deliberate, see Flow 2), gRPC-web/browser limitations explaining why the *browser* never speaks it — the Blazor server does.
Follow-ups: "How do you version a proto?" "Deadline/retry semantics?"
Drill: list two fields you must NOT add to `basket.proto` and why (anything client-priced).

## Q14: Middleware pipeline — what does order mean and where has it bitten you?
Round: deep-dive.
Repo anchor: `WebApp/Program.cs:L17-L30` — exception handler → HSTS → antiforgery → HTTPS redirect → static files → components; `Catalog.API/Program.cs:L17-L23` — `UseStatusCodePages` before endpoints.
Mid: request delegates as an onion; auth-before-endpoints; why antiforgery sits where it does for Blazor SSR forms.
Senior: the MediatR behaviors (`Ordering.API/Application/Behaviors/`) as the *same pattern one level down* — being able to say "middleware, pipeline behaviors, and delegating handlers (`.AddAuthToken()`) are all the decorator chain, at three different radii" ties the whole stack together and is a genuinely impressive close.
Drill: draw the three onion diagrams (HTTP, mediator, HttpClient) for one checkout request.
