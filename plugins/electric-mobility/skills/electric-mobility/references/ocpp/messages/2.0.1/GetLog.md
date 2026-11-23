# OCPP 2.0.1: GetLog

Direction: **CSMS → Charging Station**. CALL action: `GetLog`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `log` | yes | `LogParametersType` |  |
| `logType` | yes | `LogEnumType` |  |
| `requestId` | yes | `integer` |  |
| `retries` | no | `integer` |  |
| `retryInterval` | no | `integer` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `LogEnumType`

Allowed values: `DiagnosticsLog`, `SecurityLog`

#### `LogParametersType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `remoteLocation` | yes | `string` | maxLength=512 |
| `oldestTimestamp` | no | `string` | format=date-time |
| `latestTimestamp` | no | `string` | format=date-time |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `LogStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `filename` | no | `string` | maxLength=255 |

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
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
