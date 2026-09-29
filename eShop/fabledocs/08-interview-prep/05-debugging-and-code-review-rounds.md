# Debugging & Code Review Rounds — Timed Simulations

Seven simulations converted from modules 04/05. Run each with a timer, **out loud** (the narration is what's graded). If possible, have a friend read the "interviewer follow-ups" at you.

## Grading rubric (all sims)

- **Basic:** reached the answer eventually.
- **Solid (hire, mid-level):** stated hypotheses *before* probing; chose cheap probes; narrated dead ends without flailing; correct root cause + a regression test.
- **Strong:** ranked hypotheses by probability × probe cost; generalized the bug to its class; proposed the systemic fix.

---

## Debugging Sim 1 (25 min): The basket that wouldn't die
Setup: read scenario 1 in [../05-quality-engineering/03-systematic-debugging.md](../05-quality-engineering/03-systematic-debugging.md), then simulate *without* re-reading it.
Prompt: "Users report items reappearing in the cart after checkout. You have the dashboard, Redis CLI, and the code. Go."
Interviewer follow-ups: "Redis is empty but the UI shows 3 items — now what?" (cache invalidation in `BasketState.CheckoutAsync`); "How do you prove it before fixing it?" (breakpoint/log on `_cachedBasket` after checkout); "What's your regression test?"

## Debugging Sim 2 (25 min): The frozen order
Prompt: "Order #83 has said 'awaiting validation' for two hours. Nothing is erroring on the dashboards. Find it."
Expected path: hop checklist (Ordering published? Catalog received? Catalog published? Ordering received?) → the ack-on-error discovery (`RabbitMQEventBus.cs:L177-L180`).
Follow-ups: "The Catalog log shows 'Error Processing message' once, yesterday. Explain the mechanism." → "Fix it tonight vs fix it right — what's each?" (tonight: manually publish/set status via SQL + event; right: DLX, M2).

## Debugging Sim 3 (20 min): 200 OK, zero orders
Prompt: scenario 3 (validation swallow). The twist to handle live: interviewer insists "but the API returned success!" — your job is to *distrust the status code out loud* and walk logs → validator → catch-all.
Follow-up: "You can change one file before the demo tomorrow — which and why?" (`OrdersApi` result check = smallest honest change; say why not the handler rewrite under time pressure.)

## Debugging Sim 4 (15 min): Everyone's logged out
Prompt: scenario 5 (the deleted `sub`-claim mapping line). This one is speed practice — auth config bugs reward pattern recognition. Target: name the three hypotheses (token missing / rejected / claims remapped) inside the first two minutes.

## Review Sim 1 (20 min): Kata 2 (parallelize event handlers)
Prompt: "Review this PR; the author is a strong engineer having a normal day."
Graded on: finding the scoped-DbContext hazard, *and* the delivery — you must (a) acknowledge the legit motivation (the `// REVIEW` comment invited it), (b) block with a failure scenario, (c) offer the safe alternative.
Follow-up: "The author replies 'we've run it in staging for a week, no issues.' Respond." (Intermittent thread-safety bugs and staging load; propose a load test or scope-per-handler — evidence over rank.)

## Review Sim 2 (20 min): Kata 6 (CreatedAt + smuggled rename)
Graded on: separating the three changes by risk (additive column: fine; build-time default: bug; rename: breaking) and *requesting a split PR* rather than a rewrite.
Follow-up: "Which part would you approve today?" — the ability to approve *something* is graded.

## Review Sim 3 (25 min): Kata 4 (admin delete endpoint)
The security-flavored round. Graded on: spotting the isolation-model break before style comments; asking "who calls this and from where" (trust boundary) before proposing mechanism.
Follow-up: "Support really needs this by Friday." — scope the safe minimum (internal-only network policy + admin scope + audit log) and say what you're explicitly deferring.

---

Rehearsal protocol: never more than two sims per day; record yourself once per week and listen for filler ("umm, let me just check…") vs narration ("I'm checking X because it splits the space in half"). The second phrasing, habitual, is worth more than any additional technical prep.
