# OCPP 1.6: DiagnosticsStatusNotification

Direction: **Charge Point → Central System**. CALL action: `DiagnosticsStatusNotification`.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `string` | values: Idle, Uploaded, UploadFailed, Uploading |

Unknown object fields are rejected by this schema.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| *(empty object)* | — | — | — |

Unknown object fields are rejected by this schema.
