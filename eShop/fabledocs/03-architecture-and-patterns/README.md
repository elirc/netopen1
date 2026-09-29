# 03 — Architecture & Patterns

This is where "it works" becomes "it's the right shape." Read after Cartography.

| File | Focus |
| --- | --- |
| [01-boundaries-and-layers.md](01-boundaries-and-layers.md) | Who owns what; real boundary wins and leaks |
| [02-data-model-and-persistence.md](02-data-model-and-persistence.md) | Entities, transactions, migrations, how to change schema safely |
| [03-validation-auth-and-permissions.md](03-validation-auth-and-permissions.md) | The four validation layers; authN vs authZ; the IDOR question |
| [04-side-effects-async-and-reliability.md](04-side-effects-async-and-reliability.md) | Every side effect mapped; idempotency, retries, failure visibility |
| [05-pattern-catalog.md](05-pattern-catalog.md) | **14 pattern cards** — the module's core |
| [06-architecture-critique.md](06-architecture-critique.md) | Strengths, risks, and "what I'd change owning this" — doubles as system-design interview prep |

Vocabulary you'll exit with (all defined in context, all interview words): invariant, boundary, contract, ownership, idempotency, isolation, consistency, outbox, blast radius, saga/choreography, observability.
