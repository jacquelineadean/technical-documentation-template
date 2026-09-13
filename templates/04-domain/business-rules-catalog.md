---
doc_id: BRC-<SCOPE>-001
title: <Domain Name> — Business Rules Catalog
doc_type: brc
status: draft
version: 0.1.0
owner: <Domain Product Owner role>
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: semi-annual
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [DOM-<SCOPE>-001]
downstream_docs: []
tags: [rules]
---

# \<Domain Name\> — Business Rules Catalog

> **Purpose.** Every business rule in the domain, individually identified, atomic, testable,
> and attributed to a source of authority.
>
> **Why identifiers matter.** A rule ID lets a test case cite the rule it verifies, a code
> comment cite the rule it implements, an impact assessment enumerate what a change touches,
> and a support engineer explain to a dealer exactly why their order was held. Without IDs
> none of that is possible, and the rules exist only in code.
>
> **IDs are immutable and never reused.** A retired rule keeps its ID with
> `status: retired`; the next rule takes the next number.

---

## Contents

| Section | Summary |
| --- | --- |
| [1. Summary](#1-summary) | Active, retired, and unattributed rule counts, with confidence breakdown |
| [2. Categories](#2-categories) | Rule categories, their purposes, and allocated ID ranges |
| [3. Rule register](#3-rule-register) | One row per rule: condition, outcome, authority, implementation, volatility |
| [4. Rule detail](#4-rule-detail) | Full blocks for complex, contested, or financially significant rules |
| [5. Decision tables](#5-decision-tables) | Condition combinations as decision tables, which make gaps visible |
| [6. Rule precedence](#6-rule-precedence) | Which rule wins on conflict, and whether that is by design or execution order |
| [7. Rules by implementation mechanism](#7-rules-by-implementation-mechanism) | Rules grouped by mechanism, with change lead time and approval |
| [8. Retired rules](#8-retired-rules) | Retired rules, retained because historical data was produced under them |
| [9. Unattributed rules ⚠️](#9-unattributed-rules-) | Rules found in code with no identifiable authority — highest risk in the catalog |
| [10. Rule change log](#10-rule-change-log) | Per-rule changes with effective date and historical data affected |
| [Change log](#change-log) | Version, date, author, change |

---

## 1. Summary

| | Count |
| --- | --- |
| Active rules | |
| Retired rules | |
| Rules implemented in code | |
| Rules implemented in configuration/reference data | |
| Rules enforced manually | |
| Rules with `✅ Verified` confidence | |
| Rules with `🔴 Assumed` confidence | |
| Rules with no identified authority | |

---

## 2. Categories

| Category | Purpose | Rule range | Count |
| --- | --- | --- | --- |
| Validation | Is this input acceptable? | BR-…-0xx | |
| Derivation | What value does this produce? | BR-…-1xx | |
| Eligibility | Does this qualify? | BR-…-2xx | |
| Routing | Where does this go next? | BR-…-3xx | |
| Authorisation | Who may do this? | BR-…-4xx | |
| Timing | When must this happen? | BR-…-5xx | |
| Constraint | What must always hold? | BR-…-6xx | |

---

## 3. Rule register

| ID | Name | Category | Condition | Outcome | Authority | Implemented in | Volatility | Status | Conf |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BR-…-001 | | | | | | | | Active / Retired | ✅/🟡/🔴 |

---

## 4. Rule detail

> Use a full block for any rule that is complex, contested, financially significant, or
> frequently asked about. Simple rules can live in the register alone.

### BR-\<SCOPE\>-\<NNN\>: \<name\>

| | |
| --- | --- |
| Category | |
| Status | Active / Superseded / Retired |
| Effective from | |
| Effective to | |
| Supersedes / superseded by | |
| Authority | *(policy document + clause, regulation, contract, or "unknown — inferred from code")* |
| Owner | |
| Volatility | |
| Confidence | ✅/🟡/🔴 |
| Evidence | *(code reference with release, query result, test)* |

**Statement**

> **When** \<condition\>
> **Then** \<outcome\>
> **Because** \<business rationale\>

**Condition detail**

| Input | Source | Condition |
| --- | --- | --- |
| | | |

**Outcome detail**

| Effect | Detail |
| --- | --- |
| Data change | |
| State change | |
| Notification | |
| Downstream effect | |

**Exceptions and overrides**

| Exception | Condition | Who may apply | Approval | Logged |
| --- | --- | --- | --- | --- |
| | | | | |

**Interaction with other rules**

| Rule | Relationship | Precedence |
| --- | --- | --- |
| | Depends on / Conflicts with / Supersedes / Composed with | |

**Implementation**

| Aspect | Detail |
| --- | --- |
| Where | *(component + module/program + lines, at a stated release)* |
| Mechanism | Code / Configuration / Reference data / Database constraint / Manual |
| Change lead time | |
| Test coverage | *(test case IDs)* |

**Examples**

| # | Input | Expected outcome | Notes |
| --- | --- | --- | --- |
| 1 | | | Positive case |
| 2 | | | Negative case |
| 3 | | | Boundary |
| 4 | | | Exception |

> Boundary examples are the ones that matter. "Orders over USD 50,000 require approval"
> leaves exactly USD 50,000.00 undefined, and that is the case that will be disputed.

---

## 5. Decision tables

> Where several conditions combine, a decision table is clearer and more checkable than
> prose — and it makes gaps visible.

### DT-\<NN\>: \<name\>

| # | \<Condition 1\> | \<Condition 2\> | \<Condition 3\> | Outcome | Rule |
| --- | --- | --- | --- | --- | --- |
| 1 | Y | Y | Y | | BR-… |
| 2 | Y | Y | N | | BR-… |
| 3 | Y | N | — | | BR-… |
| 4 | N | — | — | | BR-… |

**Completeness check**

| Check | Result |
| --- | --- |
| All condition combinations covered | ✅/❌ |
| No two rows produce conflicting outcomes for the same input | ✅/❌ |
| Default/fallback row present | ✅/❌ |

> Run these checks explicitly. Uncovered combinations are exactly where production defects
> occur, and they are trivial to spot in a table and invisible in prose.

---

## 6. Rule precedence

> When rules conflict, which wins? Legacy systems usually resolve this by order of execution
> rather than by any stated principle — record what actually happens.

| Conflict | Rules | Precedence | Basis | Confidence |
| --- | --- | --- | --- | --- |
| | | | *(explicit design / order of execution / undefined)* | |

**Undefined precedence** *(conflicts with no established resolution — each is a latent
defect)*

| Conflict | Rules | Observed behaviour | Risk | Owner |
| --- | --- | --- | --- | --- |
| | | | | |

---

## 7. Rules by implementation mechanism

| Mechanism | Rules | Change lead time | Change approval | Risk |
| --- | --- | --- | --- | --- |
| Compiled code | | | | |
| Configuration | | | | |
| Reference data | | | | *(changes behaviour with no release — often outside change control)* |
| Database constraint | | | | |
| Manual procedure | | | | *(enforcement depends on a person remembering)* |

---

## 8. Retired rules

> Retained permanently. Historical data was produced under these rules, and anyone analysing
> it needs to know what they were.

| ID | Name | Effective from | Retired | Reason | Replaced by | Historical impact |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

---

## 9. Unattributed rules ⚠️

> Rules found in the implementation with no identifiable authority. These are the highest
> risk in the catalog: nobody knows why they exist, so nobody can safely decide whether to
> keep them. Each needs an owner and an investigation.

| ID | Rule | Found in | First appeared | Investigation | Owner | Target |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

---

## 10. Rule change log

| Date | Rule | Change | Reason | Approved by | Effective | Historical data affected |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
