# OCPP 2.1: ClearTariffs

Direction: **CSMS → Charging Station**. CALL action: `ClearTariffs`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `tariffIds` | no | `string[]` | minItems=1 |
| `evseId` | no | `integer` | minimum=0.0 |
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
| `clearTariffsResult` | yes | `ClearTariffsResultType[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ClearTariffsResultType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `statusInfo` | no | `StatusInfoType` |  |
| `tariffId` | no | `string` | maxLength=60 |
| `status` | yes | `TariffClearStatusEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

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

#### `TariffClearStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `NoTariff`
