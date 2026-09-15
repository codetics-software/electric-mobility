# OCPI — InvoiceReconciliation Module

## Purpose

The InvoiceReconciliation module provides a **standardized mechanism for CPOs and eMSPs to reconcile billing discrepancies** — when the eMSP's calculated invoice amount differs from the CPO's expected total. Rather than email exchanges and custom reports, both sides exchange structured reconciliation data through OCPI.

> This is an **optional module**, available in **2.3.0 edition 2** only (not in the initial 2.3.0 release or the bookings branch).

---

## Version Availability

| Version | Available |
|---|---|
| 2.1.1 | No |
| 2.2.1 | No |
| 2.3.0 (edition 1) | No |
| 2.3.0 (edition 2) | Yes — optional |

---

## Why Reconciliation Is Needed

Even with perfectly implemented OCPI, billing discrepancies occur due to:

- **Rounding differences**: Different implementations apply `step_size` rounding differently
- **Clock skew**: CPO and eMSP clocks differ by seconds, affecting time-based tariff periods
- **CDR retries**: A CDR pushed twice (network failure + retry) may cause duplicate processing
- **Tariff interpretation**: Complex tariff elements with restrictions can be interpreted differently
- **Credit CDR timing**: The original CDR and credit CDR are in different billing cycles

---

## Module Concept

The module introduces a structured workflow:

```
[Monthly billing cycle]
eMSP processes all CDRs from CPO
  ↓
eMSP generates invoice for CPO
  ↓
CPO validates invoice against its own CDR totals
  ↓
If discrepancy found:
  CPO → POST InvoiceReconciliation (list of disputed CDR IDs + amounts)
  eMSP → reviews, accepts or rejects each dispute
  Both → reach agreement or escalate
  ↓
Settled amounts confirmed
```

---

## Key Objects

### `InvoiceReconciliation`

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique reconciliation ID |
| `invoice_reference` | string | Reference to the disputed invoice |
| `period_start` | DateTime | Billing period start |
| `period_end` | DateTime | Billing period end |
| `status` | ReconciliationStatus | Current state |
| `disputes` | CdrDispute[] | List of disputed CDRs |
| `total_disputed_amount` | Price | Sum of all disputes |
| `last_updated` | DateTime | |

### `CdrDispute`

| Field | Type | Description |
|---|---|---|
| `cdr_id` | string | CDR being disputed |
| `expected_amount` | Price | What CPO expected |
| `invoiced_amount` | Price | What eMSP invoiced |
| `difference` | Price | The discrepancy |
| `reason` | string | Description of the dispute |
| `resolution` | DisputeResolution? | How it was resolved |

### `ReconciliationStatus`

| Value | Meaning |
|---|---|
| `PENDING` | Submitted, awaiting review |
| `UNDER_REVIEW` | eMSP is reviewing |
| `PARTIALLY_RESOLVED` | Some disputes settled |
| `RESOLVED` | All disputes settled |
| `REJECTED` | eMSP rejected the reconciliation request |

---

## Implementation Notes

### When to Use
Only necessary for high-volume CPO/eMSP relationships with regular billing cycles. For low-volume bilateral connections, email reconciliation may be sufficient.

### Idempotency
Reconciliation IDs must be stable — if a CPO resubmits the same reconciliation (retried POST), the eMSP must detect the duplicate by `invoice_reference` and return the existing record.

### Integration with CDRs
The CDR IDs in `CdrDispute` reference CDRs already exchanged via the CDRs module. Both parties must have already processed those CDRs before reconciliation begins.

---

## Spec References

- 2.3.0 edition 2: `mod_invoice_reconciliation.asciidoc` — `2.3.0/release/core` (edition 2 tag/commit)

> Note: The `2.3.0/release/bookings` branch does NOT include this module — it branched before edition 2. Use the core branch directly.
