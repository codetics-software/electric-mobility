# OCPP 2.1: VatNumberValidation

Direction: **Charging Station → CSMS**. CALL action: `VatNumberValidation`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vatNumber` | yes | `string` | maxLength=20 |
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
| `company` | no | `AddressType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `vatNumber` | yes | `string` | maxLength=20 |
| `evseId` | no | `integer` | minimum=0.0 |
| `status` | yes | `GenericStatusEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `AddressType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `name` | yes | `string` | maxLength=50 |
| `address1` | yes | `string` | maxLength=100 |
| `address2` | no | `string` | maxLength=100 |
| `city` | yes | `string` | maxLength=100 |
| `postalCode` | no | `string` | maxLength=20 |
| `country` | yes | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

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
