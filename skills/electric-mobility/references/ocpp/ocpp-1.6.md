# OCPP 1.6 engineering guide

Use this guide with the [1.6 JSON message cards](messages/1.6/) and [WebSocket runtime](websocket-and-runtime.md). The cards contain the OCA OCPP-J schema fields, including nested meter and smart-charging structures; no PDF is needed for routine implementation. The source set was OCA OCPP 1.6 edition 2 and its JSON schema updates. Check the chosen security extension and certification profile separately; core 1.6 support does not imply them. SOAP uses a different binding.

## Model and flow

- Negotiate `ocpp1.6` for JSON over WebSocket; SOAP is a separate transport. Do not send OCPP-J frames to a SOAP endpoint.
- Track charge point and connector identities separately. Connector `0` has charge point level meaning in several operations; do not model it as a physical charging outlet.
- `BootNotification` acceptance controls normal operation and heartbeat interval. Check the actual response status and timing before treating a connected socket as provisioned.
- Reconstruct a transaction from `Authorize` when used, `StartTransaction`, `MeterValues`, and `StopTransaction`, with `StatusNotification` as separate connector evidence. A status such as `Charging` does not prove billable energy.
- In 1.6 the CSMS returns the transaction ID in `StartTransaction` response. Preserve a station-side provisional correlation until that response arrives; offline/replayed messages need careful reconciliation.
- For remote start, correlate `RemoteStartTransaction` response with later `StartTransaction`; for remote stop, correlate `RemoteStopTransaction` with `StopTransaction`. An `Accepted` response is intent to attempt, not completion.
- Treat `GetConfiguration`/`ChangeConfiguration`, local authorization lists, firmware, diagnostics, reservation, and smart charging as feature/profile dependent. Check station support and keys before using them.
- Smart charging profiles need scope, purpose, stack level, validity, schedule units, and cleanup rules; test conflicting profiles and station reboot behavior.

## Debugging and security traps

- Confirm whether an apparent missing transaction is a delayed or repeated `StartTransaction`/`StopTransaction`, a reset, an offline buffer upload, or an ID mapping bug.
- Do not use a connector ID as a globally unique session identity; combine station identity and transaction context.
- Validate meter sample measurand, unit, context, location, phase, and timestamp before energy aggregation. Separate sampled values from signed or certified meter evidence where required.
- OCPP 1.6 core predates later security enhancements. Determine whether the station implements the OCA 1.6 security extension and which security profile is configured. Require a deployment security policy for TLS, authentication, credential/certificate rotation, and firmware integrity; never infer these protections from `ocpp1.6` alone.

Official version overview: <https://openchargealliance.org/protocols/open-charge-point-protocol/>.
