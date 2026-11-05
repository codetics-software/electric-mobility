# OCPP 2.0.1: ReserveNow

Direction: **CSMS → Charging Station**. CALL action: `ReserveNow`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `id` | yes | `integer` |  |
| `expiryDateTime` | yes | `string` | format=date-time |
| `connectorType` | no | `ConnectorEnumType` |  |
| `idToken` | yes | `IdTokenType` |  |
| `evseId` | no | `integer` |  |
| `groupIdToken` | no | `IdTokenType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AdditionalInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `additionalIdToken` | yes | `string` | maxLength=36 |
| `type` | yes | `string` | maxLength=50 |

Unknown fields are rejected in this object.

#### `ConnectorEnumType`

Allowed values: `cCCS1`, `cCCS2`, `cG105`, `cTesla`, `cType1`, `cType2`, `s309-1P-16A`, `s309-1P-32A`, `s309-3P-16A`, `s309-3P-32A`, `sBS1361`, `sCEE-7-7`, `sType2`, `sType3`, `Other1PhMax16A`, `Other1PhOver16A`, `Other3Ph`, `Pan`, `wInductive`, `wResonant`, `Undetermined`, `Unknown`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

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


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `ReserveNowStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `ReserveNowStatusEnumType`

Allowed values: `Accepted`, `Faulted`, `Occupied`, `Rejected`, `Unavailable`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
