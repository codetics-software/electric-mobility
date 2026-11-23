# OCPP 2.1: SetVariableMonitoring

Direction: **CSMS → Charging Station**. CALL action: `SetVariableMonitoring`.

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
