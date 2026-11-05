# OCPP 2.1: GetInstalledCertificateIds

Direction: **CSMS → Charging Station**. CALL action: `GetInstalledCertificateIds`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `certificateType` | no | `GetCertificateIdUseEnumType[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `GetCertificateIdUseEnumType`

Allowed values: `V2GRootCertificate`, `MORootCertificate`, `CSMSRootCertificate`, `V2GCertificateChain`, `ManufacturerRootCertificate`, `OEMRootCertificate`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `GetInstalledCertificateStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `certificateHashDataChain` | no | `CertificateHashDataChainType[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CertificateHashDataChainType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `certificateHashData` | yes | `CertificateHashDataType` |  |
| `certificateType` | yes | `GetCertificateIdUseEnumType` |  |
| `childCertificateHashData` | no | `CertificateHashDataType[]` | minItems=1; maxItems=4 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CertificateHashDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `hashAlgorithm` | yes | `HashAlgorithmEnumType` |  |
| `issuerNameHash` | yes | `string` | maxLength=128 |
| `issuerKeyHash` | yes | `string` | maxLength=128 |
| `serialNumber` | yes | `string` | maxLength=40 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `GetCertificateIdUseEnumType`

Allowed values: `V2GRootCertificate`, `MORootCertificate`, `CSMSRootCertificate`, `V2GCertificateChain`, `ManufacturerRootCertificate`, `OEMRootCertificate`

#### `GetInstalledCertificateStatusEnumType`

Allowed values: `Accepted`, `NotFound`

#### `HashAlgorithmEnumType`

Allowed values: `SHA256`, `SHA384`, `SHA512`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
