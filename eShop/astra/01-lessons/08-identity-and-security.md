# Enforce identity at the boundary that owns the data

Learning goal: tell authentication from authorization and verify ownership with more than one user.

## Trace identity

[WebApp authentication setup](../../src/WebApp/Extensions/Extensions.cs) uses cookies and OpenID Connect and requests relevant scopes. The WebApp attaches tokens to downstream clients. [Ordering Program.cs](../../src/Ordering.API/Program.cs) requires authorization on its orders route group.

Authentication establishes who is calling. Authorization determines what that caller may do. A signed-in user is not automatically allowed to read or cancel every order.

Compare list and detail queries in [OrderQueries](../../src/Ordering.API/Application/Queries/OrderQueries.cs). The list filters by buyer identity; the detail query takes only an order ID. Follow the API and command paths before concluding where an ownership check belongs.

## A two-user test matrix

| Caller | Target order | Proposed course behavior |
| --- | --- | --- |
| Anonymous | Any | Authentication rejects access |
| Alice | Alice's | Allowed operation, subject to domain rules |
| Bob | Alice's | No read or mutation; use the documented concealed-not-found policy |
| Alice | Missing | Not found |
| Alice | Alice's paid order | Domain cancellation restriction still applies |

These are proposed exercise requirements, not a description of every current endpoint. Test both reads and writes. A hidden UI button is not an authorization check.

The functional fixture inserts an identity for tests. Adapt its setup to supply controlled principals per request; do not accidentally test only the hard-coded user. Preserve a browser sign-in check to cover the actual configured authentication path.

## Trust the authenticated identity

CreateOrderRequest includes user identity fields. The request body is caller-controlled. Stage 8 asks you to derive the acting user's identity from the trusted principal and test conflicting payload values. Continue to validate domain data separately.

Do not expand this exercise into a new administration system. Keep the owner-only course policy explicit, including any future administrative exception that remains out of scope.

## Validate before slicing strings

CreateOrderAsync masks a card number with Substring before the command validator executes. A short or null string can fail before intended validation. The sample uses simulated payment; the exercise is input validation and error handling, not implementation of a payment system.

Test absent, short, and ordinary sample values and confirm invalid input reaches no mediator mutation. Avoid teaching a masking function as secure storage or payment compliance.

## Logs are an output surface

The invalid request-ID path currently logs the request object. Command and transaction logging also destructure payloads. Read these paths before claiming the normal-path masking protects every output.

Use fixed synthetic marker values in a test request, capture structured logger state, and assert those markers do not appear in fields or rendered messages. Keep safe correlation identifiers useful. Test exception branches as well as success.

Local exercises use synthetic data only. Review changes through the same contribution workflow as other behavior changes, including a clear reason for any status or contract change.

## Checkpoint

Explain why a green test calling OrdersApi.GetOrderAsync directly cannot prove real authentication, and why a passing “Alice reads Alice” test cannot prove ownership isolation. Complete the two-user matrix and a sensitive-output test before passing this stage.
