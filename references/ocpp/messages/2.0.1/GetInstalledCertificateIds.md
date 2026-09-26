# OCPP 2.0.1: GetInstalledCertificateIds

Direction: **CSMS → Charging Station**. CALL action: `GetInstalledCertificateIds`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

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
