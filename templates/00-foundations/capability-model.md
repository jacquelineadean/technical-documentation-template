---
doc_id: CAP-<SCOPE>-001
title: <System Name> — Capability Model
doc_type: cap
status: draft
version: 0.1.0
owner: <Role>
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: annual
classification: internal
systems: [<SYSTEM_CODE>]
domains: [cross-domain]
upstream_docs: [SYS-<SCOPE>-001]
downstream_docs: []
tags: []
---

# \<System Name\> — Capability Model

> **Purpose.** Describe *what* the system does in business terms, decomposed to a level a
> business stakeholder recognises and an engineer can map to components. Capabilities are
> stable; implementations are not. That stability is what makes this document the right
> place to hang ownership, criticality, and modernization decisions.
>
> **Rule:** a capability is a noun phrase describing an ability ("Order Line Decoding"),
> never a system, team, or process step.

---

## 1. Capability map

```mermaid
flowchart TD
    subgraph L1A["<b><Capability Area 1></b>"]
        A1["<Capability 1.1>"]
        A2["<Capability 1.2>"]
        A3["<Capability 1.3>"]
    end
    subgraph L1B["<b><Capability Area 2></b>"]
        B1["<Capability 2.1>"]
        B2["<Capability 2.2>"]
    end
    subgraph L1C["<b><Capability Area 3></b>"]
        C1["<Capability 3.1>"]
        C2["<Capability 3.2>"]
    end
    subgraph SUP["<b>Supporting</b>"]
        S1["Reference Data Management"]
        S2["Audit &amp; Traceability"]
    end

    A1 --> B1
    B1 --> C1
    S1 -.->|"enables"| A1
    S1 -.->|"enables"| B1

    classDef internal fill:#E8F0FE,stroke:#1A73E8,color:#0B1F3A
    classDef manual fill:#F1F3F4,stroke:#5F6368,color:#202124
    class A1,A2,A3,B1,B2,C1,C2 internal
    class S1,S2 manual
```

---

## 2. Capability register

> One row per capability. `Maturity` and `Disposition` are what make this document useful
> for planning rather than merely descriptive.

| ID | Capability | Area | Description | Owning domain | Primary components | Criticality | Maturity | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAP-01 | | | | | | Tier 1/2/3 | 1–5 | Invest / Sustain / Contain / Retire |
| CAP-02 | | | | | | | | |

**Maturity scale**

| Level | Meaning |
| --- | --- |
| 1 | Manual or heavily workaround-dependent |
| 2 | Automated but fragile; frequent exceptions requiring human intervention |
| 3 | Automated and stable; poor observability or slow to change |
| 4 | Automated, observable, changeable within a normal release cycle |
| 5 | Automated, observable, self-service configurable by the business |

> Maturity 1–2 capabilities are where operational cost hides. Quantify it: "≈ 2.5 FTE of
> manual correction per month" is an argument; "needs improvement" is not.

---

## 3. Capability → component mapping

> The bridge between business language and the TAD. Keeps modernization conversations
> honest: it shows which capabilities are entangled in the same component and therefore
> cannot be moved independently.

| Capability | Components | Shared with | Separable? | Notes |
| --- | --- | --- | --- | --- |
| CAP-01 | | | Yes / No / Partial | |

---

## 4. Capability heat map

> Plot criticality against maturity. The top-left quadrant — critical and immature — is the
> risk register for this system, and the modernization roadmap should open with it.

| Capability | Criticality (1–5) | Maturity (1–5) | Change frequency | Risk score | Priority |
| --- | --- | --- | --- | --- | --- |
| | | | High/Med/Low | *(criticality × (6 − maturity))* | |

```mermaid
quadrantChart
    title Capability risk — criticality vs. maturity
    x-axis "Low maturity" --> "High maturity"
    y-axis "Low criticality" --> "High criticality"
    quadrant-1 "Healthy core"
    quadrant-2 "Fix first"
    quadrant-3 "Tolerate"
    quadrant-4 "Over-invested"
    "<Capability A>": [0.2, 0.9]
    "<Capability B>": [0.7, 0.8]
    "<Capability C>": [0.3, 0.3]
```

---

## 5. Cross-domain capabilities

> Capabilities used by more than one domain are the most contentious things in a
> disaggregated system: everyone depends on them, nobody funds them. Name the accountable
> owner explicitly.

| Capability | Consuming domains | Accountable owner | Funding model | Contention notes |
| --- | --- | --- | --- | --- |
| | | | | |

---

## 6. Gaps and duplication

| Finding | Type | Evidence | Impact | Owner |
| --- | --- | --- | --- | --- |
| | Gap / Duplication / Shadow IT | | | |

> "Shadow IT" here means a capability the business has built outside the system — the
> spreadsheet that reconciles two reports, the Access database that tracks exceptions. These
> are capability gaps with a workaround attached, and they belong in this document rather
> than being ignored because they are not "the system".

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
