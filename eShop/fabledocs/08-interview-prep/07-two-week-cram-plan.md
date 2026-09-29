# Two-Week Cram Plan

Assumes ~2.5 focused hours/weekday, more on weekends. Everything references files in this suite. "Aloud" means aloud — silent review does not build interview performance.

## Week 1 — build the evidence base

**Day 1:** [00-fast-track.md](../00-fast-track.md) §1–3: run the system, trace Flows A/B on paper. Evening: read [08 README](README.md) golden rule; say the checkout flow aloud once, badly. (Badly is expected.)
**Day 2:** [Key Flows](../01-codebase-cartography/05-key-flows.md) 1–3 deeply (do the drills). Cards Q1–Q5 of [C# deep-dive](01-csharp-dotnet-deep-dive.md) aloud.
**Day 3:** Key Flows 4–6. Cards Q6–Q10. Annotation drills 1–2 ([gym](../04-code-reading-gym/01-annotation-drills.md)).
**Day 4:** [Pattern catalog](../03-architecture-and-patterns/05-pattern-catalog.md) cards 1–7 (outbox, idempotency, aggregate, domain events, CQRS, behaviors, pub/sub) — these seven are 80% of your deep-dive value. Cards Q11–Q14.
**Day 5:** Pattern cards 8–14. [API/data cards](03-api-and-data-modeling-questions.md) Q1–Q6 aloud. Annotation drills 3–4.
**Day 6 (weekend):** First full **mock system design** — [04-system-design-from-this-repo.md](04-system-design-from-this-repo.md), 40 min, recorded, whiteboard/paper. Then read the file's junior/mid/senior contrasts against your recording. Draft STAR stories 1 and 2 ([worksheets](06-behavioral-star-stories.md)).
**Day 7 — CHECKPOINT:** Self-assess against [../09-reference/learning-rubrics.md](../09-reference/learning-rubrics.md) interview-ready column. Gate questions: Can you narrate checkout end-to-end with idempotency+outbox+guards, unprompted, in 3 minutes? Can you name three ways this repo achieves idempotency with anchors? If no → repeat Day 2/4 material before proceeding; drop Day 9's second sim instead of skipping the fix.

## Week 2 — performance under pressure

**Day 8:** [Frontend cards](02-frontend-framework-questions.md) all 10 aloud (translate to React if your loop is React). API/data cards Q7–Q12.
**Day 9:** **Timed debugging sims 1 & 2** ([05-debugging-and-code-review-rounds.md](05-debugging-and-code-review-rounds.md)) — recorded. Review recordings against the rubric same day.
**Day 10:** **Review sims 1 & 2.** STAR stories 3–5 drafted; stories 1–2 rehearsed to <2 min.
**Day 11:** Second mock **system design**, this time a variation prompt (multi-tenancy or flash-sale — the file's prompts 1/4). Debugging sim 3.
**Day 12:** Weak-spot day: redo whichever card file scored worst; review [architecture critique](../03-architecture-and-patterns/06-architecture-critique.md) R1–R3 until you can present each as *evidence → failure scenario → smallest fix → test* in 90 seconds each.
**Day 13 (weekend):** Full loop simulation: 15 min "walk me through a system you know" + 40 min system design (fresh variation) + 20 min review sim 3 + 30 min behavioral (all 5+ rehearsed stories, shuffled prompts). Friend as interviewer if at all possible.
**Day 14 — CHECKPOINT + taper:** Re-run the Day 7 gates plus: one debugging narration cold; three STAR stories under 2 min each; the two-sentence answers to "what would you improve in that codebase?" (R1 with fix) and "what's the best design decision in it?" (outbox/pattern asymmetry — your pick, owned). Then stop. Do not learn new material the night before; re-read your own trace notes only.

## Daily constants (both weeks, 15 min)

- One teach-back: yesterday's hardest concept, aloud, 90 seconds.
- One anchor re-verification: open a file you cited yesterday and confirm you remembered it right. (Catches drift between what you *read* and what you *remember* — the #1 source of interview blowups when an interviewer drills down.)

## If you only have one week

Days 1, 2, 4, 6, 9, 12, 14 in that order. Cut frontend cards before you cut the system-design mocks; cut nothing from the checkout-flow material — it is the spine of every round.
