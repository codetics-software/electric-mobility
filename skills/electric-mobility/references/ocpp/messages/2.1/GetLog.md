# OCPP 2.1: GetLog

Direction: **CSMS → Charging Station**. CALL action: `GetLog`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `log` | yes | `LogParametersType` |  |
| `logType` | yes | `LogEnumType` |  |
| `requestId` | yes | `integer` |  |
| `retries` | no | `integer` | minimum=0.0 |
| `retryInterval` | no | `integer` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `LogEnumType`

Allowed values: `DiagnosticsLog`, `SecurityLog`, `DataCollectorLog`

#### `LogParametersType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `remoteLocation` | yes | `string` | maxLength=2000 |
| `oldestTimestamp` | no | `string` | format=date-time |
| `latestTimestamp` | no | `string` | format=date-time |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `LogStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `filename` | no | `string` | maxLength=255 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `LogStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `AcceptedCanceled`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
