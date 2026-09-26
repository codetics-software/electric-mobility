# OCPP 2.0.1: UpdateFirmware

Direction: **CSMS → Charging Station**. CALL action: `UpdateFirmware`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `retries` | no | `integer` |  |
| `retryInterval` | no | `integer` |  |
| `requestId` | yes | `integer` |  |
| `firmware` | yes | `FirmwareType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `FirmwareType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `location` | yes | `string` | maxLength=512 |
| `retrieveDateTime` | yes | `string` | format=date-time |
| `installDateTime` | no | `string` | format=date-time |
| `signingCertificate` | no | `string` | maxLength=5500 |
| `signature` | no | `string` | maxLength=800 |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `UpdateFirmwareStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

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

#### `UpdateFirmwareStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `AcceptedCanceled`, `InvalidCertificate`, `RevokedCertificate`
