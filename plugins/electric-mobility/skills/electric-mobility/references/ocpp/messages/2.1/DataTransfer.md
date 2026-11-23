# OCPP 2.1: DataTransfer

Direction: **either peer**. CALL action: `DataTransfer`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `messageId` | no | `string` | maxLength=50 |
| `data` | no | `unknown` |  |
| `vendorId` | yes | `string` | maxLength=255 |
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
| `status` | yes | `DataTransferStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `data` | no | `unknown` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `DataTransferStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `UnknownMessageId`, `UnknownVendorId`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
