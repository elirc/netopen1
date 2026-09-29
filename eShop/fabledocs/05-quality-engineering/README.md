# 05 — Quality Engineering

How this system is (and isn't) kept correct, fast, secure, and observable.

| File | Focus |
| --- | --- |
| [01-testing-strategy.md](01-testing-strategy.md) | The three real test layers, what belongs where, flake prevention |
| [02-writing-tests-here.md](02-writing-tests-here.md) | Six recipes using this repo's actual helpers |
| [03-systematic-debugging.md](03-systematic-debugging.md) | The method + five repo-specific scenarios |
| [04-performance-thinking.md](04-performance-thinking.md) | Measure-first; likely hotspots with anchors |
| [05-security-checklist.md](05-security-checklist.md) | The full boundary audit + pre-merge checklist |
| [06-observability-and-operations.md](06-observability-and-operations.md) | "How would I know this broke?" per flow |

The through-line: quality is *invariants plus evidence*. Tests pin invariants; observability produces evidence; debugging is the search procedure connecting the two.
