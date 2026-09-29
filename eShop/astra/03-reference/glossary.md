# Vocabulary connected to this repository

| Term | Plain meaning | Example here |
| --- | --- | --- |
| SDK | Tools used to restore, compile, and test code | global.json selects the .NET SDK |
| Runtime | Components needed to execute compiled .NET code | Installing only a runtime does not provide the compiler |
| Solution filter | Selected projects from a solution | eShop.Web.slnf selects the web learning path |
| Central package management | Package versions declared together | Directory.Packages.props |
| Dependency injection | Supplying dependencies through a container | CatalogService receives HttpClient |
| Scoped service | An instance shared within a DI scope | BasketState registration; actual lifetime also depends on the hosting path |
| Middleware | Code around an HTTP request pipeline | Authentication and fixture test identity behavior |
| Endpoint | A mapped request entry point | GET /api/catalog/items |
| Contract | Inputs, outputs, and behavior callers rely on | V1/V2 routes and basket.proto |
| DTO | Data shaped for transfer across a boundary | Order summary or create-order request |
| Entity | A domain or persistence object with identity | Order and CatalogItem |
| Value object | A value described by its properties | Ordering's Address |
| Aggregate | A group whose rules are controlled through a root | Order controls adding order items |
| Invariant | A condition that must remain true | Invalid OrderItem units are rejected |
| LINQ | C# operators for composing data operations | Where, Select, Sum, Skip, Take |
| IQueryable | A provider-interpreted query description | Catalog's EF query before ToListAsync |
| Materialization | Executing a query and creating results | ToListAsync |
| Tracking | EF's monitoring of loaded entities for changes | Inspect whether a read query needs it |
| Migration | A versioned schema change | Catalog and Ordering migrations |
| Transaction | A local database all-or-nothing boundary | OrderingContext transaction methods |
| gRPC | RPC over a typed protocol contract | Basket service calls |
| Protobuf field number | Stable identifier of a serialized field | product_id = 2; quantity = 6 |
| Redis | Key/value infrastructure used here for baskets | Serialized user-specific basket keys |
| Event | A record that something happened | OrderStatusChangedToPaidIntegrationEvent |
| Domain event | An in-process business notification | Order transition domain events |
| Integration event | A serialized message between services | Stock validation and payment events |
| Outbox-style event log | Persisted intent to publish alongside data | IntegrationEventLogEF; recovery still needs analysis |
| Idempotency | Repeating an operation avoids repeating its intended effect | Duplicate request/event exercises |
| Acknowledgement | Consumer tells the broker a delivery is handled | BasicAckAsync |
| Dead-letter destination | A place for messages rejected or expired under broker rules | A proposed failure-recovery exercise |
| Authentication | Establishing who the caller is | WebApp sign-in |
| Authorization | Deciding what the caller may do | Owner-only order exercises |
| Claim | A fact carried in an identity | sub identifies the user in these paths |
| Antiforgery | Protection for browser form request integrity | AntiforgeryToken in cart forms |
| Task | Representation of asynchronous completion | BasketState caches a Task |
| Cancellation token | Cooperative signal to stop work | OrderProcessor shutdown path |
| Characterization test | Test describing current behavior | OrderItem zero-unit increment |
| Regression test | Test preventing a known bug from returning | Invalid pagination rejection |
| Test double | Controlled substitute for a dependency | NSubstitute IBasketRepository |
| Functional test | Test crossing selected runtime boundaries | WebApplicationFactory with PostgreSQL |
| End-to-end test | A user journey through running components | Playwright browsing and bag tests |
| Trace | Related operations with timing and context | HTTP and event spans in the dashboard |
| Metric | Aggregated numeric measurement | Latency or failure counts |
| Liveness | Whether a process responds | Development /alive check |
| Readiness | Whether registered checks permit accepting traffic | Development /health behavior |
| ADR | A record of a design choice and consequences | Basket concurrency decision |
| Spike | A bounded experiment to resolve uncertainty | Duplicate-safe stock prototype |
| Definition of done | Evidence required to call work complete | Acceptance cases, checks, review, explanation |

Use these terms precisely in PRs. “The API works” is weaker than “the V2 HTTP contract test passed against the fixture's PostgreSQL database.”
