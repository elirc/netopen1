# B01 apprenticeship materials — eShop (READ tier)

This project already has two rich, hand-written learning trees (`fabledocs/`, `fabledoc2/`) and a 72-story bootcamp
(`astra/`) with its own checkout/outbox coverage. Per the apprenticeship brief, this repo is **READ tier**: Phase 4
(codebase navigation) only, no source edits, no incident branches. This folder does **not** re-teach what those
trees already teach well — it verifies their outbox/checkout claims against the current code, adds the one Phase-4
deliverable they're missing (a change-request placement exercise), and tells you which existing tree to read for
what.

## Start here

1. Read `navigation/00-how-this-pack-fits.md` first — it routes you to `fabledocs/`, `fabledoc2/`, or `astra/` for
   each topic, with KEEP/MERGE/IGNORE verdicts, before you read anything else here.
2. `navigation/01-checkout-outbox-correctness.md` — a tighter, re-verified pass over the checkout → ordering →
   outbox → RabbitMQ path, organized around *what guarantee holds at each step and what doesn't*, with a
   cross-check against `astra/01-lessons/09-events-and-consistency.md` and `fabledocs/01-codebase-cartography/05-key-flows.md`.
   Read this only after (or instead of, if short on time) Flow 3 and Flow 6 in `fabledocs`.
3. `navigation/02-first-change-onboarding.md` — one page: what to understand before touching this repo for real.
4. `navigation/03-outbox-sweeper-tradeoff.md` — one senior trade-off card (Problem → naive → options → trade-offs →
   choice → failure modes → tested/monitored → when to revisit) on the exact gap all three doc trees independently
   flag: no background retry for `NotPublished`/`PublishedFailed` integration-event-log rows.
5. `navigation/04-change-request.md` — do this last. Write your placement answer *before* opening `_answers/`.

Suggested order and time: item 1 (10 min) → item 2 (30–40 min, with the source files open) → item 3 (10 min) →
item 4 (15 min) → item 5 write-up (30–45 min) → compare against `_answers/04-change-request.md` (10 min).
Total: **~2 hours**, assuming you've already done `astra` stages 1–9 or `fabledocs` tracks 01/03.

## What's sealed

`training/_answers/04-change-request.md` holds the reference placement and design reasoning for the change
request in `navigation/04-change-request.md`. Don't open it before writing your own answer.

## What this pack does not do

No `ladder/`, `review/`, `incidents/`, `agentic/`, or `interview/` folders — those are LAB/DRILL-tier phases and
this project is READ tier (Phase 4 only), per the apprenticeship brief (`B01_AGENT_BRIEF.md`, kept outside this repository). `astra/03-reference/assessment.md`
already has stage gates and a self-review route if you want graded checkpoints; `fabledocs/08-interview-prep/`
already has 36 interview question cards and 7 timed simulations anchored to this repo. Use those rather than a new interview kit here.
