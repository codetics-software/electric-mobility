# OCPP 2.0.1: GetCompositeSchedule

Direction: **CSMS → Charging Station**. CALL action: `GetCompositeSchedule`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `duration` | yes | `integer` |  |
| `chargingRateUnit` | no | `ChargingRateUnitEnumType` |  |
| `evseId` | yes | `integer` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ChargingRateUnitEnumType`

Allowed values: `W`, `A`

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `status` | yes | `GenericStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `schedule` | no | `CompositeScheduleType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `ChargingRateUnitEnumType`

Allowed values: `W`, `A`

#### `ChargingSchedulePeriodType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `startPeriod` | yes | `integer` |  |
| `limit` | yes | `number` |  |
| `numberPhases` | no | `integer` |  |
| `phaseToUse` | no | `integer` |  |

Unknown fields are rejected in this object.

#### `CompositeScheduleType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `customData` | no | `CustomDataType` |  |
| `chargingSchedulePeriod` | yes | `ChargingSchedulePeriodType[]` | minItems=1 |
| `evseId` | yes | `integer` |  |
| `duration` | yes | `integer` |  |
| `scheduleStart` | yes | `string` | format=date-time |
| `chargingRateUnit` | yes | `ChargingRateUnitEnumType` |  |

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
| `customData` | no | `CustomDataType` |  |
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=512 |

Unknown fields are rejected in this object.
