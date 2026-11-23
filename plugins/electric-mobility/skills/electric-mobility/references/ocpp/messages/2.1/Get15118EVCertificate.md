# OCPP 2.1: Get15118EVCertificate

Direction: **Charging Station → CSMS**. CALL action: `Get15118EVCertificate`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `iso15118SchemaVersion` | yes | `string` | maxLength=50 |
| `action` | yes | `CertificateActionEnumType` |  |
| `exiRequest` | yes | `string` | maxLength=11000 |
| `maximumContractCertificateChains` | no | `integer` | minimum=0.0 |
| `prioritizedEMAIDs` | no | `string[]` | minItems=1; maxItems=8 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CertificateActionEnumType`

Allowed values: `Install`, `Update`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `Iso15118EVCertificateStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `exiResponse` | yes | `string` | maxLength=17000 |
| `remainingContracts` | no | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `Iso15118EVCertificateStatusEnumType`

Allowed values: `Accepted`, `Failed`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
