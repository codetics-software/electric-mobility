# OCPP 1.6: FirmwareStatusNotification

Direction: **Charge Point → Central System**. CALL action: `FirmwareStatusNotification`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA OCPP-J JSON schema set. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Downloaded, DownloadFailed, Downloading, Idle, InstallationFailed, Installing, Installed |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| *(empty object)* | — | — | — |

Unknown object fields are rejected by this schema.
