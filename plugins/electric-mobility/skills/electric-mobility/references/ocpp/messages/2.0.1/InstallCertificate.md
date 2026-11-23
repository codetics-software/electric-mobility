# OCPP 2.0.1: InstallCertificate

Direction: **CSMS → Charging Station**. CALL action: `InstallCertificate`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `certificateType` | yes | `InstallCertificateUseEnumType` |  |
| `certificate` | yes | `string` | maxLength=5500 |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `InstallCertificateUseEnumType`

Allowed values: `V2GRootCertificate`, `MORootCertificate`, `CSMSRootCertificate`, `ManufacturerRootCertificate`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `InstallCertificateStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `InstallCertificateStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `Failed`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
