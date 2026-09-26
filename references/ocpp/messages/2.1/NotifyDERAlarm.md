# OCPP 2.1: NotifyDERAlarm

Direction: **Charging Station → CSMS**. CALL action: `NotifyDERAlarm`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `controlType` | yes | `DERControlEnumType` |  |
| `gridEventFault` | no | `GridEventFaultEnumType` |  |
| `alarmEnded` | no | `boolean` |  |
| `timestamp` | yes | `string` | format=date-time |
| `extraInfo` | no | `string` | maxLength=200 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `DERControlEnumType`

Allowed values: `EnterService`, `FreqDroop`, `FreqWatt`, `FixedPFAbsorb`, `FixedPFInject`, `FixedVar`, `Gradients`, `HFMustTrip`, `HFMayTrip`, `HVMustTrip`, `HVMomCess`, `HVMayTrip`, `LimitMaxDischarge`, `LFMustTrip`, `LVMustTrip`, `LVMomCess`, `LVMayTrip`, `PowerMonitoringMustTrip`, `VoltVar`, `VoltWatt`, `WattPF`, `WattVar`

#### `GridEventFaultEnumType`

Allowed values: `CurrentImbalance`, `LocalEmergency`, `LowInputPower`, `OverCurrent`, `OverFrequency`, `OverVoltage`, `PhaseRotation`, `RemoteEmergency`, `UnderFrequency`, `UnderVoltage`, `VoltageImbalance`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |
