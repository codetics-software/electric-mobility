# OCPP 2.1: SetDERControl

Direction: **CSMS → Charging Station**. CALL action: `SetDERControl`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `isDefault` | yes | `boolean` |  |
| `controlId` | yes | `string` | maxLength=36 |
| `controlType` | yes | `DERControlEnumType` |  |
| `curve` | no | `DERCurveType` |  |
| `enterService` | no | `EnterServiceType` |  |
| `fixedPFAbsorb` | no | `FixedPFType` |  |
| `fixedPFInject` | no | `FixedPFType` |  |
| `fixedVar` | no | `FixedVarType` |  |
| `freqDroop` | no | `FreqDroopType` |  |
| `gradient` | no | `GradientType` |  |
| `limitMaxDischarge` | no | `LimitMaxDischargeType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `DERControlEnumType`

Allowed values: `EnterService`, `FreqDroop`, `FreqWatt`, `FixedPFAbsorb`, `FixedPFInject`, `FixedVar`, `Gradients`, `HFMustTrip`, `HFMayTrip`, `HVMustTrip`, `HVMomCess`, `HVMayTrip`, `LimitMaxDischarge`, `LFMustTrip`, `LVMustTrip`, `LVMomCess`, `LVMayTrip`, `PowerMonitoringMustTrip`, `VoltVar`, `VoltWatt`, `WattPF`, `WattVar`

#### `DERCurvePointsType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `x` | yes | `number` |  |
| `y` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `DERCurveType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `curveData` | yes | `DERCurvePointsType[]` | minItems=1; maxItems=10 |
| `hysteresis` | no | `HysteresisType` |  |
| `priority` | yes | `integer` | minimum=0.0 |
| `reactivePowerParams` | no | `ReactivePowerParamsType` |  |
| `voltageParams` | no | `VoltageParamsType` |  |
| `yUnit` | yes | `DERUnitEnumType` |  |
| `responseTime` | no | `number` |  |
| `startTime` | no | `string` | format=date-time |
| `duration` | no | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `DERUnitEnumType`

Allowed values: `Not_Applicable`, `PctMaxW`, `PctMaxVar`, `PctWAvail`, `PctVarAvail`, `PctEffectiveV`

#### `EnterServiceType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `priority` | yes | `integer` | minimum=0.0 |
| `highVoltage` | yes | `number` |  |
| `lowVoltage` | yes | `number` |  |
| `highFreq` | yes | `number` |  |
| `lowFreq` | yes | `number` |  |
| `delay` | no | `number` |  |
| `randomDelay` | no | `number` |  |
| `rampRate` | no | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `FixedPFType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `priority` | yes | `integer` | minimum=0.0 |
| `displacement` | yes | `number` |  |
| `excitation` | yes | `boolean` |  |
| `startTime` | no | `string` | format=date-time |
| `duration` | no | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `FixedVarType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `priority` | yes | `integer` | minimum=0.0 |
| `setpoint` | yes | `number` |  |
| `unit` | yes | `DERUnitEnumType` |  |
| `startTime` | no | `string` | format=date-time |
| `duration` | no | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `FreqDroopType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `priority` | yes | `integer` | minimum=0.0 |
| `overFreq` | yes | `number` |  |
| `underFreq` | yes | `number` |  |
| `overDroop` | yes | `number` |  |
| `underDroop` | yes | `number` |  |
| `responseTime` | yes | `number` |  |
| `startTime` | no | `string` | format=date-time |
| `duration` | no | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `GradientType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `priority` | yes | `integer` | minimum=0.0 |
| `gradient` | yes | `number` |  |
| `softGradient` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `HysteresisType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `hysteresisHigh` | no | `number` |  |
| `hysteresisLow` | no | `number` |  |
| `hysteresisDelay` | no | `number` |  |
| `hysteresisGradient` | no | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `LimitMaxDischargeType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `priority` | yes | `integer` | minimum=0.0 |
| `pctMaxDischargePower` | no | `number` |  |
| `powerMonitoringMustTrip` | no | `DERCurveType` |  |
| `startTime` | no | `string` | format=date-time |
| `duration` | no | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `PowerDuringCessationEnumType`

Allowed values: `Active`, `Reactive`

#### `ReactivePowerParamsType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vRef` | no | `number` |  |
| `autonomousVRefEnable` | no | `boolean` |  |
| `autonomousVRefTimeConstant` | no | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `VoltageParamsType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `hv10MinMeanValue` | no | `number` |  |
| `hv10MinMeanTripDelay` | no | `number` |  |
| `powerDuringCessation` | no | `PowerDuringCessationEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `DERControlStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `supersededIds` | no | `string[]` | minItems=1; maxItems=24 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `DERControlStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `NotSupported`, `NotFound`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
