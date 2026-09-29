# Troubleshoot one boundary at a time

Start with the first relevant error, the exact command, the working directory, and the selected SDK. Keep a [debugging journal](../04-templates/debugging-journal.md).

| Symptom | Inspect first | Useful next action |
| --- | --- | --- |
| SDK not found or wrong major | global.json and dotnet --list-sdks | Install a compatible SDK; run from the eShop root |
| Unsupported target/workload | Chosen solution/project | Use eShop.Web.slnf for the core course; inspect any new project registration |
| Package restore failure | First feed/network/package error and nuget.config | Separate feed access from compilation; preserve the error |
| Warning causes compilation failure | Directory.Build.props and the warning code | Fix or diagnose the cause; do not globally disable warnings |
| Docker client exists but app cannot create containers | docker info server section | Start Docker and confirm Linux-container support |
| Container startup is slow | Image pull and resource logs | Distinguish downloading from unhealthy startup |
| Store unavailable while dashboard opens | webapp and downstream resource status | Inspect the first failed reference or process |
| API started alone lacks a connection | AppHost WithReference and environment setup | Run through AppHost or reproduce its required local configuration |
| HTTPS or callback mismatch | Current endpoint schemes, certificate trust, Identity callback settings | Use the matching launch path and current resource URLs |
| Functional tests fail before assertions | Fixture startup, Docker, database logs | Diagnose infrastructure before changing expected business results |
| One catalog test fails only by itself | Shared seed mutations and total-count assumptions | Revisit ASTRA-037's data ownership strategy |
| Browser test times out at startup | Port 5045, HTTP mode, webServer timeout | Stop a conflicting course instance and use the documented test mode |
| New browser test never runs | Explicit project testMatch lists | Inspect test --list and register the file deliberately |
| Logged-in tests interfere | Shared sample identity and Redis basket | Use test-owned state/identities or a documented scoped serial strategy |
| Test CLI rejects an option | MTP and selected framework's help | Use named project/solution options and runner-supported filters |
| Cart shows stale rows after mutation | BasketState cached Task and notifications | Reproduce with a primed cache, then inspect invalidation |
| Order detail returns 404 on an outage | OrdersApi's catch scope | Separate missing-data behavior from unexpected errors |
| Order appears stuck after checkout | Grace-period worker, subscriptions, event logs | Trace the next expected event and state transition |
| Failed event disappears from queue | RabbitMQEventBus acknowledgement path | Inspect catch-then-ack behavior; use an isolated failure lab |

## A worked diagnosis

Symptom: selecting a brand shows no cards.

Prediction A: the brand has no products. Call the equivalent catalog API on pageIndex 0 and inspect Count.

Prediction B: the UI retained a later page. Inspect the browser query and the API offset. CatalogSearch currently clears page on filter changes; verify the actual link and any changes made in your branch.

Prediction C: the service failed. Check the HTTP status and trace. An empty success response and a failed call require different fixes.

Choose the explanation supported by evidence. Do not simultaneously change the query, clear all data, and rewrite the component lifecycle; that destroys your ability to identify the cause.

## Preserve your evidence

Record the earliest failure and one nearby successful case. Remove credentials and dashboard tokens from copied output. Keep local infrastructure experiments scoped to named course resources, and verify recovery after restoring a dependency.

If blocked for 30 minutes, prepare a focused help request: task, command, expected result, observed result, evidence, attempted diagnosis, and the next question. Continue independent reading or unit work while runtime access is pending.
