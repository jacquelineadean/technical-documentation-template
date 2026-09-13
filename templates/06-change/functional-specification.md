---
doc_id: FSP-<SCOPE>-001
title: <Feature Name> — Functional Specification
doc_type: fsp
status: draft
version: 0.1.0
owner: <Product Owner role>
approvers: []
created: <YYYY-MM-DD>
review_cycle: on-change
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [BRD-<SCOPE>-001, HLD-<SCOPE>-001]
downstream_docs: []
related_rules: []
tags: [requirements, functional]
---

# \<Feature Name\> — Functional Specification

> **Purpose.** The behaviour to be built, in enough detail to implement and test. The BRD
> says what the business needs; this says what the system will do.
>
> **Completeness test:** for every input a user or system can supply — including malformed,
> missing, duplicate, and out-of-order — this document says what happens. A specification
> that covers only valid input specifies half a system, and the other half gets invented
> during implementation.

---

## 1. Summary

| | |
| --- | --- |
| Feature | |
| Source requirements | |
| Design | |
| Product owner | |
| Target release | |

**Description**

---

## 2. Actors and permissions

| Actor | Can | Cannot | Authorisation |
| --- | --- | --- | --- |
| | | | |

---

## 3. Functional behaviour

### F-\<NNN\>: \<name\>

| | |
| --- | --- |
| Requirement | BR-… |
| Trigger | |
| Actor | |
| Preconditions | |
| Postconditions | |

**Main flow**

| # | Actor | Action | System response |
| --- | --- | --- | --- |
| 1 | | | |

**Alternate flows**

| ID | Condition | Behaviour | Rejoins at |
| --- | --- | --- | --- |
| A-01 | | | |

**Exception flows**

| ID | Condition | Behaviour | User sees | Recoverable |
| --- | --- | --- | --- | --- |
| E-01 | | | | |

**Business rules applied**

| Rule | Applied at | Outcome if violated |
| --- | --- | --- |
| BR-… | | |

**Data effects**

| Entity | Operation | Fields | Conditions |
| --- | --- | --- | --- |
| | Create / Update / Delete / Read | | |

**Events / notifications**

| Event | Trigger | Recipients | Content |
| --- | --- | --- | --- |
| | | | |

---

## 4. Business rules

| ID | Rule | New/Changed | Condition | Outcome | Effective from |
| --- | --- | --- | --- | --- | --- |
| BR-… | | | | | |

Full detail goes in the
[Business Rules Catalog](../04-domain/business-rules-catalog.md) — here, only what is new or
changed by this feature.

---

## 5. Validation

| Field | Rule | Message | Blocking |
| --- | --- | --- | --- |
| | | | |

**Cross-field validation**

| Rule | Condition | Message |
| --- | --- | --- |
| | | |

**Validation order** — matters where one failure masks another. If a user with three
problems must fix them one at a time across three submissions, say so deliberately rather
than by accident.

---

## 6. User interface

> Complete only where the feature has a UI. Screens are described in terms of information
> and actions, not pixels.

### Screen: \<name\>

| Element | Type | Source | Editable | Validation | Notes |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

| Action | Condition to enable | Effect | Confirmation |
| --- | --- | --- | --- |
| | | | |

**States**

| State | Displayed when | Available actions |
| --- | --- | --- |
| Empty | | |
| Loading | | |
| Populated | | |
| Error | | |
| No permission | | |

**Accessibility**

| Requirement | Approach |
| --- | --- |
| | |

---

## 7. Interfaces

| IF ID | Direction | New/Changed | Trigger | Payload changes | ICD |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 8. Batch processing

| Job | New/Changed | Schedule | Input | Output | Duration | Dependencies |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

---

## 9. Reporting

| Report | New/Changed | Contents | Audience | Frequency | Metrics |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 10. Error handling

| Error | Detection | User sees | Logged | Recovery | Support action |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

**Message style**

| Principle | Example |
| --- | --- |
| Say what is wrong | |
| Say what to do about it | |
| Never expose internal detail | |
| Include a reference for support | |

---

## 11. Migration and transition

| Aspect | Approach |
| --- | --- |
| Existing data | |
| In-flight transactions | |
| Parallel operation | |
| Cutover | |
| Backwards compatibility | |

**In-flight handling** — what happens to items mid-process when the feature goes live. The
most frequently omitted section, and the most frequent cause of post-release defects.

| Item state at cutover | Handling |
| --- | --- |
| | |

---

## 12. Configuration

| Setting | Purpose | Default | Who may change | Effect |
| --- | --- | --- | --- | --- |
| | | | | |

---

## 13. Acceptance criteria

| ID | Requirement | Given | When | Then | Test case |
| --- | --- | --- | --- | --- | --- |
| AC-01 | BR-… | | | | |

---

## 14. Out of scope

| Item | Why | Where handled |
| --- | --- | --- |
| | | |

---

## 15. Open questions

| ID | Question | Blocking | Owner | Needed by |
| --- | --- | --- | --- | --- |
| Q-001 | | | | |

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
