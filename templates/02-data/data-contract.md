---
doc_id: DCT-<SCOPE>-001
title: <Producer> → <Consumer> — Data Contract for <Dataset>
doc_type: dct
status: draft
version: 0.1.0
owner: <Producer Data Owner role>
approvers: [<Producer Data Owner>, <Consumer Data Owner>]
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: semi-annual
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [DGC-<SCOPE>-001]
downstream_docs: []
related_interfaces: []
tags: [data-contract]
---

# \<Producer\> → \<Consumer\> — Data Contract for \<Dataset\>

> **Purpose.** A binding agreement between a data producer and its consumers covering
> schema, semantics, quality, availability, and change. Distinct from an
> [ICD](../03-interfaces/interface-control-document.md): an ICD governs *transport and
> payload mechanics*; a data contract governs *meaning and guarantees*. A dataset delivered
> over an interface generally needs both.
>
> **Rule of two.** Both sides approve. A contract signed by the producer alone is a
> publication, not an agreement.

---

## Contents

| Section | Summary |
| --- | --- |
| [1. Parties](#1-parties) | Producer, consumer, accountable roles, signatures |
| [2. Dataset](#2-dataset) | Dataset name, grain, volume, classification |
| [3. Schema](#3-schema) | Field-level schema with types, optionality, valid values, CDE flags |
| [4. Quality guarantees](#4-quality-guarantees) | Per-dimension quality guarantees, measurement, breach notification |
| [5. Availability and delivery](#5-availability-and-delivery) | Schedule, delivery deadline, transport, availability commitment |
| [6. Semantics of change](#6-semantics-of-change) | Breaking versus non-breaking change classes, notice periods, consent |
| [7. Consumer obligations](#7-consumer-obligations) | Permitted use, onward sharing, and consumer-side obligations |
| [8. Monitoring and reporting](#8-monitoring-and-reporting) | Metrics published against the contract, with thresholds |
| [9. Incident handling](#9-incident-handling) | Missed, late, and defective delivery: actions and target resolution |
| [10. Dispute resolution](#10-dispute-resolution) | Escalation path from stewards to owners, with timeframes |
| [11. Change log](#11-change-log) | Contract version, change class, notice given, approver |

---

## 1. Parties

| Role | Party | Accountable role | Contact | Signed |
| --- | --- | --- | --- | --- |
| Producer | | | | |
| Consumer | | | | |
| Additional consumers | | | | |

| | |
| --- | --- |
| Contract version | |
| Effective from | |
| Review date | |
| Termination notice | |

---

## 2. Dataset

| | |
| --- | --- |
| Name | |
| Description | |
| Grain | *(what one record represents)* |
| Delivery mechanism | |
| Interface ID | IF-… |
| Format | |
| Typical volume | |
| Peak volume and driver | |
| Classification | |
| Permitted uses | |
| Prohibited uses | *(e.g. not for onward distribution; not for automated credit decisions)* |

---

## 3. Schema

| # | Field | Type | Required | Description | Valid values | Example | CDE |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | | ✅/❌ |

**Keys and constraints**

| Constraint | Fields | Notes |
| --- | --- | --- |
| Primary key | | |
| Uniqueness | | |
| Referential | | |
| Ordering | | |

**Semantics** — the part a schema cannot express:

| Field | Semantic guarantee |
| --- | --- |
| | *(e.g. `ship_date` is the date the carrier took possession, not the date the label was printed; timezone is the origin warehouse's local date)* |

| Aspect | Definition |
| --- | --- |
| Null means | |
| Absent field means | |
| Empty string means | |
| Zero means | |
| Monetary precision and rounding | |
| Timezone | |
| Date range convention | |
| Character encoding | |

> The semantics table is the reason this document exists separately from a schema
> registry. Two systems agreeing on `date` and disagreeing on what event the date records
> is the defect a data contract prevents.

---

## 4. Quality guarantees

| Dimension | Guarantee | Measurement | Breach notification |
| --- | --- | --- | --- |
| Completeness | | | |
| Validity | | | |
| Accuracy | | | |
| Uniqueness | | | |
| Timeliness | | | |
| Consistency | | | |

**Known limitations** *(accepted defects the consumer must design around)*

| Limitation | Extent | Workaround | Remediation planned |
| --- | --- | --- | --- |
| | | | |

---

## 5. Availability and delivery

| Aspect | Commitment |
| --- | --- |
| Schedule | |
| Delivery deadline | |
| Availability target | |
| Freshness (data as-at) | |
| Late delivery notification | |
| Missing delivery notification | |
| Retention at the producer | |
| Replay/backfill availability | |
| Recovery time after failure | |

**Delivery calendar**

| Period | Expected | Exceptions |
| --- | --- | --- |
| | | *(holidays, month-end, freeze periods)* |

---

## 6. Semantics of change

> The clauses that make the contract worth having.

| Change class | Examples | Notice | Consumer consent |
| --- | --- | --- | --- |
| Non-breaking | New optional field; new code value in an open set; documentation clarification | \<N\> days | Not required |
| Breaking — schema | Remove field; make optional field required; change type; narrow length | \<N\> days | Required |
| Breaking — semantic | Change a field's meaning; change a derivation; change grain; change a filter | \<N\> days | Required |
| Breaking — quality | Lower a quality guarantee; lower availability | \<N\> days | Required |
| Emergency | Correction of a defect that is actively causing harm | Immediate + post-hoc | Notify |

**Semantic change deserves the longest notice.** A field that keeps its name, type, and
nullability while changing what it counts passes every automated compatibility check and
breaks every consumer silently. Examples of semantic change to treat as breaking:

- A filter added or removed upstream (fewer or more rows for the same query)
- A derivation's rounding or tie-break rule changed
- A code set value's behaviour changed
- Grain changed from one row per line to one row per order
- A date changed from event date to processing date

**Deprecation**

| Step | Timing |
| --- | --- |
| Announce | |
| Parallel availability | |
| Consumer migration window | |
| Removal | |

---

## 7. Consumer obligations

| Obligation | Detail |
| --- | --- |
| Permitted use | |
| Onward sharing | |
| Storage and retention | |
| Security controls | |
| Report defects within | |
| Test against new versions within | |
| Maintain contact details | |
| Notify the producer of material usage change | *(volume, criticality, new downstream consumers)* |

---

## 8. Monitoring and reporting

| Metric | Measured by | Frequency | Threshold | Published to |
| --- | --- | --- | --- | --- |
| Delivery timeliness | | | | |
| Record counts vs. expected | | | | |
| Quality rule pass rate | | | | |
| Schema conformance | | | | |
| Consumer-reported defects | | | | |

---

## 9. Incident handling

| Scenario | Producer action | Consumer action | Notification | Target resolution |
| --- | --- | --- | --- | --- |
| Delivery missed | | | | |
| Delivery late | | | | |
| Quality breach detected before delivery | | | | |
| Quality breach detected after consumption | | | | |
| Schema violation | | | | |
| Data requires restatement | | | | |
| Duplicate delivery | | | | |

**Restatement protocol**

| Step | Action | Owner |
| --- | --- | --- |
| 1 | Producer identifies scope and magnitude | |
| 2 | Consumers notified with affected periods | |
| 3 | Corrected data delivered, clearly identified as a restatement | |
| 4 | Consumers confirm reprocessing complete | |
| 5 | Root cause recorded in the data issue log | |

---

## 10. Dispute resolution

| Step | Forum | Timeframe |
| --- | --- | --- |
| 1 — Stewards | | |
| 2 — Data Owners | | |
| 3 — Data Governance Council | | |
| 4 — Executive Sponsor | | |

---

## 11. Change log

| Contract version | Date | Change | Class | Notice given | Approved by |
| --- | --- | --- | --- | --- | --- |
| 1.0.0 | | Initial | — | — | |
