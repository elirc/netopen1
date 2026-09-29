# Maintainer Communication

The meta-rule: **do the thinking, then ask for the decision** — never outsource the thinking. Every template below is that rule in a different costume.

## Asking a question

```markdown
I'm trying to <goal>. I expected <X> because <anchor/doc>, but observed <Y>.
I've checked: <the 2–3 things you actually checked>.
My current hypothesis: <best guess>. Am I missing something about <specific area>?
```

Bad: "checkout doesn't work, any ideas?" Good: "Expected `OrderStartedIntegrationEvent` to clear the basket (per `OrderStartedIntegrationEventHandler.cs`), but Redis still has the key. Handler log line never appears; queue bindings look right in the management UI. Is the WebApp's direct `DeleteBasketAsync` masking a subscription problem in dev?" — the second one usually answers itself while you write it. That's the point.

## Reporting a bug (repro-first)

Environment (commit, OS, Docker y/n) → minimal repro steps (numbered, from clean state) → expected vs actual → evidence (log excerpt, trace id, screenshot) → optionally a suspected cause *labeled as suspicion*. For this repo: always say whether infra containers were fresh (`ContainerLifetime.Persistent` means your Postgres may carry old state — half of all "works on my machine" here).

## Proposing a feature

Lead with the problem and who has it; sketch the smallest version; name what you're volunteering to do; ask whether the direction is welcome *before* building the big version. Maintainers reject work, not ideas — make rejecting cheap and early.

## Responding to review

- Every comment gets a response: change made ("done, <commit>"), pushback with reasoning, or a clarifying question. Silent partial fixes force the reviewer to re-diff everything.
- Pushback shape: "I went with X because <constraint>; Y would <cost>. Happy to switch if <condition> matters more — your call." State your reasoning, hand over the decision, mean it.
- When you were wrong: "Good catch — fixed in <commit>, and added a test so it stays fixed." No self-flagellation; the test is the apology.

## Respectful disagreement (the escalation ladder)

1. Understand their position well enough to state it back. 2. Find the shared goal (correctness? shipping date?). 3. Convert the disagreement into a *testable question* where possible ("if redelivery happens in practice, my concern is real — the RabbitMQ redelivered-flag metric will tell us"). 4. If still split: decide by ownership — their module, their call; note your concern in the PR and move on. Being someone whose disagreement leaves no scar tissue is a promotable trait, and behavioral interviews probe for exactly it.

Interview angle: the "tell me about a conflict/disagreement" prompt maps to step 3 — the strongest stories end with "we turned it into an experiment/metric" rather than "I convinced them."
