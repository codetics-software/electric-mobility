# OCPP 1.6: GetDiagnostics

Direction: **Central System → Charge Point**. CALL action: `GetDiagnostics`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA OCPP-J JSON schema set. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state.

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
