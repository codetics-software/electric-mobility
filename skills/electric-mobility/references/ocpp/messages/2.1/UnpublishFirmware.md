# OCPP 2.1: UnpublishFirmware

Direction: **CSMS → Local Controller**. CALL action: `UnpublishFirmware`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `checksum` | yes | `string` | maxLength=32 |
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
| `status` | yes | `UnpublishFirmwareStatusEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `UnpublishFirmwareStatusEnumType`

Allowed values: `DownloadOngoing`, `NoFirmware`, `Unpublished`
