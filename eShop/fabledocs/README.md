# fabledocs — eShop as a Training Lab

A codebase-specific curriculum that turns this repository into a training lab for a **junior fullstack engineer (.NET/C#, plus React/Node/TS experience)** who wants to reach mid-level fast, build senior judgment, and pass interviews for mid-level fullstack roles.

Every page teaches two things at once:
1. **This repo** — where things live, how its real flows work, with exact file:line anchors.
2. **The transferable skill** — why the pattern exists, what alternatives look like, how it fails, and how to talk about it in an interview.

## What this repo is (the 8-sentence version)

eShop is Microsoft's reference e-commerce application ("AdventureWorks"), built on .NET 9 and orchestrated with **.NET Aspire** (`src/eShop.AppHost/Program.cs`). It is a services-based system: a Blazor Server storefront (`src/WebApp`), a REST **Catalog.API** (PostgreSQL + pgvector for AI search), a gRPC **Basket.API** (Redis), and an **Ordering.API** built with DDD + CQRS (MediatR commands, an `Order` aggregate, EF Core with a Postgres database). Services never call each other's databases; they communicate asynchronously through **RabbitMQ integration events** (`src/EventBusRabbitMQ`), with a transactional **outbox** (`src/IntegrationEventLogEF`) to keep database writes and event publishing consistent. Two headless workers — **OrderProcessor** (grace-period polling) and **PaymentProcessor** (simulated payment) — drive the order state machine forward. Authentication is centralized in **Identity.API** (Duende IdentityServer, OpenID Connect); the WebApp signs users in with cookies+OIDC and forwards JWTs to the backend APIs. Tests exist at three levels: MSTest/xUnit unit tests, Aspire-hosted functional tests, and Playwright e2e specs in `e2e/`. It is deliberately a *teaching* codebase: some corners are simplified (simulated payments, no dead-letter queue, permissive auth in places) — those simplifications are themselves lesson material here.

## The learning tracks

| Track | Folder | What you get |
| --- | --- | --- |
| Cartography | `01-codebase-cartography/` | System map, reading order, glossary, 6 end-to-end flow traces |
| Stack mastery | `02-stack-and-language-mastery/` | C#/.NET async model, ASP.NET Core + Blazor mental models, types & contracts, Aspire tooling |
| Architecture | `03-architecture-and-patterns/` | Layers, persistence, auth, async reliability, 14 pattern cards, a full critique |
| Reading gym | `04-code-reading-gym/` | Annotation drills, trace tables, fake-code contrasts, review katas |
| Quality | `05-quality-engineering/` | Testing strategy & recipes, systematic debugging, performance, security, observability |
| Contribution | `06-contribution-practice/` | Junior tickets → mid-level features → senior projects → design katas |
| Career | `07-career-and-collaboration/` | Code review mindset, PRs/RFCs, maintainer communication |
| **Interview prep** | `08-interview-prep/` | 45+ question cards anchored to this repo, system-design walkthrough, STAR stories, 2-week cram plan |
| Reference | `09-reference/` | Command cheatsheet, risk register, rubrics, verification log |

## How to use it

- **One weekend:** [00-fast-track.md](00-fast-track.md) only. Run it, trace two flows, make one safe change, do the teach-back.
- **Two weeks:** Fast track → `01-.../05-key-flows.md` → `03-.../05-pattern-catalog.md` → two tickets from `06-.../01-good-first-tickets.md` → skim `05-quality-engineering/`.
- **Eight weeks:** All tracks in order, one module per ~4 days, one contribution ticket per week, review katas twice a week.
- **Ongoing contributor:** live in `06-contribution-practice/` and `07-career-and-collaboration/`, use `09-reference/risk-register.md` as your radar.

**Recommended paths by profile:**

- **Brand-new junior:** 00 → 01 (all) → 02 → 04 (drills as you read) → 06 junior tickets. Skip 03-.../06-architecture-critique.md until month two.
- **Junior who knows .NET:** 00 → 01-.../05-key-flows.md → 03 (all) → 05 → 06 mid-level tickets.
- **Mid-level, new to this repo:** 01-.../01-system-map.md → 01-.../05-key-flows.md → 03-.../06-architecture-critique.md → 06 senior projects.
- **Senior doing architecture review:** 03-.../06-architecture-critique.md → 09-reference/risk-register.md → 05-.../05-security-checklist.md.
- **Interview in two weeks:** go directly to [08-interview-prep/07-two-week-cram-plan.md](08-interview-prep/07-two-week-cram-plan.md). It schedules everything else you need.

## Conventions used everywhere

- **Anchors:** `src/Ordering.Domain/AggregatesModel/OrderAggregate/Order.cs:L71-L91` means open that file at those lines. Line numbers were verified on 2026-07-16 (see [09-reference/verification-log.md](09-reference/verification-log.md)); re-check before quoting them in a PR.
- **Fake code:** every snippet not from this repo begins with `// Illustrative fake code: not from this repo`. Everything else is real.
- **Verified vs inferred:** commands marked **verified** were actually run while writing these docs; **inferred** means derived from README/CI/config but not executed.
- **Drills** end with self-grading criteria (Basic / Solid / Strong). Grade yourself honestly; "Solid" is the mid-level bar.
- **"Interview angle"** sections flag where a concept is standard interview material and what a mid-level answer sounds like.
- Suspicions are labeled *investigate* or *possible risk* — never asserted as bugs unless confirmed by reading the code.

## The mindset ladder

- **Junior asks:** "How do I make it work?"
- **Mid-level asks:** "Is this the right pattern? What does it cost? How do I test it?"
- **Senior asks:** "What does this commit us to? Who pays that cost, when, and how do we reduce the blast radius?"

Interviews for mid-level roles are a test of exactly the second and third questions — asked about code you claim to know. This repo gives you real code to know. Use it.
