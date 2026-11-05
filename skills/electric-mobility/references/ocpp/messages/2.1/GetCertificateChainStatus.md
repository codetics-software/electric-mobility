# OCPP 2.1: GetCertificateChainStatus

Direction: **Charging Station → CSMS**. CALL action: `GetCertificateChainStatus`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `certificateStatusRequests` | yes | `CertificateStatusRequestInfoType[]` | minItems=1; maxItems=4 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CertificateHashDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `hashAlgorithm` | yes | `HashAlgorithmEnumType` |  |
| `issuerNameHash` | yes | `string` | maxLength=128 |
| `issuerKeyHash` | yes | `string` | maxLength=128 |
| `serialNumber` | yes | `string` | maxLength=40 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CertificateStatusRequestInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `certificateHashData` | yes | `CertificateHashDataType` |  |
| `source` | yes | `CertificateStatusSourceEnumType` |  |
| `urls` | yes | `string[]` | minItems=1; maxItems=5 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CertificateStatusSourceEnumType`

Allowed values: `CRL`, `OCSP`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `HashAlgorithmEnumType`

Allowed values: `SHA256`, `SHA384`, `SHA512`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `certificateStatus` | yes | `CertificateStatusType[]` | minItems=1; maxItems=4 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CertificateHashDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `hashAlgorithm` | yes | `HashAlgorithmEnumType` |  |
| `issuerNameHash` | yes | `string` | maxLength=128 |
| `issuerKeyHash` | yes | `string` | maxLength=128 |
| `serialNumber` | yes | `string` | maxLength=40 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CertificateStatusEnumType`

Allowed values: `Good`, `Revoked`, `Unknown`, `Failed`

#### `CertificateStatusSourceEnumType`

Allowed values: `CRL`, `OCSP`

#### `CertificateStatusType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `certificateHashData` | yes | `CertificateHashDataType` |  |
| `source` | yes | `CertificateStatusSourceEnumType` |  |
| `status` | yes | `CertificateStatusEnumType` |  |
| `nextUpdate` | yes | `string` | format=date-time |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `HashAlgorithmEnumType`

Allowed values: `SHA256`, `SHA384`, `SHA512`
