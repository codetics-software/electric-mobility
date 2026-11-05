# OCPP 2.0.1: GetInstalledCertificateIds

Direction: **CSMS → Charging Station**. CALL action: `GetInstalledCertificateIds`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `certificateType` | no | `GetCertificateIdUseEnumType[]` | minItems=1 |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `GetCertificateIdUseEnumType`

Allowed values: `V2GRootCertificate`, `MORootCertificate`, `CSMSRootCertificate`, `V2GCertificateChain`, `ManufacturerRootCertificate`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `GetInstalledCertificateStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `certificateHashDataChain` | no | `CertificateHashDataChainType[]` | minItems=1 |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CertificateHashDataChainType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `certificateHashData` | yes | `CertificateHashDataType` |  |
| `certificateType` | yes | `GetCertificateIdUseEnumType` |  |
| `childCertificateHashData` | no | `CertificateHashDataType[]` | minItems=1; maxItems=4 |

Unknown fields are rejected in this object.

#### `CertificateHashDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `hashAlgorithm` | yes | `HashAlgorithmEnumType` |  |
| `issuerNameHash` | yes | `string` | maxLength=128 |
| `issuerKeyHash` | yes | `string` | maxLength=128 |
| `serialNumber` | yes | `string` | maxLength=40 |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `GetCertificateIdUseEnumType`

Allowed values: `V2GRootCertificate`, `MORootCertificate`, `CSMSRootCertificate`, `V2GCertificateChain`, `ManufacturerRootCertificate`

#### `GetInstalledCertificateStatusEnumType`

Allowed values: `Accepted`, `NotFound`

#### `HashAlgorithmEnumType`

Allowed values: `SHA256`, `SHA384`, `SHA512`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
