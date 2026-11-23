# OCPP 2.0.1: LogStatusNotification

Direction: **Charging Station → CSMS**. CALL action: `LogStatusNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `UploadLogStatusEnumType` |  |
| `requestId` | no | `integer` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

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
