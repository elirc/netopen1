# Performance Thinking

Rule zero: **measure first**. This repo hands you the instruments: the Aspire dashboard shows per-request traces with timing per span (including through RabbitMQ), and EF logs SQL. A perf claim without a trace or a benchmark is a vibe.

## The performance domains here, and where each would bite

| Domain | Hotspot candidates (anchors) | How to find it |
| --- | --- | --- |
| DB round trips | count+page = 2 queries (`CatalogApi.cs:L149-L156`) — fine; batch endpoint prevents cross-service N+1 (`:L162-L168`); update-then-reread in basket (`RedisBasketRepository.cs:L47`) | trace spans per request; EF command logging |
| Missing indexes | filters on `Name` (StartsWith → range-scannable), `CatalogTypeId`, `CatalogBrandId`; grace-period scan on `OrderDate`+`OrderStatus` (`GracePeriodManagerService.cs:L69-L74`, runs every cycle over the orders table!) | `EXPLAIN ANALYZE` in psql; check `EntityConfigurations`/migrations for what indexes actually exist — *don't assume; read* |
| Unbounded queries | `GetItemsByIds` no cap (ticket 12); pageSize cap? (ticket 15); vector search sorts **all embedded items** by cosine distance per query (`CatalogApi.cs:L280-L286`) — pgvector index (HNSW/IVFFlat) present? *investigate migrations* | slow-query log |
| Chatty UI | Blazor Server: every interaction is a SignalR round trip; basket badge updates via in-proc events (cheap); the real cost is circuit memory per user | dashboard metrics; load test with many idle circuits |
| Serialization | source-gen JSON in basket path (already optimal); reflection JSON on the bus (fine at this volume) | CPU profiles |
| Tracking overhead | no `AsNoTracking` on catalog reads (ticket 7) — measurable at high RPS, invisible below | BenchmarkDotNet micro-benchmark or RPS A/B |
| Startup | auto-migrate+seed (~100 items + embeddings if AI on) (`Catalog.API/Extensions/Extensions.cs:L23-L24`) | cold-start timing in dashboard |

## Worked example: "the catalog page is slow" (the interview shape)

1. Trace one request in the dashboard. Where's the time — WebApp render, HTTP hop, or SQL span?
2. SQL span dominant → get the SQL from EF logs → `EXPLAIN` it → missing index on `(CatalogTypeId, CatalogBrandId, Name)`? Offset pagination on page 500 (`OFFSET 5000`) scans 5010 rows — keyset pagination (`WHERE Name > @last ORDER BY Name LIMIT 10`) is the upgrade; requires a stable sort key and changes the API contract (no random page jumps) — *name the cost, not just the fix*.
3. Hop dominant → connection pooling? (HttpClientFactory already pools; gRPC channel reused — `AddGrpcClient` singleton channel.)
4. Render dominant → component re-render breadth; `@key` usage; move per-item work out of render path.

Being able to run that decision tree *in order, refusing to guess early* is what "performance thinking" means in a mid-level interview.

## What NOT to optimize here

The two-query count+page (correct and clear); the basket's read-back (one Redis RTT for read-your-write semantics); handler serialization on the bus (volume is tiny). Premature optimization critiques land better when you can also point at the *real* costs you'd take first (indexes, `AsNoTracking`, caps).

Interview angle: "How would you find an N+1?" (trace: many identical SQL spans under one request), "offset vs keyset pagination" (above, with the contract cost), "cache or index first?" (index — caching adds invalidation complexity; this repo has *zero* HTTP caching, and the first cache to add is response-level ETag on catalog reads, not a Redis entity cache).

Drill: open the migrations and answer with evidence: which indexes exist on CatalogItems and Orders? Does the grace-period query have a covering index? Write the two `CREATE INDEX` statements you'd propose, and what write-amplification they cost.
