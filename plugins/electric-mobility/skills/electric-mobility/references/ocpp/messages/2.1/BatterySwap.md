# OCPP 2.1: BatterySwap

Direction: **Charging Station → CSMS**. CALL action: `BatterySwap`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `batteryData` | yes | `BatteryDataType[]` | minItems=1 |
| `eventType` | yes | `BatterySwapEventEnumType` |  |
| `idToken` | yes | `IdTokenType` |  |
| `requestId` | yes | `integer` |  |
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

#### `BatteryDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `evseId` | yes | `integer` | minimum=0.0 |
| `serialNumber` | yes | `string` | maxLength=50 |
| `soC` | yes | `number` | minimum=0.0; maximum=100.0 |
| `soH` | yes | `number` | minimum=0.0; maximum=100.0 |
| `productionDate` | no | `string` | format=date-time |
| `vendorInfo` | no | `string` | maxLength=500 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `BatterySwapEventEnumType`

Allowed values: `BatteryIn`, `BatteryOut`, `BatteryOutTimeout`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `IdTokenType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `additionalInfo` | no | `AdditionalInfoType[]` | minItems=1 |
| `idToken` | yes | `string` | maxLength=255 |
| `type` | yes | `string` | maxLength=20 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |
