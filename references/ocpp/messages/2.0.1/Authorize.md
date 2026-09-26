# OCPP 2.0.1: Authorize

Direction: **Charging Station → CSMS**. CALL action: `Authorize`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `idToken` | yes | `IdTokenType` |  |
| `certificate` | no | `string` | maxLength=5500 |
| `iso15118CertificateHashData` | no | `OCSPRequestDataType[]` | minItems=1; maxItems=4 |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AdditionalInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `additionalIdToken` | yes | `string` | maxLength=36 |
| `type` | yes | `string` | maxLength=50 |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `HashAlgorithmEnumType`

Allowed values: `SHA256`, `SHA384`, `SHA512`

#### `IdTokenEnumType`

Allowed values: `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization`

#### `IdTokenType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `additionalInfo` | no | `AdditionalInfoType[]` | minItems=1 |
| `idToken` | yes | `string` | maxLength=36 |
| `type` | yes | `IdTokenEnumType` |  |

Unknown fields are rejected in this object.

#### `OCSPRequestDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `hashAlgorithm` | yes | `HashAlgorithmEnumType` |  |
| `issuerNameHash` | yes | `string` | maxLength=128 |
| `issuerKeyHash` | yes | `string` | maxLength=128 |
| `serialNumber` | yes | `string` | maxLength=40 |
| `responderURL` | yes | `string` | maxLength=512 |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `idTokenInfo` | yes | `IdTokenInfoType` |  |
| `certificateStatus` | no | `AuthorizeCertificateStatusEnumType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AdditionalInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `additionalIdToken` | yes | `string` | maxLength=36 |
| `type` | yes | `string` | maxLength=50 |

Unknown fields are rejected in this object.

#### `AuthorizationStatusEnumType`

Allowed values: `Accepted`, `Blocked`, `ConcurrentTx`, `Expired`, `Invalid`, `NoCredit`, `NotAllowedTypeEVSE`, `NotAtThisLocation`, `NotAtThisTime`, `Unknown`

#### `AuthorizeCertificateStatusEnumType`

Allowed values: `Accepted`, `SignatureError`, `CertificateExpired`, `CertificateRevoked`, `NoCertificateAvailable`, `CertChainError`, `ContractCancelled`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `IdTokenEnumType`

Allowed values: `Central`, `eMAID`, `ISO14443`, `ISO15693`, `KeyCode`, `Local`, `MacAddress`, `NoAuthorization`

#### `IdTokenInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `AuthorizationStatusEnumType` |  |
| `cacheExpiryDateTime` | no | `string` | format=date-time |
| `chargingPriority` | no | `integer` |  |
| `language1` | no | `string` | maxLength=8 |
| `evseId` | no | `integer[]` | minItems=1 |
| `groupIdToken` | no | `IdTokenType` |  |
| `language2` | no | `string` | maxLength=8 |
| `personalMessage` | no | `MessageContentType` |  |

Unknown fields are rejected in this object.

#### `IdTokenType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `additionalInfo` | no | `AdditionalInfoType[]` | minItems=1 |
| `idToken` | yes | `string` | maxLength=36 |
| `type` | yes | `IdTokenEnumType` |  |

Unknown fields are rejected in this object.

#### `MessageContentType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `format` | yes | `MessageFormatEnumType` |  |
| `language` | no | `string` | maxLength=8 |
| `content` | yes | `string` | maxLength=512 |

Unknown fields are rejected in this object.

#### `MessageFormatEnumType`

Allowed values: `ASCII`, `HTML`, `URI`, `UTF8`
