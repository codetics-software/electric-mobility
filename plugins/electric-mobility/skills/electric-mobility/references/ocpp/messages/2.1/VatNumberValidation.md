# OCPP 2.1: VatNumberValidation

Direction: **Charging Station → CSMS**. CALL action: `VatNumberValidation`.

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
