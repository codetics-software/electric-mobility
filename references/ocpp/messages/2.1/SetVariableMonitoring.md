# OCPP 2.1: SetVariableMonitoring

Direction: **CSMS → Charging Station**. CALL action: `SetVariableMonitoring`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `setMonitoringData` | yes | `SetMonitoringDataType[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ComponentType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evse` | no | `EVSEType` |  |
| `name` | yes | `string` | maxLength=50 |
| `instance` | no | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `EVSEType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | yes | `integer` | minimum=0.0 |
| `connectorId` | no | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `MonitorEnumType`

Allowed values: `UpperThreshold`, `LowerThreshold`, `Delta`, `Periodic`, `PeriodicClockAligned`, `TargetDelta`, `TargetDeltaRelative`

#### `PeriodicEventStreamParamsType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `interval` | no | `integer` | minimum=0.0 |
| `values` | no | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `SetMonitoringDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | no | `integer` | minimum=0.0 |
| `periodicEventStream` | no | `PeriodicEventStreamParamsType` |  |
| `transaction` | no | `boolean` | default=false |
| `value` | yes | `number` |  |
| `type` | yes | `MonitorEnumType` |  |
| `severity` | yes | `integer` | minimum=0.0 |
| `component` | yes | `ComponentType` |  |
| `variable` | yes | `VariableType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `VariableType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `name` | yes | `string` | maxLength=50 |
| `instance` | no | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `setMonitoringResult` | yes | `SetMonitoringResultType[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ComponentType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evse` | no | `EVSEType` |  |
| `name` | yes | `string` | maxLength=50 |
| `instance` | no | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `EVSEType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | yes | `integer` | minimum=0.0 |
| `connectorId` | no | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `MonitorEnumType`

Allowed values: `UpperThreshold`, `LowerThreshold`, `Delta`, `Periodic`, `PeriodicClockAligned`, `TargetDelta`, `TargetDeltaRelative`

#### `SetMonitoringResultType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | no | `integer` | minimum=0.0 |
| `statusInfo` | no | `StatusInfoType` |  |
| `status` | yes | `SetMonitoringStatusEnumType` |  |
| `type` | yes | `MonitorEnumType` |  |
| `component` | yes | `ComponentType` |  |
| `variable` | yes | `VariableType` |  |
| `severity` | yes | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `SetMonitoringStatusEnumType`

Allowed values: `Accepted`, `UnknownComponent`, `UnknownVariable`, `UnsupportedMonitorType`, `Rejected`, `Duplicate`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `VariableType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `name` | yes | `string` | maxLength=50 |
| `instance` | no | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
