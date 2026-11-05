# OCPP 1.6: ClearChargingProfile

Direction: **Central System → Charge Point**. CALL action: `ClearChargingProfile`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `id` | no | `integer` |  |
| `connectorId` | no | `integer` |  |
| `chargingProfilePurpose` | no | `string` | values: ChargePointMaxProfile, TxDefaultProfile, TxProfile |
| `stackLevel` | no | `integer` |  |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Unknown |

Unknown object fields are rejected by this schema.
