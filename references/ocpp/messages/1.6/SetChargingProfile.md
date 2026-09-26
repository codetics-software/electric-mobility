# OCPP 1.6: SetChargingProfile

Direction: **Central System → Charge Point**. CALL action: `SetChargingProfile`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA OCPP-J JSON schema set. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `connectorId` | yes | `integer` |  |
| `csChargingProfiles` | yes | `object` |  |

Unknown object fields are rejected by this schema.

### `csChargingProfiles` object

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

### `csChargingProfiles.chargingSchedule` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `duration` | no | `integer` |  |
| `startSchedule` | no | `string` | format=date-time |
| `chargingRateUnit` | yes | `string` | values: A, W |
| `chargingSchedulePeriod` | yes | `object[]` |  |
| `minChargingRate` | no | `number` |  |

Unknown fields are rejected in this object.

### `csChargingProfiles.chargingSchedule.chargingSchedulePeriod` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `startPeriod` | yes | `integer` |  |
| `limit` | yes | `number` |  |
| `numberPhases` | no | `integer` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Rejected, NotSupported |

Unknown object fields are rejected by this schema.
