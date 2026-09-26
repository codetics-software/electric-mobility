# OCPP 2.1 engineering guide

Use this guide with the [2.1 JSON message cards](messages/2.1/) and [WebSocket runtime](websocket-and-runtime.md). The cards contain fields from the OCA Part 3 schema package; no PDF is needed for routine implementation. The inspected schema ZIP is dated January 2025 while OCA edition 2 prose is December 2025, with June 2026 errata. Check a relevant correction and artifact revision before claiming exact edition 2 conformance. Optional Device Model appendices may change independently.

Read the [June 2026 errata digest](errata-2026-06.md) before implementing DER control, remote start, periodic streams, reset, firmware, or transaction retry behavior. Its DER corrections can override permissive schema fields and enums.

## Added capability areas

The OCA edition 2 introduction names ISO 15118-20, bidirectional power transfer, DER control, ad hoc payment, local cost calculation, prepaid authorization, transaction limits, and forced-reboot transaction resume. The schema archive includes action families such as `AFRRSignal`, `BatterySwap`, `ChangeTransactionTariff`, and DER control. These are capability areas, not mandatory features on every 2.1 station.

- Extend 2.0.1 transaction handling for limits on cost, energy, time, or state of charge and for resume after forced reboot. Keep one logical transaction identity and explicitly reconcile gaps, duplicated events, and new connection epochs.
- For V2X and DER, represent import and export directions explicitly. Do not silently net energy when tariffs, settlement, metering, or grid obligations require separate directions.
- For ISO 15118-20, verify certificate, authorization, and EV communication capabilities end to end. OCPP support in the CSMS does not prove the station or EV supports the complete flow.
- For tariffs, local cost, ad hoc payment, or prepaid balance, distinguish displayed estimates, station-calculated cost, payment authorization, and final settlement. Reject stale tariff versions and record the tariff snapshot used for a transaction.
- For battery swapping, model the swap operation as its own operational and financial lifecycle; do not force it into connector energy delivery assumptions.
- OCPP 2.1 introduces an unconfirmed SEND message type for frequent monitoring event streams. Treat its delivery, backpressure, and gap detection differently from a request/response CALL.
- Edition 2 extends authorization token length/type handling and clarifies authorization-cache expiry. Audit any 2.0.1 DTO or database field length before accepting 2.1 tokens.
- Gate each new action on negotiated version, implementation capability, security requirements, and a tested business use case. Use the matching schema and Part 2 requirements for exact fields.

## Debugging and security traps

- Identify whether the failure is protocol negotiation, unsupported functional block, schema mismatch, station state, grid/DER control, authorization, or payment integration before retrying.
- Protect tariff changes, DER commands, transaction limits, and payment-related flows with role checks, audit trails, and replay/duplicate handling. Keep payment card data out of OCPP logs and ordinary domain events.
- Test 2.0.1 coexistence explicitly. Shared application logic is useful, but 2.1-only messages must not be emitted to a 2.0.1 station.

Official version overview: <https://openchargealliance.org/protocols/open-charge-point-protocol/>.
