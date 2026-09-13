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

## Contents

| Section | Summary |
| --- | --- |
| [1. Coverage summary](#1-coverage-summary) | Requirement counts with design, test, and evidence coverage percentages |
| [2. Matrix](#2-matrix) | Requirement → design → rules → components → interfaces → tests → evidence |
| [3. Reverse traceability](#3-reverse-traceability) | Implementation back to requirement, exposing orphaned work |
| [4. Test coverage](#4-test-coverage) | Test levels covering each requirement, and requirements left uncovered |
| [5. NFR traceability](#5-nfr-traceability) | NFRs to design response, verification method, and result |
| [6. Business rule traceability](#6-business-rule-traceability) | Business rules to requirement, implementation, tests, catalog entry |
| [7. Interface traceability](#7-interface-traceability) | Interfaces to requirement, ICD, certification, counterparty sign-off |
| [8. Data traceability](#8-data-traceability) | Data elements to dictionary, lineage, DQ rules, classification |
| [9. Compliance traceability](#9-compliance-traceability) | Regulatory obligations to controls, tests, and evidence |
| [10. Defects](#10-defects) | Defects linked to requirement and test, with status and resolution |
| [11. Change control](#11-change-control) | Requirements added, modified, removed, or deferred, and the traceability effect |
| [12. Sign-off](#12-sign-off) | Acceptance per requirement set, with conditions |
| [Change log](#change-log) | Version, date, author, change |

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
