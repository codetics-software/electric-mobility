# OCPP 2.1: FirmwareStatusNotification

Direction: **Charging Station → CSMS**. CALL action: `FirmwareStatusNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `FirmwareStatusEnumType` |  |
| `requestId` | no | `integer` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `FirmwareStatusEnumType`

Allowed values: `Downloaded`, `DownloadFailed`, `Downloading`, `DownloadScheduled`, `DownloadPaused`, `Idle`, `InstallationFailed`, `Installing`, `Installed`, `InstallRebooting`, `InstallScheduled`, `InstallVerificationFailed`, `InvalidSignature`, `SignatureVerified`

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
