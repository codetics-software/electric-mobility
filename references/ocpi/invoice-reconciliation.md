# OCPI Invoice Reconciliation

Source: [OCPI 2.3.0 core module](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_invoice_reconciliation.asciidoc). Pin core edition 2, such as [`v2.3.0-ed2`](https://github.com/ocpi/ocpi/tree/v2.3.0-ed2), and partner capability before implementation. The edition 2 tag exists even though a status cell in the repository README has not caught up.

## Purpose and ownership

The module identifier is `invoicereconciliation`. It exchanges an **InvoiceReconciliationRecord**: the issuing party's invoice ID and the explicit CDR IDs included in that invoice. It does not transfer the invoice document, conduct payment, or define a dispute workflow. A CPO usually issues the record for direct billing; an eMSP may issue it for reverse billing. Either can be sender or receiver according to who invoices.

The receiver compares the listed CDRs with its own records and the separately delivered invoice. Do not infer invoice membership from billing period or CDR arrival time; a late CDR may be omitted from one invoice and appear in another.

## Wire contract

The official `InvoiceReconciliationRecord` has `country_code`, `party_id`, `id`, `invoice_id`, one or more `cdrs` identifiers, and `last_updated`. There are no standard `status`, `disputes`, `expected_amount`, `total_disputed_amount`, or `resolution` fields in this module. Keep any local dispute case as a separate product-domain concept.

- Sender interface: paginated `GET` with `date_from`, `date_to`, `offset`, and `limit` for pull/recovery.
- Receiver interface: `POST` new record, `PUT` updated record, `GET` one record, and `DELETE` an erroneous record. The object identity is scoped by country code, party ID, and record ID; use the exact endpoint paths in the pinned specification.
- Push updates if supported; also reconcile with pull after outages. An updated record replaces its previous content. `DELETE` says the record itself was erroneous; invoice/CDR corrections can use an updated record.

## Implementation checks

- Make retries idempotent using the scoped record ID and content/version evidence. Do not deduplicate by `invoice_id` alone: an invoice and a record have different identities.
- Resolve listed CDR IDs within the correct partner and party scope. Detect missing, duplicated, credited, or corrected CDRs without silently changing the original record.
- Retain the invoice document and payment process outside OCPI. Record which local invoice and CDR snapshots were compared so later corrections remain auditable.
- Test direct and reverse billing, pagination after downtime, late CDR arrival, record updates, duplicate delivery, deletion, and cross-party IDs.
