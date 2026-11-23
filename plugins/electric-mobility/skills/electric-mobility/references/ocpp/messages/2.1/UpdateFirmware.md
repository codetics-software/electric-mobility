# OCPP 2.1: UpdateFirmware

Direction: **CSMS → Charging Station**. CALL action: `UpdateFirmware`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `retries` | no | `integer` | minimum=0.0 |
| `retryInterval` | no | `integer` |  |
| `requestId` | yes | `integer` |  |
| `firmware` | yes | `FirmwareType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `FirmwareType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `location` | yes | `string` | maxLength=2000 |
| `retrieveDateTime` | yes | `string` | format=date-time |
| `installDateTime` | no | `string` | format=date-time |
| `signingCertificate` | no | `string` | maxLength=5500 |
| `signature` | no | `string` | maxLength=800 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `UpdateFirmwareStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

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

#### `UpdateFirmwareStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `AcceptedCanceled`, `InvalidCertificate`, `RevokedCertificate`
