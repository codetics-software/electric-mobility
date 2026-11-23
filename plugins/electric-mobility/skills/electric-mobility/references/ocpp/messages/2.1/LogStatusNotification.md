# OCPP 2.1: LogStatusNotification

Direction: **Charging Station → CSMS**. CALL action: `LogStatusNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `UploadLogStatusEnumType` |  |
| `requestId` | no | `integer` |  |
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

#### `UploadLogStatusEnumType`

Allowed values: `BadMessage`, `Idle`, `NotSupportedOperation`, `PermissionDenied`, `Uploaded`, `UploadFailure`, `Uploading`, `AcceptedCanceled`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |
