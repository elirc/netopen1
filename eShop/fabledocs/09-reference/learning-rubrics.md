# Learning Rubrics

Observable behaviors, not vibes. Grade yourself per skill: J = junior, M = mid, S = senior, plus the **interview-ready** column (what you must be able to *say/do live*).

| Skill | Junior (J) | Mid (M) | Senior (S) | Interview-ready when… |
| --- | --- | --- | --- | --- |
| Codebase navigation | finds code by grep after several tries | predicts location from architecture before searching; right ~80% | reads an unfamiliar repo's composition root + contracts first, maps it in an hour | you can answer "where would X live?" for arbitrary X in this repo in <30s |
| Flows | can follow one flow with the docs open | traces any of the six flows from memory with anchors | traces *and* names the failure mode at each hop | 3-minute checkout narration incl. idempotency, outbox, guards — no notes |
| Async/reliability | knows "events are used" | explains at-least-once, idempotency techniques, outbox with anchors | designs the missing pieces (DLX, sweeper, reconciler) with migration plans | can answer "what if this message is delivered twice / never?" for any consumer here |
| Persistence | writes working EF queries | knows tracking vs no-tracking, transaction boundaries, N+1s, and where indexes are missing | plans expand/contract migrations incl. the hidden raw-SQL reader | can whiteboard the checkout transaction's contents (4 kinds of rows) |
| AuthN/Z | can add `[Authorize]` | explains cookie-vs-JWT split, claim flow, and the three authZ styles (filter/check/by-construction) | audits endpoints for IDOR systematically; judges `ValidateAudience` tradeoffs | can do the R5 investigation live and narrate it |
| Testing | writes happy-path tests | picks the right layer per invariant; uses real-DB fixtures; avoids testing plumbing | uses test difficulty as design feedback; builds missing harnesses | can classify any proposed test into a layer, with reasons, in seconds |
| Debugging | reproduces and guesses | ranks hypotheses, probes cheaply, narrates | picks the single probe that halves the space; generalizes bug → class → systemic fix | passes sims 1–3 at Solid on the recorded rubric |
| Review | style comments | invariant-focused findings, graded severities, kind tone | approves partially, splits risk, teaches in comments | passes review sims at Solid; comments quote failure scenarios |
| Design communication | describes what code does | explains *why* with tradeoffs and one alternative | writes the RFC; prices options in failure modes; recommends against own work when warranted | 40-min system design hits every "magic sentence" in file 08/04 |
| Contribution craft | change works locally | answers the maintainer's five questions before opening | scopes minimal safe change; plans rollout/rollback | can present any completed ticket as a 2-min STAR story |

## Self-assessment checklist (run at cram-plan checkpoints)

- [ ] I re-verified an anchor today and it was where I remembered.
- [ ] I can name the six flows and each one's headline risk.
- [ ] I can state R1/R2/R3 as evidence → scenario → fix → test, 90s each.
- [ ] I have recorded myself debugging and reviewed the recording.
- [ ] Three STAR stories under 2 minutes, one of them a mistake story.
- [ ] I know which claims in my answers are confirmed vs hypothesis — and say so unprompted.

The last box is the whole game. Mid-level candidates fail deep-dives not by knowing too little but by asserting more than they verified. The habit these docs trained — *anchor or hedge* — is the interview skill.
