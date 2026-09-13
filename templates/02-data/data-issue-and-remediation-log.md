---
doc_id: DIL-<SCOPE>-001
title: <Domain or System> — Data Issue and Remediation Log
doc_type: dil
status: draft
version: 0.1.0
owner: <Data Steward role>
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: quarterly
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [DGC-<SCOPE>-001, DQR-<SCOPE>-001]
downstream_docs: []
tags: [data-quality, issues]
---

# \<Domain or System\> — Data Issue and Remediation Log

> **Purpose.** The standing register of known data defects: what is wrong, how wrong, who is
> affected, what is being done, and what consumers should do in the meantime.
>
> **Why a standing register rather than tickets.** A ticket closes; a data defect's
> *consequences* persist in historical data long after the cause is fixed. A consumer
> querying 2024 data needs to know that a defect affected it, even though the ticket closed
> in 2025. This log is where that survives.

---

## 1. Summary

| | Count |
| --- | --- |
| Open — Critical | |
| Open — High | |
| Open — Medium/Low | |
| Open > 90 days | |
| Closed this period | |
| Recurring (≥ 2 occurrences) | |

---

## 2. Open issues

| ID | Title | Element(s) | Severity | Detected | Age | Extent | Consumers affected | Status | Owner | Target |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DI-001 | | | | | | | | Triage / Contained / Remediating / Preventing / Verifying | | |

---

## 3. Issue detail

### DI-\<NNN\>: \<title\>

| | |
| --- | --- |
| Detected | |
| Detected by | *(DQ rule, consumer report, reconciliation break, incident, audit)* |
| Severity | |
| Status | |
| Owner | |
| Related incident | |
| Related lineage | |

**Description**

*(What is wrong, in terms a consumer can act on.)*

**Extent**

| Dimension | Value |
| --- | --- |
| Records affected | |
| Period affected | |
| Systems affected | |
| First occurrence | |
| Ongoing | Yes/No |
| Financial exposure | |

**Root cause**

| Aspect | Finding |
| --- | --- |
| Immediate cause | |
| Contributing factors | |
| Why not detected earlier | |
| Category | Source system defect / Transformation defect / Reference data / Process gap / Interface change / Human error / Unknown |

**Consumer impact**

| Consumer | Impact | Notified | Their action |
| --- | --- | --- | --- |
| | | | |

**Guidance for consumers** *(what a reader querying the affected data should do)*

> e.g. "Order lines created between 2026-03-01 and 2026-04-12 with `hold_cd = 'CR09'` have a
> null `hold_release_dt`. Treat these as released on `dispatch_dt`. Corrected values will be
> backfilled by 2026-10-15."

**Containment** *(stop it getting worse)*

| Action | Owner | Date | Status |
| --- | --- | --- | --- |

**Remediation** *(fix the affected data)*

| Aspect | Detail |
| --- | --- |
| Approach | Backfill / Restate / Recalculate / Accept / Not possible |
| Scope | |
| Method | |
| Verification | |
| Downstream reprocessing required | |
| Consumers requiring restatement | |
| Completed | |

**Prevention** *(stop it recurring)*

| Action | Type | Owner | Target | Status |
| --- | --- | --- | --- | --- |
| | Code fix / New DQ rule / Process change / Contract change / Monitoring | | | |

> An issue closed after remediation without prevention will recur. The log should show
> prevention actions for every closed issue, or an explicit acceptance of recurrence risk.

**Timeline**

| Date | Event |
| --- | --- |
| | |

---

## 4. Closed issues

> Retained permanently. Historical data carries the consequences of defects long after the
> cause is fixed, and a reader querying an affected period needs this.

| ID | Title | Severity | Detected | Closed | Days open | Period affected | Data corrected | Recurred |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | Yes/No/Partial | |

**Permanently uncorrected data**

> Defects where the data was never fixed. The most important table in this document for
> anyone analysing historical data.

| Issue | Period | Element | Nature of the defect | Guidance for analysts |
| --- | --- | --- | --- | --- |
| | | | | |

---

## 5. Recurring issues

| Pattern | Occurrences | Issues | Systemic cause | Structural fix | Owner |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 6. Analysis

**By root cause category**

| Category | Count | % | Trend |
| --- | --- | --- | --- |
| Source system defect | | | |
| Transformation defect | | | |
| Reference data | | | |
| Process gap | | | |
| Interface change | | | |
| Human error | | | |
| Unknown | | | |

**By detection method**

| Method | Count | Avg. time to detect |
| --- | --- | --- |
| Automated DQ rule | | |
| Reconciliation control | | |
| Consumer report | | |
| Incident | | |
| Audit | | |
| Chance | | |

> A high proportion of issues found by consumers or by chance means detective controls are
> insufficient — that comparison is more actionable than the raw issue count, and it should
> drive where new DQ rules go.

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
