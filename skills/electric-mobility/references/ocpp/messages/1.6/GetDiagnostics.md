# OCPP 1.6: GetDiagnostics

Direction: **Central System → Charge Point**. CALL action: `GetDiagnostics`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `location` | yes | `string` | format=uri |
| `retries` | no | `integer` |  |
| `retryInterval` | no | `integer` |  |
| `startTime` | no | `string` | format=date-time |
| `stopTime` | no | `string` | format=date-time |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `fileName` | no | `string` | maxLength=255 |

Unknown object fields are rejected by this schema.
