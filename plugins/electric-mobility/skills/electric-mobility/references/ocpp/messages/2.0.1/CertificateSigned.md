# OCPP 2.0.1: CertificateSigned

Direction: **CSMS → Charging Station**. CALL action: `CertificateSigned`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `certificateChain` | yes | `string` | maxLength=10000 |
| `certificateType` | no | `CertificateSigningUseEnumType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CertificateSigningUseEnumType`

Allowed values: `ChargingStationCertificate`, `V2GCertificate`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `CertificateSignedStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CertificateSignedStatusEnumType`

Allowed values: `Accepted`, `Rejected`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
