# OCPP 2.1: InstallCertificate

Direction: **CSMS → Charging Station**. CALL action: `InstallCertificate`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `certificateType` | yes | `InstallCertificateUseEnumType` |  |
| `certificate` | yes | `string` | maxLength=10000 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `InstallCertificateUseEnumType`

Allowed values: `V2GRootCertificate`, `MORootCertificate`, `ManufacturerRootCertificate`, `CSMSRootCertificate`, `OEMRootCertificate`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `InstallCertificateStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

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
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
