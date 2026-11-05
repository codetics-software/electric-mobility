# OCPP 1.6: GetCompositeSchedule

Direction: **Central System → Charge Point**. CALL action: `GetCompositeSchedule`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA OCPP-J JSON schema set. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `connectorId` | yes | `integer` |  |
| `duration` | yes | `integer` |  |
| `chargingRateUnit` | no | `string` | values: A, W |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Rejected |
| `connectorId` | no | `integer` |  |
| `scheduleStart` | no | `string` | format=date-time |
| `chargingSchedule` | no | `object` |  |

Unknown object fields are rejected by this schema.

### `chargingSchedule` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `duration` | no | `integer` |  |
| `startSchedule` | no | `string` | format=date-time |
| `chargingRateUnit` | yes | `string` | values: A, W |
| `chargingSchedulePeriod` | yes | `object[]` |  |
| `minChargingRate` | no | `number` |  |

Unknown fields are rejected in this object.

### `chargingSchedule.chargingSchedulePeriod` object

| Field | Required | Type | Constraints |
|---|---|---|---|
| `startPeriod` | yes | `integer` |  |
| `limit` | yes | `number` |  |
| `numberPhases` | no | `integer` |  |

Unknown fields are rejected in this object.
