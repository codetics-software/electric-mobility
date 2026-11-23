# OCPP 1.6: RemoteStopTransaction

Direction: **Central System → Charge Point**. CALL action: `RemoteStopTransaction`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `transactionId` | yes | `integer` |  |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Accepted, Rejected |

Unknown object fields are rejected by this schema.
