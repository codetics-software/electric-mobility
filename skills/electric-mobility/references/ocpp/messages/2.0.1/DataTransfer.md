# OCPP 2.0.1: DataTransfer

Direction: **either peer**. CALL action: `DataTransfer`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `messageId` | no | `string` | maxLength=50 |
| `data` | no | `unknown` |  |
| `vendorId` | yes | `string` | maxLength=255 |

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
| `status` | yes | `DataTransferStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `data` | no | `unknown` |  |

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
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
