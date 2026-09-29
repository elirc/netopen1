# A paced curriculum

[Bootcamp home](README.md) · [All stories](02-stories/README.md)

Complete onboarding before implementation work. Plan two weeks per stage as a starting rhythm, then add time for the advanced stages, review, and your own learning gaps. Expect roughly 24-36 weeks at 12-15 hours a week; the full course is approximately 300-450 hours. This is a planning estimate, not a deadline or a claim that every junior progresses at the same speed.

## Stage route

| Stage | Lesson | Stories | Outcome |
| --- | --- | --- | --- |
| 1 | [Onboard and contribute](00-onboarding/04-first-contribution.md) | [ASTRA-001](02-stories/ASTRA-001.md)–[ASTRA-006](02-stories/ASTRA-006.md) | Start, inspect, and submit a small reviewable contribution. |
| 2 | [C# and focused tests](01-lessons/02-csharp-and-testing-basics.md) | [ASTRA-007](02-stories/ASTRA-007.md)–[ASTRA-012](02-stories/ASTRA-012.md) | Explain values, state, async calls, and a focused regression test. |
| 3 | [Blazor and accessible UI](01-lessons/03-blazor-and-browser.md) | [ASTRA-013](02-stories/ASTRA-013.md)–[ASTRA-018](02-stories/ASTRA-018.md) | Improve a visible behavior and prove it in the browser. |
| 4 | [HTTP and API contracts](01-lessons/04-http-and-contracts.md) | [ASTRA-019](02-stories/ASTRA-019.md)–[ASTRA-024](02-stories/ASTRA-024.md) | Design bounded input and preserve versioned API behavior. |
| 5 | [Basket and state](01-lessons/05-basket-and-state.md) | [ASTRA-025](02-stories/ASTRA-025.md)–[ASTRA-030](02-stories/ASTRA-030.md) | Validate gRPC input and handle user-specific cached state. |
| 6 | [Persistence and domain rules](01-lessons/06-data-and-domain.md) | [ASTRA-031](02-stories/ASTRA-031.md)–[ASTRA-036](02-stories/ASTRA-036.md) | Protect invariants and verify database behavior. |
| 7 | [Reliable test suites](01-lessons/07-testing-strategy.md) | [ASTRA-037](02-stories/ASTRA-037.md)–[ASTRA-042](02-stories/ASTRA-042.md) | Build isolated tests that exercise the intended layer. |
| 8 | [Identity and defensive coding](01-lessons/08-identity-and-security.md) | [ASTRA-043](02-stories/ASTRA-043.md)–[ASTRA-048](02-stories/ASTRA-048.md) | Enforce ownership and keep sensitive data out of diagnostics. |
| 9 | [Events and consistency](01-lessons/09-events-and-consistency.md) | [ASTRA-049](02-stories/ASTRA-049.md)–[ASTRA-054](02-stories/ASTRA-054.md) | Trace asynchronous work and reason about duplicate delivery. |
| 10 | [Diagnosis and operations](01-lessons/10-debugging-and-observability.md) | [ASTRA-055](02-stories/ASTRA-055.md)–[ASTRA-060](02-stories/ASTRA-060.md) | Use traces, logs, and controlled failures to explain a symptom. |
| 11 | [Design and delivery](01-lessons/11-design-and-delivery.md) | [ASTRA-061](02-stories/ASTRA-061.md)–[ASTRA-066](02-stories/ASTRA-066.md) | Make and communicate a measured engineering decision. |
| 12 | [Capstone: available products](01-lessons/12-capstone.md) | [ASTRA-067](02-stories/ASTRA-067.md)–[ASTRA-072](02-stories/ASTRA-072.md) | Deliver one feature across contract, database query, UI, and tests. |

## Your weekly routine

- Session 1: read the lesson, trace the relevant source, and write predictions.
- Session 2: complete the smallest story slice and gather regression evidence.
- Session 3: review the diff, revise it, and explain one decision aloud.
- End of week: update the tracker, score the gate, and choose the next dependency-ready story.

A mentor pairing session of 30-45 minutes each week is enough to challenge assumptions and review one focused diff. Do the experiments yourself between sessions. Self-study learners can use a delayed review, explain the result aloud, and deliberately challenge one acceptance case.

## Paths through the course

**New to C#:** slow down at stage 2. Add scratch exercises for methods, collections, null, and exceptions until you can predict the provided examples.

**Comfortable with C#, new to this codebase:** demonstrate the first two gates with evidence, then spend more time on Blazor rendering, API versions, and the actual test fixtures. Do not skip contribution practice.

**Limited Docker access:** continue source reading, documentation work, and pure unit tests. Database and broker verification remains pending. Rejoin the runtime stories when infrastructure is available; a source-only route is not full course completion.

**Early junior milestone:** finish stages 1-8 and demonstrate one independently reviewed contribution. Stages 9-11 deliberately stretch toward broader ownership and often benefit from pairing.

**Full course:** complete all 72 stories, pass the stage gates, and deliver the stage-12 capstone. The capstone's six slices form one finished feature; they are not six alternative projects.

## Keep your practice branches understandable

Maintain a reviewed course integration branch if you intend to build later stories on earlier code. Start independent experiments from a named baseline and document what you retained. Before the capstone, list the prerequisite code changes present in its branch. Avoid mixing unrelated migration, broker, and concurrency spikes into the final feature diff simply because you completed them earlier.

Use [assessment](03-reference/assessment.md) to decide readiness. When a gate is weak, repeat the smallest relevant exercise with different data instead of adding more unreviewed code.
