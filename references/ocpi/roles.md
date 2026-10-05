# OCPI roles, interfaces, and authorization

Apply this guide in any assistant's analysis, design, review, or implementation.
The user's and assistant's task responsibilities are defined in
[agent working rules](../rules/agents.md); they are separate from these protocol roles.

## Keep four meanings of role separate

| Role concept | Represents | Must not be used as |
|---|---|---|
| Agent responsibility | User assigns work; assistant produces and validates the requested deliverable. | An OCPI credential or application permission. |
| Market role | What a party does: CPO, EMSP, NAP, NSP, SCSP, or OTHER in inspected 2.3.0 core. | Automatic authority over every module or every tenant. |
| InterfaceRole | `SENDER` or `RECEIVER` for a particular advertised module endpoint. | The HTTP client/server side of every request. |
| Product permission | Tenant/user/service authorization for a specific action or resource. | A credential role string alone. |

The wire value is `EMSP`; “eMSP” is the prose name. Read the selected edition's
[Role enum](https://github.com/ocpi/ocpi/blob/3979887793d934cdc64e2ca2c78b89cbbf79d56f/types.asciidoc)
and [Credentials](https://github.com/ocpi/ocpi/blob/3979887793d934cdc64e2ca2c78b89cbbf79d56f/credentials.asciidoc).
Do not carry the older `HUB` enum into this 2.3.0 contract. Hub functionality
is represented by `hub_party_id` and reachable role entries. PTP is a business
actor in Payments, not a listed core Role value; do not invent `PTP` or `PSP`
credential values without an agreed specification/profile mapping.

## Market responsibilities

| Party | Owns or is responsible for | Boundary |
|---|---|---|
| CPO | Location hierarchy, tariffs, operational Sessions and issued CDRs. | Delegates station communication to a CSMS; does not own eMSP tokens. |
| EMSP | Driver contracts, tokens, authorization decisions and driver service. | Initiates roaming commands; does not assert physical charging from acceptance alone. |
| NAP | National access/data aggregation. | Data access and publication depend on implemented modules and profile. |
| NSP | Navigation/location information consumption. | Receiving Locations does not authorize charging control. |
| SCSP | Smart charging services and profile decisions. | Profile exchange is distinct from station enforcement and measured behavior. |
| OTHER | A role outside the core named categories. | Not a wildcard permission. Record the actual agreed business purpose. |
| Hub platform | Transport routing and reachability of represented parties. | Authenticated hub connection does not transfer ownership of routed data. |
| CSMS | OCPP communication, station management, and operational evidence. | A system responsibility, not a core OCPI Credentials role. |
| PTP / payment service provider | Terminal operations / payment processing respectively. | Separate business actors; use the selected Payments package for wire mapping. |

A single platform can host several parties and roles. Key each CredentialsRole
by `(country_code, party_id, role)` and retain its business details. Do not store
only one role per connection or assign all its resources to the hub identity.

## Module interface ownership

| Module | Usual sender | Usual receiver | Direction trap |
|---|---|---|---|
| Locations / Tariffs | CPO | EMSP, NSP, NAP as supported | Pull GET is initiated by the receiver against the sender's interface. |
| Sessions / CDRs | CPO | EMSP | Receiver-side push does not make the EMSP the data owner. |
| Tokens | EMSP | CPO | Real-time authorization calls the EMSP sender interface. |
| Commands | EMSP | CPO | Immediate response, CPO callback, and observed charging are distinct. |
| Charging Profiles | EMSP/SCSP and CPO according to method | Counterparty | Consult method definitions; do not infer every flow from one ownership arrow. |
| Hub Client Info | Hub | Connected platform | Reachability data is not ownership of Locations/CDRs. |
| Payments | PTP for terminal-owned data | CPO as defined by method | Financial advice and other flows need their own direction checks. |
| Bookings | CPO for booking availability/resulting booking | EMSP | EMSP sends requests to CPO; distinguish request from authoritative booking state. |
| Invoice Reconciliation | Invoice issuer (CPO or EMSP) | Counterparty | Reverse billing swaps issuer; do not hard-code CPO as sender. |
| Credentials | Both platforms | Both platforms | For discovery, upstream advises `SENDER` and ignoring the peer's credentials interface role. |

Read the module before coding methods. `SENDER`/`RECEIVER` is scoped to the module,
not a permanent platform label. Use advertised URL and interface pairs from
[Versions details](https://github.com/ocpi/ocpi/blob/3979887793d934cdc64e2ca2c78b89cbbf79d56f/version_information_endpoint.asciidoc).

## Authorization and hub routing

1. Authenticate the platform connection with its credentials token. Store inbound
   verification and outbound calling credentials by direction; labels TOKEN_B/C
   depend on which platform initiated registration.
2. Resolve claimed source/destination parties from routing context, path, and
   object identity. Verify they are reachable and authorized under the direct
   connection or hub agreement; treat headers as claims, not proof.
3. Require agreement among authenticated connection, permitted market role,
   module interface, method, party ownership, and tenant scope before state
   changes. A CPO role cannot rewrite EMSP tokens or another CPO's records.
4. Keep platform, party, tenant, end user, station, and object identity separate.
   Apply per-type `CiString` comparison without normalizing case-sensitive signed
   data, credentials, or display strings.
5. Represent hub identity as the five-character country-code/party-ID combination
   in `hub_party_id`. In 2.3.0, retain the reachable parties in Credentials.roles.
   Refresh reachability and restrict routing when access is revoked. Do not use a
   stale role list as indefinite authorization.
6. Preserve `OCPI-from-*`, `OCPI-to-*`, and request/correlation headers according
   to the selected transport specification. Routing headers have defined
   exceptions; do not assume all four must be populated on every request.
7. Test mixed CPO/EMSP platforms, white-label parties, same local object IDs under
   different owners, delegated hub clients, forged routing identities, wrong
   methods/interfaces, removed parties, and cross-tenant access.

These checks combine protocol identity with local security policy. Distinguish
upstream obligations from deployment-specific authorization decisions.
