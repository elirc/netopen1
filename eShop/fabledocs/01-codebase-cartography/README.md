# 01 — Codebase Cartography

Before you can change a system safely you must be able to *locate* things in it faster than the people who wrote it. This module builds that map.

| File | What it gives you |
| --- | --- |
| [01-system-map.md](01-system-map.md) | The shape of the repo: services, ownership, public vs private surfaces, a diagram |
| [02-file-reading-order.md](02-file-reading-order.md) | 28 files in reading order with junior/mid/senior paths |
| [03-domain-glossary.md](03-domain-glossary.md) | The product nouns and the confusables (Basket vs Cart vs Order draft…) |
| [04-runtime-and-tooling-map.md](04-runtime-and-tooling-map.md) | Build/test/run tooling, runtime boundaries, env/config surfaces |
| [05-key-flows.md](05-key-flows.md) | **The spine of the whole curriculum** — six end-to-end traces |

Suggested order: 01 → 05 → 02 (use it as a checklist over a week) → 03/04 as reference.

Transferable skill: the questions these files answer — *what are the deployable units? where do contracts live? who owns which data?* — are the first four questions to ask of **any** unfamiliar repo, and the first thing a system-design interviewer probes when you say "I know microservices."
