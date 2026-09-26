# OCPP 1.6: RemoteStartTransaction

Direction: **Central System → Charge Point**. CALL action: `RemoteStartTransaction`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA OCPP-J JSON schema set. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `connectorId` | no | `integer` |  |
| `idTag` | yes | `string` | maxLength=20 |
| `chargingProfile` | no | `object` |  |

Unknown object fields are rejected by this schema.

### `chargingProfile` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `chargingProfileId` | yes | `integer` |  |
| `transactionId` | no | `integer` |  |
| `stackLevel` | yes | `integer` |  |
| `chargingProfilePurpose` | yes | `string` | values: ChargePointMaxProfile, TxDefaultProfile, TxProfile |
| `chargingProfileKind` | yes | `string` | values: Absolute, Recurring, Relative |
| `recurrencyKind` | no | `string` | values: Daily, Weekly |
| `validFrom` | no | `string` | format=date-time |
| `validTo` | no | `string` | format=date-time |
| `chargingSchedule` | yes | `object` |  |

Unknown fields are rejected in this object.

### `chargingProfile.chargingSchedule` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `duration` | no | `integer` |  |
| `startSchedule` | no | `string` | format=date-time |
| `chargingRateUnit` | yes | `string` | values: A, W |
| `chargingSchedulePeriod` | yes | `object[]` |  |
| `minChargingRate` | no | `number` |  |

Unknown fields are rejected in this object.

### `chargingProfile.chargingSchedule.chargingSchedulePeriod` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `startPeriod` | yes | `integer` |  |
| `limit` | yes | `number` |  |
| `numberPhases` | no | `integer` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Rejected |

Unknown object fields are rejected by this schema.
