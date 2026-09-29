# The .NET Runtime Model (for someone who knows Node)

## Threads, the pool, and why async still matters

Node: one JS thread, an event loop, I/O callbacks. .NET: a **thread pool** with many threads — but threads are expensive (~1MB stack), so a server that *blocks* a thread per request dies at a few thousand concurrent requests. `async/await` exists to release the thread during I/O, exactly like Node releases its one thread — .NET just has N of them.

Repo evidence: every I/O call in every handler is awaited — `CatalogApi.cs:L149-L156` (DB), `RedisBasketRepository.cs:L25` (Redis), `RabbitMQEventBus.cs:L97-L102` (publish). There is no `.Result`/`.Wait()` anywhere in the request paths (grep it — the absence is the lesson). Sync-over-async is the .NET equivalent of blocking Node's loop: everything else queues behind it.

## What `await` compiles to

A state machine: the method's locals become fields, the rest of the method becomes a continuation scheduled when the task completes. In ASP.NET Core there is **no SynchronizationContext** — continuations resume on *any* pool thread. Consequences you can see here:
- No `ConfigureAwait(false)` noise in app code (it matters in libraries; the EventBus does not use it either — acceptable, it's app-tier).
- Anything relying on thread affinity (thread-static caches, culture in old code) is a bug factory. Blazor Server *does* have a sync context (the circuit) so UI code touches components safely after await — one of the few places the distinction matters. Relevant to `BasketState`: it runs on the circuit, and its `HashSet` of subscriptions (`BasketState.cs:L16`) is mutated without locks — safe only because of the circuit's single-logical-thread model. That's an *invariant* held by the framework, worth saying aloud.

## Serial vs parallel awaits

- Serial because they must be: two EF queries on one `DbContext` (`CatalogApi.cs:L149-L156`) — DbContext is not thread-safe.
- Parallel because they can be: `Task.WhenAll` over independent validators (`ValidatorBehavior.cs:L20-L21`) and UI notifications (`BasketState.cs:L111-L112`).
- Deliberately serial despite the temptation: event handlers per message (`RabbitMQEventBus.cs:L204-L207` — the `// REVIEW` comment; handlers may share a scoped DbContext).

That three-way classification is a complete interview answer to "when do you parallelize awaits?"

## Cancellation

`CancellationToken` threads through commands (`CreateOrderCommandHandler.cs:L29`) and the worker loop (`GracePeriodManagerService.cs:L26`, `Task.Delay(delayTime, stoppingToken)` — cancels the *sleep*, which is why shutdown is prompt). Node's `AbortSignal` is the same idea, later to the party. Junior code ignores tokens; mid-level code forwards them; senior code knows where cancelling is *wrong* (after the DB commit, mid-compensation).

## GC in one paragraph

Generational, compacting; allocation is a pointer bump (cheap), collection cost scales with *survivors*. Server GC (default for ASP.NET) trades memory for throughput. Where this repo cares: `StringGetLeaseAsync` (`RedisBasketRepository.cs:L25`) rents a buffer instead of allocating a string — a deliberate low-allocation read path; and source-generated JSON (L51-L56) avoids reflection allocations. You rarely tune GC; you avoid allocating in hot paths.

Interview angle:
1. "How does async improve throughput if there's no parallelism?" (thread freed during I/O — cite any handler)
2. "What's thread-pool starvation and how do you cause it?" (sync-over-async under load)
3. "When must awaits be sequential?" (shared non-thread-safe state — DbContext)
4. "How does graceful shutdown reach your background loop?" (token through `Task.Delay`) — each cross-linked in [../08-interview-prep/01-csharp-dotnet-deep-dive.md](../08-interview-prep/01-csharp-dotnet-deep-dive.md) (Q1, Q8, Q11).

Drill: find every `Task.WhenAll` in `src/` (grep) and classify each: safe-parallel, unsafe-if-parallel, or irrelevant. Self-grade — Solid: all found and classified; Strong: you can state the shared resource that makes each safe or unsafe.
