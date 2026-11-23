# OCPP 2.1: SignCertificate

Direction: **Charging Station → CSMS**. CALL action: `SignCertificate`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `csr` | yes | `string` | maxLength=5500 |
| `certificateType` | no | `CertificateSigningUseEnumType` |  |
| `hashRootCertificate` | no | `CertificateHashDataType` |  |
| `requestId` | no | `integer` |  |
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

#### `CertificateSigningUseEnumType`

Allowed values: `ChargingStationCertificate`, `V2GCertificate`, `V2G20Certificate`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `HashAlgorithmEnumType`

Allowed values: `SHA256`, `SHA384`, `SHA512`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `GenericStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `GenericStatusEnumType`

Allowed values: `Accepted`, `Rejected`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
