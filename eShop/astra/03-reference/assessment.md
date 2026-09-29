# Assessment, review gates, and mentor guidance

Use evidence to decide readiness. Completing a file or repeating vocabulary is not enough to pass a gate.

## Score five dimensions

Score each dimension 0-3, for a maximum of 15.

| Dimension | 0: missing | 1: assisted | 2: independent | 3: transferable |
| --- | --- | --- | --- | --- |
| Understanding | Cannot explain the path | Explains with prompts | Explains inputs, state, and boundaries | Predicts a new case correctly |
| Implementation | Acceptance behavior missing | Partial behavior or substantial help | Cohesive change meets the brief | Handles an adjacent edge case without excess scope |
| Verification | No meaningful evidence | Happy path only or unclear test boundary | Appropriate positive/negative evidence | Can demonstrate what would break the test |
| Collaboration | Unreviewable work | Needs help limiting or describing diff | Clear PR and useful review response | Helps another person reason through the tradeoff |
| Judgment | Claims exceed evidence | Limits need prompting | States assumptions and limitations | Chooses a smaller or better approach from evidence |

Pass a stage with at least **10/15 and no dimension below 2**. This ensures the score cannot conceal a critical weakness. For an investigation story, “implementation” means completing the specified experiment or analysis, not inventing an unnecessary code change.

If a dimension is below 2, select one targeted remedial exercise and revisit the gate. Do not assign five more stories as punishment.

## Stage gates

| Stage | Required demonstration | If weak, repeat |
| --- | --- | --- |
| 1 | Start or precisely diagnose setup; trace a page; present a small reviewed contribution | ASTRA-004 with a different filter and ASTRA-006 |
| 2 | Explain C# state changes and show a meaningful failing/passing test | ASTRA-010 with another boundary input |
| 3 | Demo a UI improvement with URL state and keyboard evidence | ASTRA-017 from a new query |
| 4 | Explain routing versus validation and prove an API boundary | ASTRA-020 with a new extreme value |
| 5 | Show validation before persistence and recovery from cached failure | ASTRA-030 with a different interleaving |
| 6 | Explain stock or order invariants and demonstrate database rollback | ASTRA-036 at another pre-commit failure point |
| 7 | Prove discovery and test-data isolation; name each layer's limit | ASTRA-037 in a focused run and ASTRA-042 |
| 8 | Demonstrate two-user ownership and sensitive-log rejection | ASTRA-044/045 with a fresh order and ASTRA-047 |
| 9 | Trace the event chain and explain publish/consume failure windows | ASTRA-051 with a new interruption point |
| 10 | Diagnose a controlled outage and verify recovery with evidence | ASTRA-056 and a revised ASTRA-060 report |
| 11 | Defend an ADR, test its assumption, and lead a review | ASTRA-061 with a challenged assumption |
| 12 | Deliver the complete capstone across API, UI, tests, and handoff | The specific capstone slice with missing evidence |

Keep scores, dates, reviewer identity or self-review method, and follow-ups in [PROGRESS.md](../PROGRESS.md). A blocked database or browser check remains pending; it cannot receive an evidence score of 2 based on source reading alone.

## Capstone rubric

In addition to the five dimensions, require every row below:

- [ ] V2 filtering, defaults, invalid input, filter composition, counts, and pagination are covered.
- [ ] V1 compatibility has explicit evidence.
- [ ] Shared client and implementer changes are coherent.
- [ ] UI state survives refresh and navigation and includes empty recovery.
- [ ] Browser tests are discovered in the intended project.
- [ ] Dataset ownership makes results reproducible.
- [ ] Performance and failure claims match measurements.
- [ ] The PR, demo, and local runbook explain limitations.
- [ ] No critical acceptance gap remains hidden by a green subset of tests.
- [ ] The learner can explain the implementation and test boundary without a supplied script.

Graduation means independent contribution within this codebase's learned scope. It does not imply production expertise in every service or guarantee readiness to own payment, identity, or infrastructure systems alone.

## A 30-minute mentor review

1. Five minutes: learner states the user problem and predicts an edge case.
2. Ten minutes: learner demonstrates the result and one regression test.
3. Ten minutes: reviewer asks about a boundary, a failure, and a tradeoff.
4. Five minutes: agree on a score and one next step.

Ask before showing the answer: “Where is that value trusted?”, “What would the test do if the service returned no rows?”, or “Which side effect proves completion?” Offer the first hint, then let the learner investigate.

## Self-study route

Leave a short gap between implementation and review. Read only the story and diff, rerun the documented commands, and explain the behavior aloud. Change a test input or deliberately break a local assertion to verify understanding, then restore the working result. Score conservatively and identify which conclusions still need an external review.

## Working with coding assistance

You may use an assistant to explain syntax, suggest edge cases, or review a bounded diff. Before accepting generated code, predict what it does, inspect every changed line, and run the relevant checks. You remain responsible for the evidence and explanation. If you cannot explain an abstraction, simplify it or ask for a lesson before keeping it.
