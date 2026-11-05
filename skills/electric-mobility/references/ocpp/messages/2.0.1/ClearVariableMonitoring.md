# OCPP 2.0.1: ClearVariableMonitoring

Direction: **CSMS → Charging Station**. CALL action: `ClearVariableMonitoring`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `id` | yes | `integer[]` | minItems=1 |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `clearMonitoringResult` | yes | `ClearMonitoringResultType[]` | minItems=1 |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ClearMonitoringResultType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `ClearMonitoringStatusEnumType` |  |
| `id` | yes | `integer` |  |
| `statusInfo` | no | `StatusInfoType` |  |

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
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
