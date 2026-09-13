---
doc_id: RTM-<SCOPE>-001
title: <Initiative Name> — Requirements Traceability Matrix
doc_type: rtm
status: draft
version: 0.1.0
owner: <QA Lead role>
created: <YYYY-MM-DD>
review_cycle: on-change
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [BRD-<SCOPE>-001, FSP-<SCOPE>-001]
downstream_docs: []
tags: [traceability, qa]
---

# \<Initiative Name\> — Requirements Traceability Matrix

> **Purpose.** One grid connecting requirement → design → implementation → test → evidence.
> It answers two questions that are otherwise expensive: *is everything we agreed to build
> actually built and tested?* and *if this breaks, what business requirement is affected?*
>
> Keep it generated or maintained mechanically where possible. A hand-maintained matrix in a
> long project drifts, and a drifted matrix is worse than none because it is trusted.

---

## 1. Coverage summary

| | Count | % |
| --- | --- | --- |
| Requirements — total | | |
| With a design element | | |
| With an implementation | | |
| With at least one test | | |
| With a passing test | | |
| Accepted by the business | | |
| **Orphaned** *(no requirement)* | | |
| **Uncovered** *(no test)* | | |

| Priority | Total | Designed | Implemented | Tested | Passing | Accepted |
| --- | --- | --- | --- | --- | --- | --- |
| Must | | | | | | |
| Should | | | | | | |
| Could | | | | | | |

---

## 2. Matrix

| Req ID | Requirement | Priority | Design | Rules | Components | Interfaces | Test cases | Status | Evidence | Accepted |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BR-001 | | Must | HLD §… | BR-… | | IF-… | TC-… | Pass / Fail / Not run | | ✅/❌ |

---

## 3. Reverse traceability

> From implementation back to requirement. Finds **orphaned work** — things built that
> nobody asked for, which are usually either scope creep or an undocumented requirement.
> Both are worth knowing about.

| Component / change | Requirement | Justification if none |
| --- | --- | --- |
| | | |

---

## 4. Test coverage

| Req ID | Unit | Integration | Interface | Performance | Security | UAT | Regression |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | ✅/❌/NA | | | | | | |

**Uncovered requirements**

| Req ID | Priority | Why uncovered | Risk | Mitigation | Owner |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 5. NFR traceability

| NFR ID | Requirement | Design response | Verification | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 6. Business rule traceability

| Rule | Requirement | Implemented in | Test cases | Verified | Catalogued |
| --- | --- | --- | --- | --- | --- |
| BR-… | | | | | ✅/❌ |

---

## 7. Interface traceability

| IF ID | Requirement | ICD | Implemented | Certified | Counterparty signed off |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 8. Data traceability

| Data element | Requirement | Dictionary | Lineage | DQ rules | Classified |
| --- | --- | --- | --- | --- | --- |
| | | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

---

## 9. Compliance traceability

| Obligation | Source | Requirement | Control | Test | Evidence |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 10. Defects

| Defect | Requirement | Test | Severity | Status | Resolution |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 11. Change control

| Date | Requirement | Change | Reason | Impact on traceability | Approved by |
| --- | --- | --- | --- | --- | --- |
| | | Added / Modified / Removed / Deferred | | | |

---

## 12. Sign-off

| Requirement set | Tested by | Date | Accepted by | Date | Conditions |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
