# OCPI versions available in the official repository

This is a routing and migration guide. The [official version history](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/version_history.asciidoc), [version discovery definition](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/version_information_endpoint.asciidoc), [repository tags](https://github.com/ocpi/ocpi/tags), and the selected version's module document are authoritative for exact wire behavior. These are the six numbered OCPI versions recorded by the current repository. Drafts 0.3 and 0.4 are historical documents, not production version targets. Release candidates and `-dN` documentation updates are not new protocol versions.

| Wire version | Official source to start from | Engineering distinction | Status for new work |
|---|---|---|---|
| **2.0** | [version history](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/version_history.asciidoc), then the 2.0 release document in the repository | Initial official version: location, authorization/token, tariff, session/CDR, credentials exchange. No Commands module. | Legacy partner compatibility only; confirm which 2.0 documentation revision (`2.0` or `2.0-d2`) the partner implements. |
| **2.1** | [version history](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/version_history.asciidoc), then the 2.1 release document | Introduced Commands and real-time authorization. | Deprecated by 2.1.1; implement only for a partner that actually negotiates it. |
| **2.1.1** | [`release-2.1.1-bugfixes`](https://github.com/ocpi/ocpi/tree/release-2.1.1-bugfixes); stable [2.1.1-d2 tag](https://github.com/ocpi/ocpi/tree/2.1.1-d2) | Fixes 2.1 defects; CPO/eMSP bilateral model. | Supported legacy line. Use the partner's exact revision and compatibility behavior. |
| **2.2** | [`release-2.2-bugfixes`](https://github.com/ocpi/ocpi/tree/release-2.2-bugfixes); stable [2.2-d2 tag](https://github.com/ocpi/ocpi/tree/2.2-d2) | Adds hubs, multi-role platforms, smart charging, and broad module changes. | Deprecated by 2.2.1; use only when negotiated by an existing partner. |
| **2.2.1** | [`release-2.2.1-bugfixes`](https://github.com/ocpi/ocpi/tree/release-2.2.1-bugfixes); [v2.2.1-d2 tag](https://github.com/ocpi/ocpi/tree/v2.2.1-d2) | Corrective release of 2.2; includes field/type and command changes such as `connector_id` on StartSession. | Common interoperability target; pin revision and hub profile. |
| **2.3.0** | [core branch](https://github.com/ocpi/ocpi/tree/2.3.0/release/core) and [tags](https://github.com/ocpi/ocpi/tags) | Extensible 2.3.0 core; edition 2 adds Invoice Reconciliation and other changes. Payments and Bookings are packaged separately. | Current line; pin core edition **and** optional module edition. |

The 2.3.0 packaging needs particular care. `v2.3.0` includes Payments in the older edition 1 lineage. `v2.3.0-ed1` is core edition 1; `v2.3.0-ed2` is core edition 2. The Payments line has `v2.3.0-payments` and `v2.3.0-ed2-payments`; Bookings has a separate release branch/tag. GitHub's [release list](https://github.com/ocpi/ocpi/releases) shows edition 2 tags, while the main README compatibility table still labels some combinations planned. Treat the actual tag's content and partner support as stronger evidence than that stale status cell. Do not combine Bookings and core edition 2 features unless a compatible published artifact is identified.

## Module availability by version line

This table guides source selection; it is not a claim that any particular partner exposes every available module. Confirm the Versions details endpoint and the module requirements for the chosen tag.

| Module group | 2.0 | 2.1 / 2.1.1 | 2.2 / 2.2.1 | 2.3.0 |
|---|---|---|---|---|
| Versions, Credentials, Locations, Sessions, CDRs, Tariffs, Tokens | Available | Available | Available | Available |
| Commands | No | Available | Available | Available |
| Charging Profiles, Hub Client Info | No | No | Available | Available |
| Invoice Reconciliation | No | No | No | Core edition 2 |
| Payments | No | No | No | Separate Payments package / older `v2.3.0` lineage |
| Bookings | No | No | No | Separate Bookings package |

## Version selection workflow

1. Use the peer's Versions endpoint to find a mutually supported **wire version**, then fetch that version's details and advertised module endpoints. Do not infer support for a module from the version number alone.
2. Record the version, document revision or edition, source tag/commit, platform roles, each module's sender/receiver interface, hub profile, and partner-specific deviations.
3. Validate incoming and outgoing objects against the selected version's exact field and enum rules. Keep versioned protocol DTOs; translate into a common domain model only after validation.
4. For migrations, compare semantics module by module: identity and roles, Credentials handshake, endpoint discovery, authorization, Location/EVSE/Connector, Session/CDR, tariff pricing, Commands callbacks, and optional modules. Reconcile persisted history instead of rewriting old records into a new wire shape.
5. Test both versions during a transition, including downgrade/unsupported-module behavior. Keep each partner pinned until its migration is confirmed.

## Version-sensitive traps

- **Commands:** no standard Commands module in 2.0; introduced in 2.1. A 2.0 remote start requires an out-of-band arrangement, not a fabricated OCPI endpoint.
- **Roles and hubs:** 2.2 introduced multi-role platforms and hub support. Do not apply 2.2 routing/role requirements to 2.1.1.
- **Documentation revision:** `-d2` clarifies text/examples without intentionally changing the wire contract. A patch version such as 2.1.1 or 2.2.1 can change fields and semantics.
- **Authorization header:** current transport guidance requires base64 encoding of the credentials token. The upstream guide documents older 2.1.1/2.2 implementations that sent it unencoded; isolate that exception per partner.
- **Optional modules:** Charging Profiles and Hub Client Info belong to the 2.2 line; 2.3.0 Payments and Bookings have independent packaging. Invoice Reconciliation belongs to core edition 2. Check endpoint discovery and the pinned source before using any of them.
