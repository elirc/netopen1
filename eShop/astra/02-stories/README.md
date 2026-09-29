# User story index

[Bootcamp home](../README.md) · [Curriculum](../CURRICULUM.md) · [Progress](../PROGRESS.md)

These 72 briefs are progressively harder practice assignments. Read the linked lesson first. Complete prerequisites before dependent work; they include both skills and any earlier code the story explicitly builds on. A number is a recommended reading order, not permission to skip a prerequisite because another story looks easier.

Kinds include characterization (preserve and explain current behavior), proposed features (implement the stated new policy), investigations (deliver evidence), and spikes (test a design with explicit limits). Use a practice branch; these are not published upstream issues.

Every story has acceptance criteria, source links, a suggested approach, verification evidence, two hints, and a review question. Use hints only after recording a prediction. Apply the shared definition of done in addition to the story-specific criteria.

## Stage 1: Onboard and contribute

Read [the stage lesson](../00-onboarding/04-first-contribution.md). Typical story estimate: 1-2 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-001](ASTRA-001.md) | Record a reproducible workstation | Guided onboarding | None |
| [ASTRA-002](ASTRA-002.md) | Launch and tour the local store | Guided runtime lab | [ASTRA-001](ASTRA-001.md) |
| [ASTRA-003](ASTRA-003.md) | Create a one-page codebase map | Code reading | [ASTRA-002](ASTRA-002.md) |
| [ASTRA-004](ASTRA-004.md) | Trace a catalog request with real values | Guided debugging | [ASTRA-003](ASTRA-003.md) |
| [ASTRA-005](ASTRA-005.md) | Make a small onboarding documentation contribution | First contribution | [ASTRA-004](ASTRA-004.md) |
| [ASTRA-006](ASTRA-006.md) | Practice a full review cycle | Collaboration lab | [ASTRA-005](ASTRA-005.md) |

## Stage 2: C# and focused tests

Read [the stage lesson](../01-lessons/02-csharp-and-testing-basics.md). Typical story estimate: 1-3 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-007](ASTRA-007.md) | Explain the C# shapes used by this app | Language lab | [ASTRA-006](ASTRA-006.md) |
| [ASTRA-008](ASTRA-008.md) | Characterize order totals with meaningful values | First unit test | [ASTRA-007](ASTRA-007.md) |
| [ASTRA-009](ASTRA-009.md) | Prove repeated product additions merge correctly | Unit-test practice | [ASTRA-008](ASTRA-008.md) |
| [ASTRA-010](ASTRA-010.md) | Test domain guard boundaries | Boundary testing | [ASTRA-009](ASTRA-009.md) |
| [ASTRA-011](ASTRA-011.md) | Verify anonymous basket reads never reach storage | Mock-boundary testing | [ASTRA-010](ASTRA-010.md) |
| [ASTRA-012](ASTRA-012.md) | Trace async completion and cancellation | Async characterization | [ASTRA-011](ASTRA-011.md) |

## Stage 3: Blazor and accessible UI

Read [the stage lesson](../01-lessons/03-blazor-and-browser.md). Typical story estimate: 2-4 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-013](ASTRA-013.md) | Give an empty catalog a recovery action | First UI feature | [ASTRA-006](ASTRA-006.md), [ASTRA-012](ASTRA-012.md) |
| [ASTRA-014](ASTRA-014.md) | Make pagination understandable to assistive technology | Accessibility improvement | [ASTRA-013](ASTRA-013.md) |
| [ASTRA-015](ASTRA-015.md) | Help shoppers recover from a missing product | UI recovery | [ASTRA-014](ASTRA-014.md) |
| [ASTRA-016](ASTRA-016.md) | Give cart quantity controls distinct labels | Accessible forms | [ASTRA-015](ASTRA-015.md) |
| [ASTRA-017](ASTRA-017.md) | Lock in filter reset behavior | Browser characterization | [ASTRA-016](ASTRA-016.md) |
| [ASTRA-018](ASTRA-018.md) | Normalize invalid UI page numbers | UI input handling | [ASTRA-017](ASTRA-017.md) |

## Stage 4: HTTP and API contracts

Read [the stage lesson](../01-lessons/04-http-and-contracts.md). Typical story estimate: 3-5 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-019](ASTRA-019.md) | Document the catalog HTTP response contract | API investigation | [ASTRA-018](ASTRA-018.md) |
| [ASTRA-020](ASTRA-020.md) | Reject invalid catalog pagination before querying | API validation feature | [ASTRA-019](ASTRA-019.md) |
| [ASTRA-021](ASTRA-021.md) | Make catalog pagination stable for tied names | Query correction | [ASTRA-020](ASTRA-020.md) |
| [ASTRA-022](ASTRA-022.md) | Prove version 2 filters compose correctly | Contract tests | [ASTRA-021](ASTRA-021.md) |
| [ASTRA-023](ASTRA-023.md) | Preserve missing-order and service-failure meanings | Error handling correction | [ASTRA-022](ASTRA-022.md) |
| [ASTRA-024](ASTRA-024.md) | Validate short checkout input before masking | Defensive API coding | [ASTRA-023](ASTRA-023.md) |

## Stage 5: Basket and state

Read [the stage lesson](../01-lessons/05-basket-and-state.md). Typical story estimate: 3-5 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-025](ASTRA-025.md) | Test unauthenticated basket mutations | gRPC boundary tests | [ASTRA-024](ASTRA-024.md) |
| [ASTRA-026](ASTRA-026.md) | Validate basket product IDs and quantities | gRPC validation feature | [ASTRA-025](ASTRA-025.md) |
| [ASTRA-027](ASTRA-027.md) | Reject duplicate rows in one basket update | Contract consistency | [ASTRA-026](ASTRA-026.md) |
| [ASTRA-028](ASTRA-028.md) | Make successful basket deletion invalidate display state | State correction | [ASTRA-027](ASTRA-027.md) |
| [ASTRA-029](ASTRA-029.md) | Handle products missing from a basket's catalog lookup | Cross-service recovery | [ASTRA-028](ASTRA-028.md) |
| [ASTRA-030](ASTRA-030.md) | Allow recovery after a failed basket load | Async-state recovery | [ASTRA-029](ASTRA-029.md) |

## Stage 6: Persistence and domain rules

Read [the stage lesson](../01-lessons/06-data-and-domain.md). Typical story estimate: 3-6 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-031](ASTRA-031.md) | Characterize catalog stock arithmetic | Domain testing | [ASTRA-030](ASTRA-030.md) |
| [ASTRA-032](ASTRA-032.md) | Reject negative restocking without changing state | Domain correction | [ASTRA-031](ASTRA-031.md) |
| [ASTRA-033](ASTRA-033.md) | Turn order transitions into a tested state table | Domain characterization | [ASTRA-032](ASTRA-032.md) |
| [ASTRA-034](ASTRA-034.md) | Measure a read-only order-query improvement | Query experiment | [ASTRA-033](ASTRA-033.md) |
| [ASTRA-035](ASTRA-035.md) | Rehearse a backward-compatible schema addition | Migration practice | [ASTRA-034](ASTRA-034.md) |
| [ASTRA-036](ASTRA-036.md) | Prove order writes roll back together | Transaction integration lab | [ASTRA-035](ASTRA-035.md) |

## Stage 7: Reliable test suites

Read [the stage lesson](../01-lessons/07-testing-strategy.md). Typical story estimate: 3-6 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-037](ASTRA-037.md) | Remove catalog tests' dependence on global counts | Test reliability correction | [ASTRA-036](ASTRA-036.md) |
| [ASTRA-038](ASTRA-038.md) | Create reusable test data without hidden state | Test maintainability | [ASTRA-037](ASTRA-037.md) |
| [ASTRA-039](ASTRA-039.md) | Make a new browser test discoverable | Test infrastructure | [ASTRA-038](ASTRA-038.md) |
| [ASTRA-040](ASTRA-040.md) | Isolate logged-in basket browser scenarios | Browser reliability | [ASTRA-039](ASTRA-039.md) |
| [ASTRA-041](ASTRA-041.md) | Test authentication boundaries honestly | Fixture audit | [ASTRA-040](ASTRA-040.md) |
| [ASTRA-042](ASTRA-042.md) | Publish a risk-based test plan for a feature | Quality planning | [ASTRA-041](ASTRA-041.md) |

## Stage 8: Identity and defensive coding

Read [the stage lesson](../01-lessons/08-identity-and-security.md). Typical story estimate: 4-7 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-043](ASTRA-043.md) | Build an order authorization matrix | Security investigation | [ASTRA-042](ASTRA-042.md) |
| [ASTRA-044](ASTRA-044.md) | Restrict order detail reads to the owner | Authorization feature | [ASTRA-043](ASTRA-043.md), [ASTRA-023](ASTRA-023.md) |
| [ASTRA-045](ASTRA-045.md) | Restrict order mutations to the owner | Authorization feature | [ASTRA-044](ASTRA-044.md) |
| [ASTRA-046](ASTRA-046.md) | Derive checkout identity from the authenticated caller | Trust-boundary correction | [ASTRA-045](ASTRA-045.md), [ASTRA-024](ASTRA-024.md) |
| [ASTRA-047](ASTRA-047.md) | Keep checkout secrets out of every log path | Sensitive-output correction | [ASTRA-046](ASTRA-046.md) |
| [ASTRA-048](ASTRA-048.md) | Validate webhook subscription ownership locally | Authorization review lab | [ASTRA-047](ASTRA-047.md) |

## Stage 9: Events and consistency

Read [the stage lesson](../01-lessons/09-events-and-consistency.md). Typical story estimate: 4-8 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-049](ASTRA-049.md) | Trace checkout to its eventual order status | Distributed code reading | [ASTRA-048](ASTRA-048.md) |
| [ASTRA-050](ASTRA-050.md) | Characterize duplicate command handling | Idempotency testing | [ASTRA-049](ASTRA-049.md), [ASTRA-012](ASTRA-012.md) |
| [ASTRA-051](ASTRA-051.md) | Map integration-event log failure windows | Consistency investigation | [ASTRA-050](ASTRA-050.md), [ASTRA-036](ASTRA-036.md) |
| [ASTRA-052](ASTRA-052.md) | Prototype duplicate-safe stock processing | Advanced consistency spike | [ASTRA-051](ASTRA-051.md), [ASTRA-032](ASTRA-032.md) |
| [ASTRA-053](ASTRA-053.md) | Observe failed-message acknowledgement and propose recovery | Broker reliability lab | [ASTRA-052](ASTRA-052.md) |
| [ASTRA-054](ASTRA-054.md) | Test an additive event-contract change | Compatibility lab | [ASTRA-053](ASTRA-053.md) |

## Stage 10: Diagnosis and operations

Read [the stage lesson](../01-lessons/10-debugging-and-observability.md). Typical story estimate: 3-6 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-055](ASTRA-055.md) | Produce a cross-service diagnostic trace | Observability lab | [ASTRA-054](ASTRA-054.md) |
| [ASTRA-056](ASTRA-056.md) | Compare liveness and readiness during an outage | Operational experiment | [ASTRA-055](ASTRA-055.md) |
| [ASTRA-057](ASTRA-057.md) | Propagate cancellation through a background database read | Async reliability feature | [ASTRA-056](ASTRA-056.md), [ASTRA-012](ASTRA-012.md) |
| [ASTRA-058](ASTRA-058.md) | Measure a catalog page with a repeatable workload | Performance investigation | [ASTRA-057](ASTRA-057.md), [ASTRA-021](ASTRA-021.md) |
| [ASTRA-059](ASTRA-059.md) | Make webhook HTTP failures observable | HTTP reliability feature | [ASTRA-058](ASTRA-058.md), [ASTRA-048](ASTRA-048.md) |
| [ASTRA-060](ASTRA-060.md) | Write an incident report another developer can use | Operational handoff | [ASTRA-059](ASTRA-059.md) |

## Stage 11: Design and delivery

Read [the stage lesson](../01-lessons/11-design-and-delivery.md). Typical story estimate: 4-8 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-061](ASTRA-061.md) | Write an ADR for concurrent basket updates | Design decision | [ASTRA-060](ASTRA-060.md), [ASTRA-030](ASTRA-030.md) |
| [ASTRA-062](ASTRA-062.md) | Prototype one basket concurrency strategy | Design spike | [ASTRA-061](ASTRA-061.md) |
| [ASTRA-063](ASTRA-063.md) | Refactor one shared-client seam without changing behavior | Maintainability refactor | [ASTRA-062](ASTRA-062.md) |
| [ASTRA-064](ASTRA-064.md) | Make the contribution's checks discoverable in CI | Delivery tooling | [ASTRA-063](ASTRA-063.md), [ASTRA-039](ASTRA-039.md) |
| [ASTRA-065](ASTRA-065.md) | Rehearse local release and rollback | Delivery lab | [ASTRA-064](ASTRA-064.md), [ASTRA-035](ASTRA-035.md) |
| [ASTRA-066](ASTRA-066.md) | Lead a focused feature review | Independent contribution gate | [ASTRA-065](ASTRA-065.md) |

## Stage 12: Capstone: available products

Read [the stage lesson](../01-lessons/12-capstone.md). Typical story estimate: 4-8 hours; the larger spikes have individual estimates.

| Story | Assignment | Type | Prerequisites |
| --- | --- | --- | --- |
| [ASTRA-067](ASTRA-067.md) | Define the availability-filter capstone | Capstone planning | [ASTRA-066](ASTRA-066.md) |
| [ASTRA-068](ASTRA-068.md) | Implement the version 2 in-stock API filter | Capstone API slice | [ASTRA-067](ASTRA-067.md), [ASTRA-020](ASTRA-020.md), [ASTRA-021](ASTRA-021.md), [ASTRA-022](ASTRA-022.md) |
| [ASTRA-069](ASTRA-069.md) | Connect the shared client and catalog toggle | Capstone UI slice | [ASTRA-068](ASTRA-068.md), [ASTRA-013](ASTRA-013.md), [ASTRA-017](ASTRA-017.md), [ASTRA-063](ASTRA-063.md) |
| [ASTRA-070](ASTRA-070.md) | Prove the capstone in the browser and across versions | Capstone test slice | [ASTRA-069](ASTRA-069.md), [ASTRA-039](ASTRA-039.md), [ASTRA-040](ASTRA-040.md), [ASTRA-042](ASTRA-042.md) |
| [ASTRA-071](ASTRA-071.md) | Evaluate capstone performance and failure behavior | Capstone operational slice | [ASTRA-070](ASTRA-070.md), [ASTRA-058](ASTRA-058.md), [ASTRA-060](ASTRA-060.md) |
| [ASTRA-072](ASTRA-072.md) | Deliver and teach the completed capstone | Final assessment | [ASTRA-071](ASTRA-071.md), [ASTRA-065](ASTRA-065.md), [ASTRA-066](ASTRA-066.md) |
