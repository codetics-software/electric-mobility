# OCPP 2.1: NotifySettlement

Direction: **Charging Station → CSMS**. CALL action: `NotifySettlement`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `transactionId` | no | `string` | maxLength=36 |
| `pspRef` | yes | `string` | maxLength=255 |
| `status` | yes | `PaymentStatusEnumType` |  |
| `statusInfo` | no | `string` | maxLength=500 |
| `settlementAmount` | yes | `number` |  |
| `settlementTime` | yes | `string` | format=date-time |
| `receiptId` | no | `string` | maxLength=50 |
| `receiptUrl` | no | `string` | maxLength=2000 |
| `vatCompany` | no | `AddressType` |  |
| `vatNumber` | no | `string` | maxLength=20 |
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

#### `PaymentStatusEnumType`

Allowed values: `Settled`, `Canceled`, `Rejected`, `Failed`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `receiptUrl` | no | `string` | maxLength=2000 |
| `receiptId` | no | `string` | maxLength=50 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |
