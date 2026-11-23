# OCPI 2.3.0 stable implementation and migration

## Baseline and provenance

OCPI **2.3.0 is the current official stable protocol release**. Use it as the
stated default for new integrations, while negotiating each partner's actual
version. The [upstream README](https://github.com/ocpi/ocpi) identifies the
`2.3.0/release/*` branches as the maintained sources; `master`, release candidates,
and the frozen `release-2.3.0-bugfixes` branch are not the starting point for new work.

Verified on 2026-10-05 against:

- Stable [`v2.3.0`](https://github.com/ocpi/ocpi/tree/v2.3.0-ed2-payments)
- Maintained [core source](https://github.com/ocpi/ocpi/)
- [Published tag inventory](https://github.com/ocpi/ocpi/tags)
- Separate [Payments](https://github.com/ocpi/ocpi/tree/2.3.0/release/payments)
  and [Bookings](https://github.com/ocpi/ocpi/tree/2.3.0/release/bookings) packages.
  Pin their own commit and module/core pairing when implementing them. The
  Bookings source may be newer than the `v2.3.0-bookings` tag.

Do not equate stable `2.3.0`, an edition 2 tag, and every optional module with one
universally deployed contract. A core/module edition is not a new wire version.
Record protocol, source commit, edition, package, topology, role identities,
discovered interfaces, partner deviations, and contract-test evidence.

## Concrete changes from 2.2.1-d2

Read the [official changelog](https://github.com/ocpi/ocpi/blob/3979887793d934cdc64e2ca2c78b89cbbf79d56f/changelog.asciidoc)
and selected module definitions. The following changes affect real code:

| Area | 2.3.0 contract | Implementation consequence |
|---|---|---|
| JSON extensions | Unknown JSON field names must not by themselves cause rejection. | Accept extension fields; still validate required fields and supported behavior. Avoid blanket strict object validators. |
| Open enums | Selected enums, including ModuleID, VersionNumber, connector/capability/vehicle classifications, are OpenEnum strings. | Preserve unknown values; distinguish known executable capabilities from unknown descriptive values. Do not make every enum open. |
| Location support | `Location.help_phone` is optional. | Store/display support contact; do not invent `support_phone`. |
| Parking | `Location.parking_places` contains Parking objects; `EVSE.parking` contains EVSEParking links using `parking_id` and optional `evse_position`. | Model parking identity within a Location and multiple EVSE/parking links. Do not put a `vehicle_type` array on Location or EVSE. |
| Vehicle/accessibility | `Parking.vehicle_types`, dimensions, accessibility and other parking constraints provide richer data. | Preserve units and applicability. Known values include `PERSONAL_VEHICLE`, `MOTORCYCLE`, `VAN`, and `DISABLED`; do not substitute invented `CAR`/`TRUCK` categories. |
| Accepted contracts | `EVSE.accepted_service_providers` lists eMSP names. | Preserve names for information; this list is not party-ID routing or proof of token authorization. |
| Connector information | `Connector.capabilities` includes ISO 15118-2/20 Plug & Charge values; connector standards include `SAE_J3400`. | Store connector-level capabilities independently of EVSE capabilities. Advertised support does not prove an authorization or charging outcome. |
| Hub credentials | `Credentials.hub_party_id` identifies the hub; hub-reachable parties appear in `roles`. | Separate authenticated platform connection from represented parties. Read [roles.md](roles.md) before routing or authorization code. |
| Session/CDR money | `Price` now uses required `before_taxes` plus `taxes` entries. | Replace the 2.2.1 `excl_vat`/`incl_vat` DTO; migrate estimates, CDR costs, billing mapping, UI, and contracts together. |
| Tariff money | Required `Tariff.tax_included` uses `YES`, `NO`, or `N/A`; min/max use `PriceLimit`. | Validate the field and tax basis; PriceLimit has required `before_taxes`, optional `after_taxes`. Do not reuse the Session/CDR Price schema. |

Exact definitions: [Locations](https://github.com/ocpi/ocpi/blob/3979887793d934cdc64e2ca2c78b89cbbf79d56f/mod_locations.asciidoc),
[shared types](https://github.com/ocpi/ocpi/blob/3979887793d934cdc64e2ca2c78b89cbbf79d56f/types.asciidoc),
[Tariffs](https://github.com/ocpi/ocpi/blob/3979887793d934cdc64e2ca2c78b89cbbf79d56f/mod_tariffs.asciidoc),
[Credentials](https://github.com/ocpi/ocpi/blob/3979887793d934cdc64e2ca2c78b89cbbf79d56f/credentials.asciidoc).

`TaxAmount` requires `name` and `amount`; `percentage` and `account_number` are
optional. Keep the transmitted tax breakdown and decimal precision. Do not assume
one VAT rate, require a percentage when absent, or backfill missing tax data with
zero. An absent breakdown is not evidence of exemption. Downgrading a multi-tax
Price to a 2.2.1 Price can lose meaning; define a verified mapping or reject an
unsupported conversion rather than silently inventing a VAT-only representation.

For extensibility, keep unknown descriptive values and safe extension evidence
without granting new permissions or invoking unknown commands. Apply size/depth
limits and safe logging. The transport guide discourages `x-`/`custom` field-name
prefixes; no mandatory `custom_data` wrapper was introduced. OpenAPI `x-*`
specification metadata is a separate mechanism from OCPI payload extensions.

## Edition 2 differences: gate on the selected edition

| Correction/addition | Required engineering check |
|---|---|
| CDR `PARKING_TIME` refers to time the vehicle is not requesting power. | Do not charge loitering fees just because station/grid control withheld energy while the EV was requesting it. Use evidence of demand; zero measured power is insufficient. The Tariffs summary still says “not charging”; resolve that shorthand against the corrected CDR definition and selected agreement. |
| `SignedValue.plain_data` supports up to 5000 characters. | Update storage, validators and OpenAPI; preserve signed content without truncation or case changes. |
| Location address/state length correction | In inspected core, Location `address` allows 255 characters and `state` 45. CdrLocation still specifies 45/20; use its own schema rather than copying Location constraints. |
| Authentication status clarification | Missing/unknown credentials and bootstrap TOKEN_A used outside Versions/Credentials return HTTP 401 in the inspected transport source. Verify all HTTP/error mappings against the selected revision. |
| Tariff step-size example correction | Test numerical examples and combined dimensions; do not implement an erroneous example as the pricing rule. |
| EVSE parking examples corrected | Use `evse_position` in EVSEParking, not a guessed field name. |
| Invoice Reconciliation | Implement `InvoiceReconciliationRecord` only for an agreed edition/capability; it links invoices to CDR IDs and does not execute payments or settle disputes. |

Edition 2 source: [changelog](https://github.com/ocpi/ocpi/blob/3979887793d934cdc64e2ca2c78b89cbbf79d56f/changelog.asciidoc),
[CDRs](https://github.com/ocpi/ocpi/blob/3979887793d934cdc64e2ca2c78b89cbbf79d56f/mod_cdrs.asciidoc),
[transport](https://github.com/ocpi/ocpi/blob/3979887793d934cdc64e2ca2c78b89cbbf79d56f/transport_and_format.asciidoc),
[Invoice Reconciliation](invoice-reconciliation.md).

## Changes that must not be misattributed to 2.3.0

- `CdrToken.country_code` and `party_id` were already required in 2.2.1. Corrected
  2.2.1-d2 examples are not newly added 2.3.0 fields.
- `StartSession.evse_uid` remains optional, but is required when `connector_id`
  is supplied. `connector_id` is required for `START_SESSION_CONNECTOR_REQUIRED`.
  It was added to StartSession in 2.2.1; do not invent a ReserveNow connector field.
- Command acceptance and the later CommandResult remain separate from observed
  charging. Do not invent mandatory Session PATCH deadlines or contiguous
  ChargingPeriod requirements from vague “transparency” claims.
- AFIR-related fields do not alone prove regulatory compliance. Do not claim
  `AD_HOC_PAYMENT` became universally mandatory as an OCPI 2.3.0 rule.

## Migration and acceptance workflow

1. Inventory the supported roles, module interfaces, DTOs, validators, persisted
   monetary values, hub paths, generated clients, and existing partner versions.
2. Build a module/field delta against the exact old and new source commits.
   Add version-specific adapters; translate validated data into the domain.
3. Add storage for parking links, help contact, accepted provider names,
   connector capabilities, hub parties, and tax breakdown where needed. Preserve
   old wire evidence, tariff snapshots, CDRs, and historical interpretation.
4. Negotiate Versions and read endpoint details for each peer. Advertise only
   implemented module/interface pairs. Optional modules require a compatible
   package/edition and explicit partner agreement, not just `2.3.0` discovery.
5. Generate versioned OpenAPI JSON and fixtures using
   [code-design-and-api.md](../code-design-and-api.md). Keep 2.2.1 contracts for
   existing partners; do not change every partner when adding a new version.
6. Test both versions: required/unknown fields, unknown open and invalid closed
   enums, tax conversion, long signed values, parking referential integrity,
   hub party substitution, bootstrap scope, credential rotation, pagination,
   retries, callback outcomes, late CDRs, and unsupported modules.
7. Report source pins, implemented capabilities, validation results, migration
   and rollback behavior. Claim conformance only for what has been verified.
