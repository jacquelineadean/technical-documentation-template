---
doc_id: IMP-<SCOPE>-001
title: <Change Name> — Impact Assessment
doc_type: imp
status: draft
version: 0.1.0
owner: <Delivery Lead role>
created: <YYYY-MM-DD>
review_cycle: on-change
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [BRD-<SCOPE>-001]
downstream_docs: []
tags: [change, impact]
---

# \<Change Name\> — Impact Assessment

> **Purpose.** Establish the blast radius of a proposed change before committing to it, and
> enumerate every document, test, and party that must be updated or told.
>
> **Start mechanically, then apply judgement.** Traverse the documentation dependency graph
> first:
>
> ```bash
> python3 tools/validate_docs.py . --impact <DOC-ID>
> ```
>
> That gives you the documents your change invalidates. It will not give you the report
> somebody built in a spreadsheet, the partner whose parser is stricter than the spec, or
> the batch job that depends on an implicit ordering. Those are what the rest of this
> document is for.

---

## Contents

| Section | Summary |
| --- | --- |
| [1. Change summary](#1-change-summary) | Change, driver, source, and proposed timing |
| [2. Mechanical traversal](#2-mechanical-traversal) | Documents reached by traversing the dependency graph — the mechanical floor |
| [3. Component impact](#3-component-impact) | Components affected directly and indirectly, with effort and regression scope |
| [4. Data impact](#4-data-impact) | New, modified, and retired data elements; migration and historical comparability |
| [5. Interface impact](#5-interface-impact) | Interfaces affected, breaking changes, notice periods, counterparty lead times |
| [6. Process and rules impact](#6-process-and-rules-impact) | Processes and business rules affected, with retraining and catalog updates |
| [7. Batch and scheduling impact](#7-batch-and-scheduling-impact) | Jobs affected, duration and dependency changes, and window slack before and after |
| [8. Reporting impact](#8-reporting-impact) | Reports, metric comparability, series breaks, and shadow reporting |
| [9. Non-functional impact](#9-non-functional-impact) | Projected effect on latency, throughput, and other quality attributes |
| [10. Security, privacy, compliance](#10-security-privacy-compliance) | Classification, personal data, and compliance assessments triggered |
| [11. Operational impact](#11-operational-impact) | Runbooks, monitoring, alerting, support model, capacity |
| [12. Reversibility](#12-reversibility) | Whether the change is reversible, and the rollback window |
| [13. Test scope](#13-test-scope) | Test scope derived from the impact above, not chosen independently |
| [14. Documents to update](#14-documents-to-update) | Documents to update, and whether before, with, or after release |
| [15. Risks](#15-risks) | Risks with likelihood, impact, mitigation, owner |
| [16. Summary](#16-summary) | Overall complexity and the count of elements affected |
| [Change log](#change-log) | Version, date, author, change |

---

## 1. Change summary

| | |
| --- | --- |
| Change | |
| Driver | |
| Source | *(BRD, incident, regulatory, technical debt)* |
| Proposed by | |
| Target release | |
| Assessed by | |
| Date | |

**What is changing**

| Element | Change | Rationale |
| --- | --- | --- |
| | | |

---

## 2. Mechanical traversal

| Document | Relationship | Change required | Owner | Effort |
| --- | --- | --- | --- | --- |
| | Direct downstream / Transitive | | | |

---

## 3. Component impact

| Component | Impact | Change type | Owning team | Effort | Risk | Regression scope |
| --- | --- | --- | --- | --- | --- | --- |
| | Direct / Indirect / None-but-verify | Code / Config / Data / Schedule | | | | |

---

## 4. Data impact

| Aspect | Impact |
| --- | --- |
| New data elements | |
| Modified data elements | |
| Retired data elements | |
| Schema changes | |
| Volume changes | |
| Migration required | |
| Backfill required | |

**Historical data** ⚠️

| Question | Answer |
| --- | --- |
| Does this change the meaning of existing data? | |
| Are historical records still interpretable under the new rules? | |
| Is reprocessing of historical data required? | |
| Are historical reports still reproducible? | |
| Is a break in series introduced? | |
| Do reference data changes need effective dating? | |

> This block catches the most expensive class of change: one that is straightforward
> prospectively and silently invalidates years of history. A field whose meaning changes
> without its name changing will pass every test and break every trend report.

**Lineage impact**

| Lineage | Hops affected | Consumers | Update required |
| --- | --- | --- | --- |
| | | | |

**Data quality impact**

| Rule | Affected | Threshold change | Action |
| --- | --- | --- | --- |
| | | | |

---

## 5. Interface impact

| IF ID | Counterparty | Change | Breaking | Notice required | Notice period | Their lead time | Coordination |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | Yes/No | | | | |

**External party notification**

| Party | Interfaces | Notice period | Notify by | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

> Work backwards from the go-live date through each counterparty's notice period and lead
> time. A 90-day contractual notice discovered during UAT is a schedule failure, and this
> table is where it should be found instead.

---

## 6. Process and rules impact

| Process | Impact | Steps affected | Retraining needed | Owner |
| --- | --- | --- | --- | --- |
| | | | | |

| Rule | Change | Effective date | Historical rules retained | Catalog update |
| --- | --- | --- | --- | --- |
| BR-… | New / Modified / Retired | | | |

| Entity | State model change | Migration of in-flight items | Owner |
| --- | --- | --- | --- |
| | | *(what happens to entities currently in a state that no longer exists?)* | |

---

## 7. Batch and scheduling impact

| Job | Impact | Duration change | Dependency change | Window impact | Critical path affected |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

**Window analysis**

| Chain | Current p95 | Projected p95 | Window | Slack before | Slack after | Acceptable |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

---

## 8. Reporting impact

| Report / dashboard | Owner | Impact | Change required | Break in series | Communication |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

| Metric | Definition change | Comparability | Catalog update | Consumers to notify |
| --- | --- | --- | --- | --- |
| | | | | |

**Shadow reporting** — spreadsheets and local extracts built on the data you are changing.
They are invisible to every automated analysis and their owners will be affected regardless.

| Known shadow report | Owner | Impact | How identified |
| --- | --- | --- | --- |
| | | | |

---

## 9. Non-functional impact

| Attribute | Current | Projected | Acceptable | Mitigation |
| --- | --- | --- | --- | --- |
| Latency | | | | |
| Throughput | | | | |
| Batch window | | | | |
| Storage | | | | |
| Availability | | | | |
| Cost | | | | |

---

## 10. Security, privacy, compliance

| Aspect | Impact | Assessment required | Owner |
| --- | --- | --- | --- |
| New data classification | | | |
| Personal data | | | |
| Access model | | | |
| Audit trail | | | |
| Retention | | | |
| Regulatory reporting | | | |
| Controls affected | | | |

---

## 11. Operational impact

| Aspect | Impact | Action | Owner |
| --- | --- | --- | --- |
| Runbooks | | | |
| Monitoring and alerts | | | |
| DR plan | | | |
| Support model | | | |
| Capacity | | | |
| Training | | | |

---

## 12. Reversibility

| Aspect | Assessment |
| --- | --- |
| Reversible after deployment | Yes / No / Time-limited |
| Rollback window | |
| Point of no return | |
| Data written that the old version cannot read | |
| External transmissions that cannot be recalled | |
| Rollback procedure | |
| Rollback tested | |

---

## 13. Test scope

> Derived from the impact above, not chosen independently. Every impacted element should
> map to a test.

| Area | Scope | Type | Environment | Data | Owner |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

**Regression scope**

| Area | Rationale | Depth |
| --- | --- | --- |
| | | Full / Targeted / Smoke |

---

## 14. Documents to update

| Document | Owner | Change | When | Status |
| --- | --- | --- | --- | --- |
| | | | Before / With / After release | |

> Documentation updates land **with** the change, not after. "Docs to follow" is the
> mechanism by which a documentation corpus dies.

---

## 15. Risks

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 16. Summary

| Dimension | Assessment |
| --- | --- |
| Overall complexity | Low / Medium / High |
| Components affected | |
| Interfaces affected | |
| External parties requiring notice | |
| Documents to update | |
| Estimated effort | |
| Longest lead time | |
| Recommended change class | |
| Key risk | |

**Recommendation**

| | |
| --- | --- |
| Proceed | Yes / Yes with conditions / No |
| Conditions | |
| Prerequisites | |

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
