# OCPP 2.0.1: UpdateFirmware

Direction: **CSMS → Charging Station**. CALL action: `UpdateFirmware`.

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
