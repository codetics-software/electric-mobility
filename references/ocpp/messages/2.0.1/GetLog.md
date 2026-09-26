# OCPP 2.0.1: GetLog

Direction: **CSMS → Charging Station**. CALL action: `GetLog`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

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
