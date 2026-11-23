# Securing payments, public charging, and billing

Read [the security gate](README.md) first. Pair this guide with
[charging lifecycles](../charging-lifecycles.md) and, for roaming payments,
[direct payment](../ocpi/direct-payment.md). Stripe is used as the example provider;
apply the same rules to any provider. Legal requirements for ad-hoc payment, price
display, and metering depend on the country, so verify them for the deployment.

## The threat model

Whoever is standing at a charger can edit requests, replay them, and share links. They
want free energy, someone else's refund, or a stranger's session. An operator's QR
sticker can be replaced by a fraudster's sticker. A provider's notifications can arrive
late, twice, or out of order.

## The order of trust

```text
Browser says "paid"           -> proves nothing
Redirect to success page      -> proves nothing
Station says "Accepted"       -> proves the station took the request
Signed provider notification  -> proves payment, once matched to the order
Station's start message       -> proves a transaction began
Meter values                  -> evidence of energy, subject to sanity checks
Final meter reading           -> the basis for the final amount
```

## Creating a payment

**The server chooses everything that matters.** The browser sends only the charge point
reference, a credit amount within limits, a request ID, and its tracking secret. The
server resolves tenant, station, connector, tariff, currency, and connected account
from its own records.

- **Check availability under a lock**, so that two people cannot pay for one connector.
- **Freeze the tariff.** Copy prices onto the order at creation. Later edits must not
  change what this driver pays.
- **Bound the credit** with a minimum and a maximum.
- **Make retries safe.** The same request ID must return the same order, and must also
  present the original tracking secret, so a guessed request ID cannot reveal someone
  else's checkout. A reused ID with a different connector or amount is refused.
- **Give a stable idempotency key to every provider call**, derived from the order.
- **Fail closed.** With no provider key or encryption key, payment is unavailable. It
  does not fall back to a free mode. A test payment adapter must be unreachable in
  production.

## Provider notifications

- **Verify the signature on the raw bytes**, before parsing. Check the timestamp, so old
  captured notifications fail. Keep the webhook out of CSRF and session handling, but
  never skip the signature.
- **Match every field to the order under a lock:** connected account, checkout ID,
  amount, currency, and payment intent. Any mismatch is refused and investigated.
- **On a multi-account platform, the account check is critical.** Without it, a payment
  on one tenant's account could activate a session for another tenant.
- **Deduplicate by event ID, in the same transaction as the effect.** A check outside
  the transaction leaves a window for concurrent duplicates.
- **Handle disorder.** If the notification arrives before you stored the checkout ID,
  return a retryable error so the provider redelivers. Do not drop it.
- **Handle delayed methods.** "Checkout completed" may arrive with payment still
  pending. Start only when the status says paid.
- **Paid but no longer valid** (order expired, station offline, disabled): refund
  automatically and do not start.

## Starting and stopping

- **Use a narrow, temporary authorization.** After payment, issue a token limited to
  that station and connector, with a short lifetime. It cannot start any other
  connector, and it is consumed at start and disabled at the end.
- **Refund in full if it does not start.** A station refusal or no start within the
  window (five minutes works in practice) triggers a refund. A late station report must
  not then begin an unpaid session; decide this rule explicitly and test it.
- **Be honest about stopping.** Running out of credit requests a stop, but a station
  that does not answer keeps delivering. Exposure is therefore not capped by the credit
  while a station is unresponsive. Cap what you **bill** at the credit, record any
  overrun for the operator, and never display "stopped" before confirmation.
- **Keep a session limit.** A maximum duration and an implausible-energy threshold catch
  stuck or falsified sessions.

## Meter evidence and the final amount

- **Bill from the final reading**, and refund the rest only after it arrives. Do not
  refund based on a live estimate.
- **Never let a value reduce the charge by accident.** Clamp negative energy to zero,
  use the highest observed reading while live, and ignore samples dated before the
  start or too far ahead. Allow a small clock skew.
- **Keep signed readings exactly as received.** Signed meter data such as OCMF supports
  later verification with transparency software, and any change breaks it. Meter-law
  rules such as Germany's Eichrecht may require this, so check the deployment's country.
- **Use exact arithmetic and a documented rounding rule.** Use decimal or minor units,
  and test rounding at half a cent and time at second granularity.
- **Separate energy from money facts.** Store the measured energy, the tariff snapshot,
  and the amount, so that a dispute can be recalculated.

## Public tracking

A driver without an account follows the session with a secret only their browser knows.

- **Generate 256 bits or more from a CSPRNG**, sent in a request header rather than a
  URL, because URLs leak into history, logs, and referrers. Keep it in session-scoped
  browser storage.
- **Store a hash for checking.** Encrypt a copy only if a recovery path needs it.
- **Compare in constant time.** A wrong secret returns the same not-found as a missing
  order, so order IDs cannot be probed.
- **Grant the minimum.** The secret reads this session and can request a stop. It gives
  no dashboard access, no other sessions, and no personal details.

## QR codes and portals

- **Treat stickers as replaceable.** Encode a single HTTPS URL on your own domain, show
  the operator's identity and the station on the page, and tell drivers what to check.
  Inspect QR stickers during site visits.
- **Do not put secrets in a QR code.** It is printed on a public object.
- **Have the app parse scanned codes strictly.** Accept only known hosts and schemes,
  and never open arbitrary URLs from a scan.
- **Use the provider's hosted page** so that card data never touches your systems. This
  shrinks your PCI DSS scope; confirm your exact scope with the provider.
- **Tie each published charge point** explicitly to tenant, station, connector, and
  tariff. Unpublishing must take effect immediately.

## Refunds

- Only the server initiates refunds, and only from recorded state, never from a client
  amount.
- Refund at most the unused amount, with an idempotency key, and never twice.
- A refused refund is visible to the operator, and the driver's state stays accurate
  rather than claiming the refund succeeded.
- Operator-initiated refunds need a role check and an audit entry with a reason.

## Connected accounts, invoices, and cards

- **Keep each tenant on its own connected account.** Never accept an account ID from a
  client. Verify the account is ready before enabling payments.
- **Invoices are records.** Correct them with credit notes rather than editing them.
- **Physical cards and wallet passes:** the printed or NFC number activates only for the
  person who ordered it. A card awaiting activation is refused by the station. Check
  both NFC byte orders, because readers differ. A number from someone else's order must
  not activate, and an assigned card cannot be reused.
- **Wallet signing keys** are production secrets, kept with the same care as payment
  keys.

## Tests every payment change needs

- Forged, altered, and old webhook signatures are refused.
- Mismatched account, checkout, amount, or currency does not start anything.
- A duplicate webhook has one effect, including under concurrency.
- A notification arriving before the checkout ID is stored gets a retryable response.
- A delayed payment method waits for the paid status.
- A retried checkout creates one order and one charge.
- A public token cannot start another connector.
- A station refusal and a start timeout each produce a full refund.
- An unused balance is refunded only after the final reading.
- Billing never exceeds the credit, and negative energy cannot reduce the amount.
- The wrong tracking secret gets the same response as a missing order.
- A public route without a valid secret cannot read or stop a session.
