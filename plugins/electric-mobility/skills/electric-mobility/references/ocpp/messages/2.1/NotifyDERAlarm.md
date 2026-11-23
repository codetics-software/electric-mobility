# OCPP 2.1: NotifyDERAlarm

Direction: **Charging Station → CSMS**. CALL action: `NotifyDERAlarm`.

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
