# 08 — Interview Prep (first-class module)

Target: **mid-level fullstack interviews** for a .NET/C# candidate (with React/Node crossover notes). Over 60% of the question cards here anchor to real code in this repo, so you practice answering with *evidence* instead of recited definitions.

## How mid-level loops are typically structured

1. **Screen** (30–45 min): language/runtime fundamentals, one small coding exercise.
2. **Technical deep-dive** (60 min): "walk me through a system you know well." *This repo is that system now.*
3. **Practical coding** (60 min): build/extend/debug something realistic.
4. **System design** (45–60 min): mid-level bar = a coherent design with named tradeoffs, not planet-scale.
5. **Behavioral** (45 min): STAR stories; for mid-level they probe ownership and collaboration.

## The golden rule

Every answer = **concept + concrete example + tradeoff + failure mode**. "The outbox pattern keeps DB writes and events consistent — in eShop, a price change writes the event to a log table in the same transaction (`CatalogApi.cs:L350-L356`), publishes after commit, and the gap is that a crash between commit and publish needs a sweeper, which that repo lacks." That is a mid-level answer. A definition alone is a junior answer.

## Files

| File | Contents |
| --- | --- |
| [01-csharp-dotnet-deep-dive.md](01-csharp-dotnet-deep-dive.md) | 14 cards: async/await, DI lifetimes, EF, LINQ, exceptions, records… |
| [02-frontend-framework-questions.md](02-frontend-framework-questions.md) | 10 cards: Blazor Server (with React parallels), forms, state, rendering |
| [03-api-and-data-modeling-questions.md](03-api-and-data-modeling-questions.md) | 12 cards: REST/gRPC, versioning, pagination, idempotency, schema design |
| [04-system-design-from-this-repo.md](04-system-design-from-this-repo.md) | Full whiteboard walkthrough: "design an e-commerce platform" |
| [05-debugging-and-code-review-rounds.md](05-debugging-and-code-review-rounds.md) | Timed simulations built from modules 04/05 |
| [06-behavioral-star-stories.md](06-behavioral-star-stories.md) | 9 STAR worksheets sourced from the contribution tickets |
| [07-two-week-cram-plan.md](07-two-week-cram-plan.md) | Day-by-day plan with checkpoints |

Counts (recounted 2026-10-06): files 01–03 hold **36 question cards, 35 of them with a "Repo anchor" line**; file 05 adds **7 timed simulations** (4 debugging, 3 review).
