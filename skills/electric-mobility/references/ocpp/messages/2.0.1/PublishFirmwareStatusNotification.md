# OCPP 2.0.1: PublishFirmwareStatusNotification

Direction: **Local Controller → CSMS**. CALL action: `PublishFirmwareStatusNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `PublishFirmwareStatusEnumType` |  |
| `location` | no | `string[]` | minItems=1 |
| `requestId` | no | `integer` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `PublishFirmwareStatusEnumType`

Allowed values: `Idle`, `DownloadScheduled`, `Downloading`, `Downloaded`, `Published`, `DownloadFailed`, `DownloadPaused`, `InvalidChecksum`, `ChecksumVerified`, `PublishFailed`


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
