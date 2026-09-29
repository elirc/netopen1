# ASTRA-060: Write an incident report another developer can use

[Story index](README.md) · [Progress](../PROGRESS.md)

**Stage:** 10 — Diagnosis and operations  
**Type:** Operational handoff · **Estimate:** 3-6 hours  
**Prerequisites:** [ASTRA-059](ASTRA-059.md)  
**Read first:** [Stage lesson](../01-lessons/10-debugging-and-observability.md)

## User story

As the next developer on support, I want a clear incident report so that I can recognize and resolve the same failure quickly.

## Starting point and scope

Use one controlled failure from stages 9-10. Produce a local report and runbook with no invented production incident or impact.

- [Program.cs](../../src/eShop.AppHost/Program.cs)
- [Extensions.cs](../../src/eShop.ServiceDefaults/Extensions.cs)

## Acceptance criteria

- [ ] The report distinguishes observed facts, inferred cause, and unanswered questions.
- [ ] A timeline links symptom, evidence, experiment, restoration, and verification.
- [ ] The runbook names the specific resource and recovery check.
- [ ] One prioritized follow-up is small enough to become a separate story.

## Suggested approach

1. Use the incident template and your actual experiment notes.
2. Have a mentor or delayed self-review follow the diagnosis steps.
3. Revise unclear commands and remove sensitive output.

## Verification and evidence

Submit the incident report and a replay result for the runbook. Identify any step that remains untested instead of claiming a proven recovery path.

## Hints, in order

1. A process restart may restore new requests while leaving old messages stranded.
2. Do not assign real customer impact to a synthetic local exercise.

## Review conversation

What would someone unfamiliar with your experiment need in the first two minutes? Record the result using the [evidence template](../04-templates/story-evidence.md) and the [definition of done](../00-onboarding/04-first-contribution.md).
