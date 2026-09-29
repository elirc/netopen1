# How this pack fits alongside `fabledocs/`, `fabledoc2/`, and `astra/`

Three learning trees already exist in this checkout, all written against the same baseline commit
(`9b4f943`, verified by `git log -1` at the time this pack was written — 2026-09-23). This page is the map so you
don't read the same explanation three times.

| Tree | What it is | Verdict |
| --- | --- | --- |
| `astra/` | 72-story junior→capstone bootcamp, 12 stages, with a `CURRICULUM.md`, `PROGRESS.md`, glossary, assessment rubric, and a workbook convention. Stage 9 (`01-lessons/09-events-and-consistency.md`, stories ASTRA-046/047/049/051) covers checkout identity, secret handling, the checkout→status trace, and outbox failure windows directly. | **KEEP.** This is the primary, most exercise-dense track. If you only do one thing in this repo, do `astra`. |
| `fabledocs/` | 9-track reference curriculum (cartography → stack → architecture → reading gym → quality → contribution → career → interview prep → reference). `01-codebase-cartography/05-key-flows.md` Flow 3 (checkout) and Flow 6 (admin price change / outbox) are the deepest existing evidence-backed traces of exactly what this pack was asked to cover. `08-interview-prep/` has 45+ questions and a 2-week cram plan. | **KEEP.** Read Flow 3 + Flow 6 before this pack's `01-checkout-outbox-correctness.md` — that file assumes you have and adds a narrower "what guarantee holds where" lens plus a fresh line-by-line re-check, not a re-explanation. |
| `fabledoc2/` | 10 reverse-engineered ADRs (`README.md`), each in Problem/Decision/Alternatives/Consequences/Status form. ADR-003 ("Services coordinate by choreographed events over RabbitMQ, not synchronous calls") is the senior-trade-off writeup for the event bus design; ADR-002 covers the database-per-service split the outbox lives inside. | **KEEP.** Don't duplicate ADR-003. This pack's `03-outbox-sweeper-tradeoff.md` picks the one concrete decision ADR-003 names as a consequence but doesn't design (the missing retry sweeper) and works it in the same Problem→...→when-to-revisit format, as a *sequel* card, not a replacement. |

## What this pack (`training/`) adds that isn't already there

1. **A change-request placement exercise** (`04-change-request.md` + sealed `_answers/04-change-request.md`).
   None of the three existing trees has this exact artifact: a feature request you must place (files, data
   changes, tests) *before* an agent implements it, graded against a reference answer. `astra/02-stories/ASTRA-067`
   is the closest thing (the capstone feature definition), but it's a multi-week capstone, not a single change
   placed against the current outbox design. This pack's request is scoped to something you can place in one
   sitting.
2. **A re-verification pass**, not a re-explanation, of the checkout→outbox→RabbitMQ path, cross-checked against
   the current source on 2026-09-23 (see `01-checkout-outbox-correctness.md` for what was re-read and confirmed).
   All three trees independently claim "no background sweeper retries `NotPublished`/`PublishedFailed` rows" —
   this pack re-confirms that specific claim against `IIntegrationEventLogService` and its two registrations
   (Catalog.API, Ordering.API) and shows the interface-level reason a sweeper can't be bolted on trivially.
3. **One senior trade-off card** on that exact gap (`03-outbox-sweeper-tradeoff.md`), feeding directly into the
   change request.

## What this pack deliberately skips

- Full system map, glossary, reading order → already in `fabledocs/01-codebase-cartography/` (KEEP, use it).
- Full architecture critique and pattern catalog → `fabledocs/03-architecture-and-patterns/` (KEEP, use it).
- Interview questions, STAR stories, system design → `fabledocs/08-interview-prep/` (KEEP, use it; this repo is
  READ tier, so no separate `interview/` folder was created here — see the brief).
- Junior/mid/senior ticket ladder → `astra/02-stories/` already has 72 stories across 12 stages (KEEP, use it);
  this repo doesn't get a LAB-tier `ladder/` per the tier rules.
