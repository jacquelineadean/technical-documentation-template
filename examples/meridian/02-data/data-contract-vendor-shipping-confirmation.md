---
doc_id: DCT-VND-001
title: Fulfilment Vendors → Meridian — Data Contract for Shipping Confirmation
doc_type: dct
status: approved
version: 2.1.0
owner: Vendor Integration Lead
reviewers: [Order Data Steward, Finance Controller, Sales Data Steward]
approvers: [Vendor Integration Lead, VP Order Operations]
created: 2025-03-05
last_reviewed: 2026-06-11
next_review: 2026-12-11
review_cycle: semi-annual
classification: internal
systems: [MERIDIAN]
domains: [order-processing, vendor-integration]
upstream_docs: [DGC-MER-001]
downstream_docs: [DLN-OPS-001]
related_interfaces: [IF-044]
tags: [data-contract, vendor, asn, edi]
---

# Fulfilment Vendors → Meridian — Data Contract for Shipping Confirmation

> **Distinct from the ICD.** [ICD-VND-002](../03-interfaces/icd-vendor-dispatch-outbound.md)
> governs transport mechanics for the vendor interfaces. This governs **meaning and
> guarantees**: what `ship_date` records, what quantity means when a shipment is split, and
> what a vendor commits to about timeliness and accuracy.
>
> It exists because a vendor can send a perfectly valid EDI 856 that means something
> different from what Meridian assumes — and that failure is invisible to every schema check.

---

## 1. Parties

| Role | Party | Accountable role | Signed |
| --- | --- | --- | --- |
| **Producer** | 43 fulfilment vendors | Each vendor's nominated data contact | **38 of 43** ⚠️ |
| **Consumer** | Meridian Order Processing | VP, Order Operations | ✅ 2025-03-05 |
| Additional consumer | Meridian Sales Processing (incentive eligibility) | Director, Sales Operations | ✅ 2025-03-05 |
| Additional consumer | Corporate ERP (AR, via invoice) | Finance Systems Lead | ✅ 2025-03-05 |

| | |
| --- | --- |
| Contract version | 2.1 |
| Effective from | 2026-07-01 |
| Review date | 2026-12-11 |
| Termination notice | Per each vendor's master agreement — 90 or 180 days |

**Unsigned vendors** — for these five, `SHP_DT` semantics are 🟡 **inferred** from observed
data patterns rather than agreed. Their shipments carry a higher restatement risk at period
boundaries.

| Vendor | Volume share | Blocker | Owner | Target |
| --- | --- | --- | --- | --- |
| V19 | 4.1% | Legal review of the semantic-change clause | Vendor Integration Lead | 2026-10-31 |
| V27 | 1.8% | No nominated data contact | Vendor Integration Lead | 2026-09-30 |
| V31 | 0.9% | Disputes the 4-hour timeliness commitment | Vendor Integration Lead | 2026-11-30 |
| V38 | 0.6% | In contract renegotiation | Commercial | 2027-Q1 |
| V41 | 0.3% | Onboarded 2026-05; signature pending | Vendor Integration Lead | 2026-09-30 |

---

## 2. Dataset

| | |
| --- | --- |
| Name | Shipping confirmation (Advance Shipping Notice) |
| Description | Notification that goods against a dispatch instruction have been handed to a carrier |
| **Grain** | **One record per dispatch instruction per shipment event.** A split shipment produces multiple records for one `DSP_ID` |
| Delivery mechanism | EDI 856 over AS2 or SFTP |
| Interface | `IF-044` |
| Format | X12 004010, transaction set 856 |
| Typical volume | ~17,100/day across 43 vendors |
| Peak volume | ~48,000/day |
| Peak driver | Model-year changeover; vendors clear backlogs |
| Classification | Internal; the combination with `DSP_INS` is Confidential (reveals pricing) |
| Permitted uses | Order status, invoice trigger, incentive eligibility, vendor performance reporting |
| Prohibited uses | **Disclosure of one vendor's data to another**, including in aggregate performance benchmarks where a vendor is identifiable |

---

## 3. Schema and semantics

| # | Field | EDI source | Type | Req | Description | Example |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `dispatch_id` | `PRF-01` | `AN(20)` | M | The dispatch instruction being confirmed | `DSP260612V07-00891` |
| 2 | `ship_date` | `DTM-02` qual 011 | `DT(8)` | M | See §3.1 | `20260619` |
| 3 | `ship_quantity` | `SN1-01` | `N0(9)` | M | Units handed to the carrier in **this** event | `10` |
| 4 | `total_quantity` | `SN1-02` | `N0(9)` | M | Total units to be shipped against this dispatch | `12` |
| 5 | `carrier_code` | `TD5-03` | `AN(4)` | M | SCAC or an agreed pseudo-carrier | `ABCD` |
| 6 | `tracking_ref` | `REF-02` qual `CN` | `AN(30)` | C | Required when the carrier supports tracking | — |
| 7 | `shipment_seq` | `HL-01` | `N0(3)` | M | Sequence within the dispatch; starts at 1 | `1` |
| 8 | `final_flag` | `REF-02` qual `ZZ01` | `AN(1)` | M | `Y` when no further shipment will follow | `N` |

**Keys and constraints**

| Constraint | Fields | Notes |
| --- | --- | --- |
| Uniqueness | `(dispatch_id, shipment_seq)` | Duplicates rejected at ingest |
| Referential | `dispatch_id` must exist in `DSP_INS` | Unmatched rejected with an error file |
| Balance | `SUM(ship_quantity)` across sequences ≤ `total_quantity` | Excess rejected |
| Terminal | Exactly one record per `dispatch_id` with `final_flag = 'Y'` | A second is rejected |

---

### 3.1 `ship_date` semantics ⚠️

> The clause this contract exists for.

| Aspect | Agreed meaning |
| --- | --- |
| **What it records** | The date the goods were **handed to the carrier at the origin facility** — not the date the label was printed, not the date of pick, not the date the carrier scanned them |
| **Timezone** | **The origin facility's local date.** No offset is supplied and none is expected |
| **Meridian's handling** | Stored **as received**, without conversion to UTC |
| **Downstream effect** | `INV_LIN.INV_DT = SHP_DT`, so invoice date and therefore accounting period derive directly from this value |
| **Period boundary** | A shipment leaving Singapore at 23:00 on the 31st is dated the 31st locally, which may be the 30th UTC. Meridian uses the local date, so it falls in the earlier period |

**Why this clause exists.** Before it, three interpretations were in use across the vendor
base: label print date (11 vendors), carrier handover (26 vendors), and first carrier scan
(6 vendors). The spread between print and first scan averaged 1.4 days, which at a period
boundary moved revenue between months. A 2024 SOX sample test found 340 lines recognised in
the wrong period as a result.

| Aspect | Detail |
| --- | --- |
| Null | Not permitted; `ship_date` is mandatory |
| Future dates | **Rejected.** A date later than the receipt date + 1 day is rejected with `ERR-856-14` |
| Back-dated | Accepted up to 30 days before receipt; beyond that, rejected with `ERR-856-15` |
| Precision | Date only; no time component is transmitted or expected |

---

### 3.2 Quantity semantics

| Aspect | Agreed meaning |
| --- | --- |
| `ship_quantity` | Units in **this** shipment event, not cumulative |
| `total_quantity` | The total the vendor expects to ship against this dispatch. **May be less than the dispatched quantity** — that is a short ship |
| Short ship | `total_quantity < DSP_INS.QTY`. Meridian invoices only what shipped and leaves the residual open |
| Over ship | `SUM(ship_quantity) > total_quantity` is **rejected**. `total_quantity > DSP_INS.QTY` is rejected |
| Zero quantity | A record with `ship_quantity = 0` is rejected; a vendor cancelling a dispatch uses a 997 rejection or a separate cancellation message |
| Unit of measure | Always the dispatch's unit of measure. **No UOM is transmitted**; it is implied by the dispatch |

> The last row is a deliberate simplification carried over from 2014 and it is a latent
> risk: if any product line ever ships in a different UOM from the one ordered, the contract
> has no way to express it. Noted as an accepted limitation in §4.

---

### 3.3 Other semantics

| Field | Semantic guarantee |
| --- | --- |
| `dispatch_id` | Echoed exactly as transmitted in the 850. Case-sensitive, no trimming |
| `carrier_code` | A published SCAC, or one of the six agreed `MER1`–`MER6` pseudo-carriers for vendor-managed transport |
| `tracking_ref` | Where supplied, resolvable on the carrier's public tracking service for at least 90 days |
| `final_flag` | `'Y'` is a commitment that **no further shipment will follow** for this dispatch. Meridian closes the residual and stops expecting more |
| `shipment_seq` | Monotonic from 1, no gaps. A gap indicates a lost message and triggers investigation |

| Aspect | Definition |
| --- | --- |
| Null means | Not permitted on mandatory fields; on `tracking_ref`, "the carrier does not support tracking" |
| Absent field means | Same as null for optional fields |
| Empty string means | **Not permitted.** Omit the element instead |
| Character encoding | ASCII; extended characters are transliterated by the vendor before transmission |
| Date convention | `CCYYMMDD`, no separators |

---

## 4. Quality guarantees

| Dimension | Guarantee | Measurement | Breach notification |
| --- | --- | --- | --- |
| **Timeliness** | 856 transmitted within **4 hours** of carrier handover | Meridian receipt timestamp vs. `ship_date` + agreed cutoff | Monthly vendor scorecard; breach above 5% triggers review |
| **Completeness** | An 856 for **every** dispatched line, including short ships and cancellations | Dispatch-to-ASN reconciliation | Weekly; escalation above 50 unmatched |
| **Accuracy — date** | `ship_date` accurate to the day, per §3.1 | Quarterly sample against carrier records | Immediate for a systematic error |
| **Accuracy — quantity** | `ship_quantity` matches physical units handed over | Carrier weight/count reconciliation, sampled | As above |
| **Validity** | Conforms to §3 | Ingest validation | Immediate, error file |
| **Uniqueness** | No duplicate `(dispatch_id, shipment_seq)` | Unique key at ingest | Immediate, rejected |

**Known limitations** — accepted defects consumers must design around:

| Limitation | Extent | Workaround | Remediation |
| --- | --- | --- | --- |
| `ship_date` has no time or offset | All vendors | Period-boundary shipments are reviewed manually at close | Would require an X12 layout change across 43 vendors — not planned |
| No unit of measure transmitted | All vendors | UOM implied by the dispatch | Accepted; would need a contract and layout change |
| 5 vendors have not signed | 7.7% of volume | Their `ship_date` semantics are inferred | §1 |
| No cancellation message | All vendors | A dispatch the vendor will not fulfil is communicated by email | **Gap** — proposed for contract v3.0 |
| Tracking reference not validated | All vendors | ~2% are unresolvable on the carrier's service | Accepted; low business impact |

---

## 5. Availability and delivery

| Aspect | Commitment |
| --- | --- |
| Schedule | Event-driven, continuous |
| Delivery deadline | Within 4 hours of carrier handover |
| Availability target | Vendor's EDI endpoint available ≥ 99.0% monthly |
| Freshness | Data as-at handover; Meridian receipt is stamped separately |
| Late delivery notification | Vendor notifies if their system is down > 4 hours |
| Missing delivery notification | **Meridian's obligation** — the daily ASN-expected control (in development, `DI-2026-003`) will alert both sides |
| Retention at the producer | 12 months, per the master agreement |
| Replay | Vendor will retransmit on request for up to 30 days |
| Recovery time after failure | 24 hours to restore transmission and clear backlog |

---

## 6. Semantics of change

| Change class | Examples | Notice | Consent |
| --- | --- | --- | --- |
| Non-breaking | New optional `REF` segment; a new agreed pseudo-carrier | 30 days | Not required |
| Breaking — schema | Remove a segment; make an optional element mandatory; change a length | **90 days** | Required, both sides |
| **Breaking — semantic** | **Change what `ship_date` records; change quantity semantics; change `final_flag` meaning** | **180 days** | **Required, both sides, in writing** | 
| Breaking — quality | Lower a timeliness or completeness guarantee | 90 days | Required |
| Emergency | Correcting a defect causing active harm | Immediate + post-hoc notification | Notify |

> **Semantic change carries the longest notice, and deliberately so.** A vendor that changes
> `ship_date` from handover to label print keeps the field name, type, and format identical.
> Every schema validation passes. The only symptom is that revenue starts landing in the
> wrong period, and it takes a quarterly SOX sample to find it.
>
> **This clause has been invoked once.** In 2025-10, vendor V12 changed their WMS and
> `ship_date` silently became label print date. Detected after 6 weeks by the period-boundary
> review; 890 lines were re-dated and one period was restated. V12 had given no notice
> because their own team did not consider it a change to the interface. The 180-day clause
> and an explicit list of what counts as semantic change were added in contract v2.0 as a
> direct result.

**Deprecation**

| Step | Timing |
| --- | --- |
| Announce | 180 days before |
| Parallel availability | 90 days |
| Migration window | 90 days |
| Removal | At the end of parallel running |

---

## 7. Consumer obligations

| Obligation | Detail |
| --- | --- |
| Permitted use | §2 |
| Onward sharing | **Never share one vendor's data with another**, including in identifiable aggregate |
| Storage and retention | 7 years, per SOX |
| Security | Confidential when joined to `DSP_INS`; access per `DGC-MER-001` |
| Report defects within | 5 business days of detection |
| Test against new versions within | 30 days of a sandbox being made available |
| Maintain contact details | Reviewed at each semi-annual contract review |
| Notify the producer of material usage change | Meridian must tell vendors if ASN data starts driving a new decision — e.g. the 2025 addition of incentive eligibility |

---

## 8. Monitoring

| Metric | Measured by | Frequency | Threshold | Published to |
| --- | --- | --- | --- | --- |
| Timeliness — % within 4h | Meridian | Daily, reported monthly | ≥ 95% | Vendor scorecard |
| Completeness — unmatched dispatches | Meridian | Weekly *(daily in development)* | ≤ 50 | Vendor Integration |
| Schema conformance — rejection rate | Meridian | Daily | ≤ 0.5% | Vendor scorecard |
| Duplicate rate | Meridian | Daily | 0 | Vendor Integration |
| Date accuracy — sample vs. carrier records | Meridian + vendor | Quarterly | ≥ 99% | Both |
| Per-vendor volume vs. 4-week average | Meridian | Daily *(in development)* | ≥ 40% | Vendor Integration |

**Current performance** *(2026-Q2, 43 vendors)*

| Metric | Best | Median | Worst | Below threshold |
| --- | --- | --- | --- | --- |
| Timeliness | 99.8% | 97.2% | **81.4%** (V19) | 4 vendors |
| Rejection rate | 0.0% | 0.1% | **2.3%** (V31) | 3 vendors |
| Completeness | 0 unmatched | 2 | **41** (V19) | 2 vendors |

---

## 9. Incident handling

| Scenario | Producer action | Consumer action | Notification | Target resolution |
| --- | --- | --- | --- | --- |
| Transmission missed | Retransmit | Hold invoicing for affected lines | Vendor → Meridian within 4h | 24h |
| Malformed record | Correct and retransmit | Error file returned; line stays undispatched-confirmed | Automatic | 24h |
| Wrong `ship_date` detected | Send a corrected 856 with the same `shipment_seq` | **Re-date the invoice; restate the period if closed** | Either party | 5 business days |
| Duplicate transmission | — | Rejected at ingest; no action needed | Automatic | — |
| Vendor system outage > 4h | Notify Meridian; agree a catch-up plan | Suspend the ASN-expected alert for that vendor | Vendor → Meridian | Per outage |
| **Semantic drift suspected** | Confirm current interpretation in writing | Quarterly sample against carrier records | Either party | 10 business days |

**Restatement protocol**

| Step | Action | Owner |
| --- | --- | --- |
| 1 | Meridian identifies the scope and financial magnitude | Order Data Steward |
| 2 | Affected consumers notified **before** correction — ERP AR, SPR incentive, warehouse | Order Data Steward |
| 3 | Corrected records ingested, clearly flagged as restatements | Vendor Integration |
| 4 | Invoices re-dated; credit and re-invoice if a period has closed | Finance Controller |
| 5 | Incentive attainment recomputed if the period is still open, else an `LA` adjustment | Sales Data Steward |
| 6 | Root cause recorded in the data issue log | Order Data Steward |

---

## 10. Dispute resolution

| Step | Forum | Timeframe |
| --- | --- | --- |
| 1 | Vendor data contact ↔ Vendor Integration Lead | 5 business days |
| 2 | Vendor account manager ↔ VP Order Operations | 10 business days |
| 3 | Commercial escalation per the master agreement | Per contract |

---

## 11. Change log

| Contract version | Date | Change | Class | Notice | Approved by |
| --- | --- | --- | --- | --- | --- |
| 2.1 | 2026-06-11 | Added the per-vendor volume monitoring metric; recorded the 5 unsigned vendors explicitly | Non-breaking | 30 days | Vendor Integration Lead |
| 2.0 | 2025-11-14 | **Added the 180-day semantic-change clause and an explicit list of what counts as semantic change**, after the V12 incident | Breaking (process) | 90 days | Vendor Integration Lead, VP Order Operations |
| 1.1 | 2025-07-02 | Added `final_flag` semantics after two vendors interpreted it differently | Clarification | 30 days | Vendor Integration Lead |
| 1.0 | 2025-03-05 | Initial contract. `ship_date` semantics agreed and pinned for the first time | — | — | Vendor Integration Lead, VP Order Operations |
