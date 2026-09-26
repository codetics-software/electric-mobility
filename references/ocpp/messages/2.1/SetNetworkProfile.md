# OCPP 2.1: SetNetworkProfile

Direction: **CSMS → Charging Station**. CALL action: `SetNetworkProfile`. Pair the request with the response using the message ID; a valid business rejection uses the response status where defined.

This is a compact wire-field reference derived from the OCA Part 3 JSON schema archive. `Required` and constraints are schema facts. Apply the version's use-case rules and security profile. An optional field is not automatically valid in every state. For OCPP 2.x, apply the adjacent [June 2026 errata digest](../../errata-2026-06.md); corrected use-case rules can narrow a schema-permitted value.

## Request payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `configurationSlot` | yes | `integer` |  |
| `connectionData` | yes | `NetworkConnectionProfileType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `APNAuthenticationEnumType`

Allowed values: `PAP`, `CHAP`, `NONE`, `AUTO`

#### `APNType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `apn` | yes | `string` | maxLength=2000 |
| `apnUserName` | no | `string` | maxLength=50 |
| `apnPassword` | no | `string` | maxLength=64 |
| `simPin` | no | `integer` |  |
| `preferredNetwork` | no | `string` | maxLength=6 |
| `useOnlyPreferredNetwork` | no | `boolean` | default=false |
| `apnAuthentication` | yes | `APNAuthenticationEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `NetworkConnectionProfileType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `apn` | no | `APNType` |  |
| `ocppVersion` | no | `OCPPVersionEnumType` |  |
| `ocppInterface` | yes | `OCPPInterfaceEnumType` |  |
| `ocppTransport` | yes | `OCPPTransportEnumType` |  |
| `messageTimeout` | yes | `integer` |  |
| `ocppCsmsUrl` | yes | `string` | maxLength=2000 |
| `securityProfile` | yes | `integer` | minimum=0.0 |
| `identity` | no | `string` | maxLength=48 |
| `basicAuthPassword` | no | `string` | maxLength=64 |
| `vpn` | no | `VPNType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.

#### `OCPPInterfaceEnumType`

Allowed values: `Wired0`, `Wired1`, `Wired2`, `Wired3`, `Wireless0`, `Wireless1`, `Wireless2`, `Wireless3`, `Any`

#### `OCPPTransportEnumType`

Allowed values: `SOAP`, `JSON`

#### `OCPPVersionEnumType`

Allowed values: `OCPP12`, `OCPP15`, `OCPP16`, `OCPP20`, `OCPP201`, `OCPP21`

#### `VPNEnumType`

Allowed values: `IKEv2`, `IPSec`, `L2TP`, `PPTP`

#### `VPNType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `server` | yes | `string` | maxLength=2000 |
| `user` | yes | `string` | maxLength=50 |
| `group` | no | `string` | maxLength=50 |
| `password` | yes | `string` | maxLength=64 |
| `key` | yes | `string` | maxLength=255 |
| `type` | yes | `VPNEnumType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.


## Response payload

| Field | Required | Type | Constraints |
|---|---|---|---|
| `status` | yes | `SetNetworkProfileStatusEnumType` |  |
| `statusInfo` | no | `StatusInfoType` |  |
| `customData` | no | `CustomDataType` |  |

Unknown object fields are rejected by this schema.


### Referenced types

#### `CustomDataType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `vendorId` | yes | `string` | maxLength=255 |

#### `SetNetworkProfileStatusEnumType`

Allowed values: `Accepted`, `Rejected`, `Failed`

#### `StatusInfoType`

| Field | Required | Type | Constraints |
|---|---|---|---|
| `reasonCode` | yes | `string` | maxLength=20 |
| `additionalInfo` | no | `string` | maxLength=1024 |
| `customData` | no | `CustomDataType` |  |

Unknown fields are rejected in this object.
