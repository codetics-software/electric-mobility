# OCPP 2.1: GetTariffs

Direction: **CSMS → Charging Station**. CALL action: `GetTariffs`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evseId` | yes | `integer` | minimum=0.0 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `TariffGetStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `tariffAssignments` | no | `TariffAssignmentType[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffAssignmentType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `tariffId` | yes | `string` | maxLength=60 |
| `tariffKind` | yes | `TariffKindEnumType` |  |
| `validFrom` | no | `string` | format=date-time |
| `evseIds` | no | `integer[]` | minItems=1 |
| `idTokens` | no | `string[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `TariffGetStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `NoTariff`

#### `TariffKindEnumType`

Allowed values: `DefaultTariff`, `DriverTariff`
