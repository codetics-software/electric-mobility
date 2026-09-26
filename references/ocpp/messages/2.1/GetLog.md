# OCPP 2.1: GetLog

Direction: **CSMS → Charging Station**. CALL action: `GetLog`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

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
