# OCPP 2.0.1: FirmwareStatusNotification

Direction: **Charging Station → CSMS**. CALL action: `FirmwareStatusNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `FirmwareStatusEnumType` |  |
| `requestId` | no | `integer` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `FirmwareStatusEnumType`

Allowed values: `Downloaded`, `DownloadFailed`, `Downloading`, `DownloadScheduled`, `DownloadPaused`, `Idle`, `InstallationFailed`, `Installing`, `Installed`, `InstallRebooting`, `InstallScheduled`, `InstallVerificationFailed`, `InvalidSignature`, `SignatureVerified`


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
