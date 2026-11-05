# OCPP 2.1: ClearVariableMonitoring

Direction: **CSMS → Charging Station**. CALL action: `ClearVariableMonitoring`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | yes | `integer[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `clearMonitoringResult` | yes | `ClearMonitoringResultType[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ClearMonitoringResultType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `ClearMonitoringStatusEnumType` |  |
| `id` | yes | `integer` | minimum=0.0 |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `ClearMonitoringStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `NotFound`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
