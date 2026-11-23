# OCPP message coverage and generation

Use this index to select an action, then read its bundled `messages/<version>/<Action>.md` card for exact JSON field names, required fields, types, bounds, enums, and nested objects. These cards are sufficient to design DTOs and validate wire shapes without downloading a ZIP or loading a PDF. Use the version, runtime, and management guides for the use-case preconditions and response meaning. Confirm feature/profile support before enabling an action; the presence of a card does not imply mandatory support.

## OCPP 1.6: 28 distinct CALL actions

The OCA edition 2 specification lists ten operations initiated by the Charge Point and nineteen initiated by the Central System; `DataTransfer` appears in both directions, giving 28 distinct action names.

| Initiator | Action names |
|---|---|
| Charge Point → Central System | `Authorize`, `BootNotification`, `DataTransfer`, `DiagnosticsStatusNotification`, `FirmwareStatusNotification`, `Heartbeat`, `MeterValues`, `StartTransaction`, `StatusNotification`, `StopTransaction` |
| Central System → Charge Point | `CancelReservation`, `ChangeAvailability`, `ChangeConfiguration`, `ClearCache`, `ClearChargingProfile`, `DataTransfer`, `GetCompositeSchedule`, `GetConfiguration`, `GetDiagnostics`, `GetLocalListVersion`, `RemoteStartTransaction`, `RemoteStopTransaction`, `ReserveNow`, `Reset`, `SendLocalList`, `SetChargingProfile`, `TriggerMessage`, `UnlockConnector`, `UpdateFirmware` |

Implement the request and response body for each supported action from the [1.6 cards](messages/1.6/), plus CALLERROR handling. OCPP 1.6 optional feature profiles determine which Central System actions a station is expected to support. A `NotSupported` response and a transport error have different meanings. Keep vendor `DataTransfer` payloads in a bounded, isolated extension handler.

## OCPP 2.0.1: 64 request/response actions

Every name below has both request and response fields in its [2.0.1 card](messages/2.0.1/). The action on a CALL frame is `Name` without the `Request` suffix.

| Group for discovery | Actions |
|---|---|
| Provisioning, connectivity, configuration | `BootNotification`, `Heartbeat`, `Reset`, `SetNetworkProfile`, `GetVariables`, `SetVariables`, `GetBaseReport`, `GetReport`, `NotifyReport`, `DataTransfer` |
| Authorization and local lists | `Authorize`, `ClearCache`, `GetLocalListVersion`, `SendLocalList`, `CustomerInformation`, `NotifyCustomerInformation` |
| Transactions, metering, availability, remote control | `TransactionEvent`, `MeterValues`, `StatusNotification`, `ChangeAvailability`, `RequestStartTransaction`, `RequestStopTransaction`, `GetTransactionStatus`, `TriggerMessage`, `UnlockConnector`, `ReserveNow`, `CancelReservation`, `ReservationStatusUpdate` |
| Smart charging and EV communication | `SetChargingProfile`, `ClearChargingProfile`, `GetChargingProfiles`, `ReportChargingProfiles`, `GetCompositeSchedule`, `NotifyChargingLimit`, `ClearedChargingLimit`, `NotifyEVChargingNeeds`, `NotifyEVChargingSchedule`, `Get15118EVCertificate` |
| Security, certificates, firmware, diagnostics | `SecurityEventNotification`, `SignCertificate`, `CertificateSigned`, `GetCertificateStatus`, `InstallCertificate`, `DeleteCertificate`, `GetInstalledCertificateIds`, `UpdateFirmware`, `FirmwareStatusNotification`, `PublishFirmware`, `UnpublishFirmware`, `PublishFirmwareStatusNotification`, `GetLog`, `LogStatusNotification` |
| Monitoring, display, cost | `SetVariableMonitoring`, `ClearVariableMonitoring`, `GetMonitoringReport`, `NotifyMonitoringReport`, `SetMonitoringBase`, `SetMonitoringLevel`, `NotifyEvent`, `SetDisplayMessage`, `ClearDisplayMessage`, `GetDisplayMessages`, `NotifyDisplayMessages`, `CostUpdated` |

The groups are an implementation index, not official certification profile names. Confirm each action's initiator, response status, timing, and state preconditions in Part 2. Some actions report information asynchronously after a different accepted request.

## OCPP 2.1: 90 request/response actions plus SEND

The inspected 2.1 Part 3 ZIP contains all 64 names above and these 26 additional request/response actions:

An action retaining its name may still have changed fields, enum sets, or use-case meaning in 2.1. Read the matching [2.1 card](messages/2.1/) and keep the DTO versioned; do not reuse a 2.0.1 DTO merely because the action name matches.

| Capability area | New action names |
|---|---|
| DER, V2X, schedules | `AFRRSignal`, `ClearDERControl`, `GetDERControl`, `SetDERControl`, `ReportDERControl`, `NotifyDERAlarm`, `NotifyDERStartStop`, `NotifyAllowedEnergyTransfer`, `PullDynamicScheduleUpdate`, `UpdateDynamicSchedule`, `NotifyPriorityCharging`, `UsePriorityCharging` |
| Tariff, payment, settlement | `ChangeTransactionTariff`, `ClearTariffs`, `GetTariffs`, `SetDefaultTariff`, `NotifySettlement`, `NotifyWebPaymentStarted`, `VatNumberValidation` |
| Periodic monitoring streams | `AdjustPeriodicEventStream`, `ClosePeriodicEventStream`, `GetPeriodicEventStream`, `OpenPeriodicEventStream` |
| Certificates and battery swapping | `GetCertificateChainStatus`, `BatterySwap`, `RequestBatterySwap` |

The same ZIP also includes **`NotifyPeriodicEventStream.json`**, which is not a Request/Response pair. OCPP 2.1 Part 4 defines the unconfirmed SEND frame used by event streams. Implement SEND dispatch separately and never synthesize a response schema for it. OCPP 2.1 also adds CALLRESULTERROR for an invalid response payload. Read [websocket-and-runtime.md](websocket-and-runtime.md) for frame behavior.

## Build every message accurately

For each selected action, record: protocol version and source artifact; feature/profile; initiator and receiver; exact request and response schema; required/optional fields and enum handling; identifier scopes; units/time; allowed lifecycle state; synchronous result versus later event; error mapping; authorization and audit; idempotency/retry; and a valid and invalid wire fixture.

Use the included cards as the DTO input contract. Preserve the chosen protocol version and source edition in project metadata, review generated types, and validate serialized JSON at the boundary. Build a dispatcher keyed by negotiated version + action + direction, and require the matching response type for the pending CALL. An unknown or unsupported action goes through the version-specific CALLERROR path; a known action with a business rejection returns its defined response status when the specification says so.

The cards summarize the JSON schema packages. This skill also includes Part 2/Part 4 behavior in the adjacent guides. For certification or a conflicting interpretation, compare with [OCA's current editions and errata](https://openchargealliance.org/protocols/open-charge-point-protocol/). Source downloads are optional and should be targeted to the relevant disputed issue.

