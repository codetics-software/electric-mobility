# OCPP 2.0.1 engineering guide

Use this guide with the [2.0.1 JSON message cards](messages/2.0.1/) and [WebSocket runtime](websocket-and-runtime.md). The cards contain fields from the OCA Part 3 schema package; no PDF is needed for routine implementation. OCA 2.0.1 edition 4 prose and June 2026 errata can be newer than that schema package, so check the relevant correction before claiming exact edition 4 conformance. Optional Device Model appendices can change independently; record the appendix revision used by a vendor or test suite.

Read the [June 2026 errata digest](errata-2026-06.md) for corrected remote start, RPC, reset, firmware, and transaction behavior.

## Model and flow

- Negotiate `ocpp2.0.1`. Do not translate 1.6 payloads by renaming actions: the station/EVSE/connector hierarchy, transaction semantics, and configuration model changed.
- `BootNotification` and `StatusNotification` describe provisioning/availability; `TransactionEvent` carries transaction progression. Correlate events by station, transaction ID, event type, and `seqNo`. Handle offline and out-of-order events before calculating final state.
- The station generates the transaction ID, unlike the CSMS-assigned ID in 1.6. Transaction-related start, stop, meter, and status evidence moves into `TransactionEvent`; `StatusNotification` remains for connector availability. Model that distinction when migrating.
- Use the Device Model component/variable/attribute model for configuration, inventory, and monitoring. Query supported components and characteristics; avoid hard-coded assumptions that every station exposes every variable.
- OCPP 2.0.1 has JSON/WebSocket transport and no SOAP transport. Check subprotocol negotiation, frame/schema validation, and optional compression before blaming application state.
- Treat `RequestStartTransaction` and `RequestStopTransaction` responses as request handling. Confirm the resulting `TransactionEvent` and meter evidence before updating operational or financial finality.
- Design authorization around `idToken`, cache/local list, certificate-related paths, and the chosen ISO 15118 capability. Record the decision source and expiry; do not treat cached authorization as perpetual.
- Smart charging, firmware, diagnostics, display messages, and certificate management depend on functional blocks and profiles. Build a capability matrix per model/firmware.

## Debugging and security traps

- Compare wire payloads with the matching JSON schema, then with the use case. A schema-valid payload can still be semantically invalid for the station state.
- Detect transaction event gaps and duplicates using `seqNo` within transaction context; do not interpret an isolated `Ended` event as complete metering history.
- Check the configured security profile, TLS chain, CSMS identity, station credential/certificate, and certificate lifecycle. Limit device variable writes and firmware operations to authorized operators; audit before/after values and results.
- Distinguish station clock drift from server receive time. Preserve original event timestamps and ingestion timestamps separately.

Official version overview: <https://openchargealliance.org/protocols/open-charge-point-protocol/>.
