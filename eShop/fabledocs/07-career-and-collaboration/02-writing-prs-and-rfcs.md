# Writing PRs and RFCs

## PR description template (tuned to this repo)

```markdown
## What
One paragraph. Lead with the user/operator-visible change.

## Why
The problem, with anchors (file:line). Link the issue/risk-register entry.

## How
Key decisions only — what a reviewer can't infer from the diff.
Which existing pattern this follows (outbox / IdentifiedCommand / options / …).

## Contract impact
REST/gRPC/event shape changes? Version story? "None" is a valid answer — say it explicitly.

## How tested
Commands run + what they proved. Manual verification steps if e2e.
What is NOT covered and why that's acceptable.

## Risks & rollback
Blast radius. How to turn it off. Migration reversibility.
```

The "Contract impact: none" line is this repo's most valuable habit — half the review katas' blocking findings are smuggled contract changes.

## Commit messages

Imperative, scoped, why-bearing: `Basket.API: expire baskets after 90 days (config BasketOptions:TtlDays)` beats `fix redis issue`. One logical change per commit; migrations in their own commit (reviewers diff them differently).

## When to RFC instead of PR

Any of: touches a wire contract consumed by another service; changes messaging topology (queue args are *immutable* in RabbitMQ — M2's lesson); changes failure semantics (R1/R3 fixes); adds a new service or store; anything with a multi-step rollout. Rule of thumb: **if rollback is not "revert the commit," write the RFC first.**

## RFC template (one page, tailored here)

```markdown
# RFC: <title>
Status: Draft | Reviewed | Accepted
Problem — with evidence (anchors, logs, risk-register row).
Constraints — contracts that must not break, services that can't be redeployed together.
Option A / B / C — one paragraph each: mechanism, blast radius, rollout, rollback.
  (Always include "do nothing" with its cost.)
Recommendation — and what evidence would change it.
Consumer impact audit — who calls/consumes this today (greps, not vibes).
Rollout plan — flags, sequencing across services, queue/schema migration steps.
Open questions.
```

Worked prompt: kata G (the R3 contract-honesty RFC) — its consumer audit is one grep (`OrderingService` in WebApp) plus one judgment call (mobile BFF exposure), which is exactly the right size for a first RFC.

Interview angle: "walk me through a technical decision you documented" — an RFC you actually wrote against this repo (kata G, or M2's queue migration) is a better artifact than any employer anecdote a junior has. Bring it.
