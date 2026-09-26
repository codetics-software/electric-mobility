# OCPP 2.1: GetCompositeSchedule

Direction: **CSMS → Charging Station**. CALL action: `GetCompositeSchedule`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `duration` | yes | `integer` |  |
| `chargingRateUnit` | no | `ChargingRateUnitEnumType` |  |
| `evseId` | yes | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ChargingRateUnitEnumType`

Allowed values: `W`, `A`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `GenericStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `schedule` | no | `CompositeScheduleType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ChargingRateUnitEnumType`

Allowed values: `W`, `A`

#### `ChargingSchedulePeriodType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `startPeriod` | yes | `integer` |  |
| `limit` | no | `number` |  |
| `limit_L2` | no | `number` |  |
| `limit_L3` | no | `number` |  |
| `numberPhases` | no | `integer` | minimum=0.0; maximum=3.0 |
| `phaseToUse` | no | `integer` | minimum=0.0; maximum=3.0 |
| `dischargeLimit` | no | `number` | maximum=0.0 |
| `dischargeLimit_L2` | no | `number` | maximum=0.0 |
| `dischargeLimit_L3` | no | `number` | maximum=0.0 |
| `setpoint` | no | `number` |  |
| `setpoint_L2` | no | `number` |  |
| `setpoint_L3` | no | `number` |  |
| `setpointReactive` | no | `number` |  |
| `setpointReactive_L2` | no | `number` |  |
| `setpointReactive_L3` | no | `number` |  |
| `preconditioningRequest` | no | `boolean` |  |
| `evseSleep` | no | `boolean` |  |
| `v2xBaseline` | no | `number` |  |
| `operationMode` | no | `OperationModeEnumType` |  |
| `v2xFreqWattCurve` | no | `V2XFreqWattPointType[]` | minItems=1; maxItems=20 |
| `v2xSignalWattCurve` | no | `V2XSignalWattPointType[]` | minItems=1; maxItems=20 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CompositeScheduleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evseId` | yes | `integer` | minimum=0.0 |
| `duration` | yes | `integer` |  |
| `scheduleStart` | yes | `string` | format=date-time |
| `chargingRateUnit` | yes | `ChargingRateUnitEnumType` |  |
| `chargingSchedulePeriod` | yes | `ChargingSchedulePeriodType[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `GenericStatusEnumType`

Allowed values: `Accepted`, `Rejected`

#### `OperationModeEnumType`

Allowed values: `Idle`, `ChargingOnly`, `CentralSetpoint`, `ExternalSetpoint`, `ExternalLimits`, `CentralFrequency`, `LocalFrequency`, `LocalLoadBalancing`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `V2XFreqWattPointType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `frequency` | yes | `number` |  |
| `power` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `V2XSignalWattPointType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `signal` | yes | `integer` |  |
| `power` | yes | `number` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
