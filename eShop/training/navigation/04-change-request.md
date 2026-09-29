# Change request: retry stranded outbox events

**From:** Ops (fictional, written for this exercise — not an upstream eShop issue)
**To:** you, as the engineer picking this up

> "We had a five-minute RabbitMQ blip last week. Support tells us at least one customer's order sat in
> `AwaitingValidation` far longer than normal and we had to manually poke it. Looking at the code, it seems like
> if the broker publish fails right after an order commits, that event — and maybe the order — is just stuck
> with nobody watching it. Can you make stranded integration events retry automatically? We don't need it
> instant, a minute or two of delay before recovery is fine. We do need it to not become a worse problem than the
> one it's fixing — no duplicate-order storms, no hammering a broker that's still down."

## Your task

**Before writing or asking an agent to write any code**, answer these in writing:

1. Which project(s)/files does this change touch? Name them specifically — don't say "the backend."
2. Does the existing `IIntegrationEventLogService` interface (`src/IntegrationEventLogEF/Services/IIntegrationEventLogService.cs`)
   support what you need, or does it need a new method? If a new method, what's its signature, and what query does
   it run?
3. Where does the retry loop itself live — an existing `BackgroundService`, a new one, or something else? Which
   existing worker in this repo is the closest architectural precedent, and why is (or isn't) it a good template?
4. This repo currently registers `IIntegrationEventLogService` **per service, generic over that service's own
   `DbContext`** (`Catalog.API` and `Ordering.API` each register their own). What does that mean for whether your
   retry mechanism is one shared component or one per service? Say which, and why.
5. What stops your sweeper from re-publishing the same event twice in a way that causes real harm (as opposed to
   a harmless duplicate)? Name the specific downstream mechanism(s) that make redelivery safe today, and whether
   they cover *every* event type this sweeper might touch or only some.
6. What test would you add, and where, to prove the sweeper actually recovers a stranded event? Name the test
   project and roughly what it needs to simulate (hint: how would you make a publish "fail" in a test without a
   real broker outage?).
7. What's the one thing that could make this change **worse** than doing nothing — i.e., what's the failure mode
   of the sweeper itself, and how would you bound it?

Write your answers in your own workbook (see `astra/04-templates/` for a template, or just a plain markdown
file) before opening `_answers/04-change-request.md`. There is no code to write for this exercise — READ-tier
projects in this apprenticeship don't get source edits; this is a placement/design exercise only.

## Constraints

- Don't touch `src/` — this is a design exercise, not an implementation task, for this project.
- Your answer should read like a design-note comment on a real PR, not a tutorial. Cite files and, where you've
  opened them, approximate line numbers or method names.
- If you genuinely don't know something (e.g. exact registration lifetime), write "UNKNOWN — needs inspection"
  rather than guessing confidently. That's the honest failure mode; grading rewards it.

## Related reading

`navigation/01-checkout-outbox-correctness.md` (row 4) and `navigation/03-outbox-sweeper-tradeoff.md` cover the
exact gap this request is asking you to close, including one candidate option already ruled out (inline retry)
and why. Read both before answering question 3.
