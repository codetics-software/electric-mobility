# OCPP 2.1: PublishFirmwareStatusNotification

Direction: **Local Controller → CSMS**. CALL action: `PublishFirmwareStatusNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `PublishFirmwareStatusEnumType` |  |
| `location` | no | `string[]` | minItems=1 |
| `requestId` | no | `integer` | minimum=0.0 |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `PublishFirmwareStatusEnumType`

Allowed values: `Idle`, `DownloadScheduled`, `Downloading`, `Downloaded`, `Published`, `DownloadFailed`, `DownloadPaused`, `InvalidChecksum`, `ChecksumVerified`, `PublishFailed`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


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
