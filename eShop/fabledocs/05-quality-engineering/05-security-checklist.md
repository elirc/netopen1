# Security Checklist

Mapped to real code. Severity is judged *for a production system shaped like this* — the repo is a sample and several findings are deliberate simplifications; the skill is telling which.

## Findings map

| Area | State here | Anchor | Verdict |
| --- | --- | --- | --- |
| Authentication | Central OIDC; JWT bearer on APIs; cookie on WebApp | `AuthenticationExtensions.cs:L33-L50`, `WebApp/Extensions.cs:L66-L87` | solid shape |
| Audience validation | **disabled** (`ValidateAudience = false`) | `AuthenticationExtensions.cs:L49` | R6 — one service's token works at another |
| Authorization (writes) | Catalog mutations: none | `CatalogApi.cs:L93-L110` | R4 — top finding |
| IDOR | Basket: safe by construction (key = own `sub`). Orders list: filtered by identity (`OrdersApi.cs:L95`). Order-by-id: **unverified ownership** | `OrdersApi.cs:L80-L91` | R5 — *investigate `OrderQueries`* |
| Input validation | Route constraints, ProblemDetails 400s, FluentValidation, aggregate invariants | module 03/03 | layered, good |
| Mass assignment | `SetValues(productToUpdate)` copies every column from the request body | `CatalogApi.cs:L340-L341` | watch: any future sensitive column is client-writable |
| Injection | EF parameterization throughout; the one raw SQL uses parameters correctly (`AddWithValue`) | `GracePeriodManagerService.cs:L69-L74` | clean |
| XSS | Blazor encodes by default; no `MarkupString` in pages read | — | *inferred clean; grep `MarkupString` before asserting* |
| CSRF | Antiforgery middleware + Blazor form handling | `WebApp/Program.cs:L24` | present |
| SSRF | No user-supplied URLs fetched. Webhooks.API registers third-party callback URLs — the classic SSRF/egress spot | `src/Webhooks.API` (not read in depth) | *investigate: is the destination validated? does registration verify ownership (challenge token)?* |
| Secrets | `ClientSecret = "secret"`, seeded users, `tempkey.jwk` in Identity.API | `WebApp/Extensions.cs:L78` | sample-only; production = vault + rotation |
| Sensitive data handling | Card number masked before logging/command (`PadLeft` mask), body deliberately not logged | `OrdersApi.cs:L124-L144` | genuinely good pattern to quote — but note CVV (`CardSecurityNumber`) travels the full pipeline and is stored on the command; PCI would forbid persisting it. Check what `Buyer`/`PaymentMethod` persist |
| Transport | HTTPS + HSTS on WebApp; `RequireHttpsMetadata=false` for local identity | `WebApp/Program.cs:L20-L26`, `AuthenticationExtensions.cs:L39` | dev-only flags to gate by env |
| Rate limiting | none anywhere | — | absent; first place: order creation + login |
| Dependency risk | Central package versions; preview feeds in `nuget.config` | `Directory.Packages.props` | pin + audit; preview feeds are a supply-chain surface |
| Uploads | none (catalog pics are repo assets served by path — path built from DB filename, `CatalogApi.cs:L217-L221`; filename is server-controlled, so no traversal *today*; becomes one the day an upload endpoint writes `PictureFileName`) | | pre-emptive note |
| Message bus | events unauthenticated/unsigned; anyone on the broker can publish "OrderPaymentSucceeded" | `RabbitMQEventBus.cs` | fine intra-VPC; know it's a trust boundary |

## The pre-merge security checklist (use on every PR here — and everywhere)

1. New endpoint? → Who can call it (authN), what may they touch (authZ), and is the resource id owner-checked?
2. New input? → Validated at the boundary, length-capped, and absent from logs if sensitive?
3. New query? → Parameterized (EF or explicit params)? Filtered by tenant/owner?
4. New config? → Secret? Then not in the repo, not in logs, rotatable.
5. New outbound call? → URL user-influenced (SSRF)? Timeout set? Failure handled?
6. New event/consumer? → Idempotent? What happens if a hostile/buggy peer publishes it?
7. Contract change? → Does it widen what a client can write (mass assignment) or read (over-fetch)?

Interview angle: security rounds for fullstack mids are exactly rows of this table: "what's an IDOR / how do you prevent CSRF / where do you validate?" Answer each with this repo's concrete instance + the fix. The masked-card-logging line (`OrdersApi.cs:L140`) is a rare *positive* example candidates almost never have — use it.

Drill: complete the two *investigate* items (order-by-id ownership; webhook URL validation) by reading `OrderQueries.cs` and `Webhooks.API`. Write both up as security-review findings: evidence, exploit scenario, fix, test. Self-grade — Strong: your exploit scenario includes the actual HTTP request an attacker would send.
