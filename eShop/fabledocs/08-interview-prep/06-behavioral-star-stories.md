# Behavioral STAR Stories — 9 Worksheets

Sourced from the contribution tickets/projects. Do the work → fill the worksheet the same day → rehearse to under 2 minutes. If you haven't done the ticket, the worksheet still works as "studying/contributing to a large open-source codebase" — but done > described.

Format per story: Prompts it answers / Situation / Task / Action / Result / Evidence / Senior-signal details / Resume bullet / Rehearsal check (≤2 min? concrete? ends with impact?).

---

## Story 1: Learning a 19-project codebase fast
Prompts: "Tell me about ramping up on a complex system" / "How do you approach unfamiliar code?"
Source: this curriculum's Phase-1 method itself.
S: Needed working knowledge of a 7-service .NET system (eShop) with DDD, CQRS, and event-driven messaging. T: Be able to trace and modify any flow. A: Mapped the composition root first (AppHost), then contracts (routes/protos/events), then data ownership; traced six flows end-to-end with file:line notes; verified every claim by reading code, not docs. R: Could locate any behavior in minutes; found N confirmed design risks (ack-on-error, orphaned outbox rows) that the code's own comments confirmed.
Senior signals: method over heroics; evidence discipline (verified vs inferred).
Resume bullet: "Reverse-engineered a 7-service event-driven .NET system; produced a verified architecture risk register."

## Story 2: The API that returned 200 on failure (ticket 2 / kata G)
Prompts: "A time you found a serious bug" / "Disagreed with existing design."
Key A-material: traced swallowed exceptions (`IdentifiedCommandHandler` catch-all) → proved failures returned Ok() → audited the consumer before changing the contract → shipped the fix with a functional test.
Senior signals: consumer audit *before* the fix; treating a status code as a contract.
Resume bullet: "Fixed an order API that reported success on failed commands, including consumer-compatibility audit."

## Story 3: Making message loss visible (M2 / project 1)
Prompts: "Hardest technical problem" / "Improved reliability."
Key A-material: identified ack-on-exception; learned RabbitMQ queue args are immutable → designed queue migration; capped retries to avoid poison-message loops (the naive fix I *didn't* ship is part of the story).
Senior signals: the rejected first fix; migration thinking.
Resume bullet: "Designed dead-letter handling and queue migration for a RabbitMQ event bus, eliminating silent message loss."

## Story 4: The race I chose not to fix (Flow 2's lost update)
Prompts: "A tradeoff you made" / "When did you push back on scope?"
Key A-material: documented the basket's read-modify-write race, sized the blast radius (basket contents, self-correcting at price re-resolution), and argued it was acceptable — while fixing the *money-path* equivalents.
Senior signals: risk-proportional engineering; saying "no fix" with evidence. Interviewers rate this story type surprisingly highly — it shows judgment, the scarcest signal.
Resume bullet: "Prioritized concurrency fixes by blast radius, documenting accepted risks with evidence."

## Story 5: Ownership check nobody asked for (M3 / IDOR)
Prompts: "Went beyond the ticket" / "Security mindset."
Key A-material: security-checklist sweep → order-by-id lacked ownership verification → confirmed by reading the query layer → shipped filter + two-identity test, chose 404 over 403 deliberately.
Resume bullet: "Identified and closed an IDOR in an order API during a self-initiated security review."

## Story 6: The spike that prevented a bad build (M10)
Prompts: "Influencing without authority" / "A time you wrote instead of coded."
Key A-material: asked how web-tier bus consumption scales to N nodes *before* the feature request landed; delivered a one-page comparison; the recommendation was adopted (or: would be defensible to a team).
Resume bullet: "Authored architecture spike on real-time notification fan-out; recommendation adopted."

## Story 7: Test that argued for a refactor (recipe 6)
Prompts: "Improving testability/quality" / "Legacy code."
Key A-material: tried to test `BasketState` cache invalidation → concrete-class dependencies blocked it → used the test difficulty as the *evidence* in a small interface-extraction PR, rather than refactoring on taste.
Senior signals: testability pressure as design feedback — say the phrase.
Resume bullet: "Drove interface extraction with testability evidence, unlocking UI-state regression tests."

## Story 8: The mistake story (pick a real one from doing these tickets)
Prompts: "Tell me about a mistake."
Template guidance: the strongest shape from this repo's work is *"I assumed X without reading the code — my anchor/claim was wrong — I built a verification habit."* Fill it with the actual moment it happens to you during these drills (it will). End with the changed behavior, not the feeling.
Rehearsal check applies double here: under 2 minutes, zero defensiveness.

## Story 9: Teaching it back (fast-track teach-back / this curriculum)
Prompts: "Mentoring/knowledge sharing" / "Communication skills."
Key A-material: turned flow traces into teachable material (trace tables, glossary of confusables); measured success by whether a newcomer could answer the pause-and-predict questions.
Resume bullet: "Built onboarding curriculum for an event-driven microservices codebase (flows, drills, risk register)."

---

Mapping table (prompt → stories): conflict/disagreement → 2, 4, 6 · ambiguity → 1, 6 · mistake → 8 · technical tradeoff → 3, 4 · leadership/initiative → 5, 6, 9 · failure recovered → 3, 8 · learning fast → 1, 9.
Rehearsal check for all: said aloud in <2 min; contains one number or file-level concrete; ends with impact, not activity.
