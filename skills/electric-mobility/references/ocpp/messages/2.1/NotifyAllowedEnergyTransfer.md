# OCPP 2.1: NotifyAllowedEnergyTransfer

Direction: **Charging Station → CSMS**. CALL action: `NotifyAllowedEnergyTransfer`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `transactionId` | yes | `string` | maxLength=36 |
| `allowedEnergyTransfer` | yes | `EnergyTransferModeEnumType[]` | minItems=1 |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `EnergyTransferModeEnumType`

Allowed values: `AC_single_phase`, `AC_two_phase`, `AC_three_phase`, `DC`, `AC_BPT`, `AC_BPT_DER`, `AC_DER`, `DC_BPT`, `DC_ACDP`, `DC_ACDP_BPT`, `WPT`


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `NotifyAllowedEnergyTransferStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `NotifyAllowedEnergyTransferStatusEnumType`

Allowed values: `Accepted`, `Rejected`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
