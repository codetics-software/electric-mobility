# OCPP 2.1: SendLocalList

Direction: **CSMS → Charging Station**. CALL action: `SendLocalList`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `localAuthorizationList` | no | `AuthorizationData[]` | minItems=1 |
| `versionNumber` | yes | `integer` |  |
| `updateType` | yes | `UpdateEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AdditionalInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `additionalIdToken` | yes | `string` | maxLength=255 |
| `type` | yes | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `AuthorizationData`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `idToken` | yes | `IdTokenType` |  |
| `idTokenInfo` | no | `IdTokenInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `AuthorizationStatusEnumType`

Allowed values: `Accepted`, `Blocked`, `ConcurrentTx`, `Expired`, `Invalid`, `NoCredit`, `NotAllowedTypeEVSE`, `NotAtThisLocation`, `NotAtThisTime`, `Unknown`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `IdTokenInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `AuthorizationStatusEnumType` |  |
| `cacheExpiryDateTime` | no | `string` | format=date-time |
| `chargingPriority` | no | `integer` |  |
| `groupIdToken` | no | `IdTokenType` |  |
| `language1` | no | `string` | maxLength=8 |
| `language2` | no | `string` | maxLength=8 |
| `evseId` | no | `integer[]` | minItems=1 |
| `personalMessage` | no | `MessageContentType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `IdTokenType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `additionalInfo` | no | `AdditionalInfoType[]` | minItems=1 |
| `idToken` | yes | `string` | maxLength=255 |
| `type` | yes | `string` | maxLength=20 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `MessageContentType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `format` | yes | `MessageFormatEnumType` |  |
| `language` | no | `string` | maxLength=8 |
| `content` | yes | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `MessageFormatEnumType`

Allowed values: `ASCII`, `HTML`, `URI`, `UTF8`, `QRCODE`

#### `UpdateEnumType`

Allowed values: `Differential`, `Full`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `SendLocalListStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `SendLocalListStatusEnumType`

Allowed values: `Accepted`, `Failed`, `VersionMismatch`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
