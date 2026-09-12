---
doc_id: MDM-<SCOPE>-001
title: <Master Entity> — Master Data Management
doc_type: mdm
status: draft
version: 0.1.0
owner: <Data Owner role>
approvers: []
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: semi-annual
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [DGC-<SCOPE>-001, CDM-<SCOPE>-001]
downstream_docs: []
tags: [mdm, master-data]
---

# \<Master Entity\> — Master Data Management

> **Purpose.** How one master entity — dealer, product, vendor, customer, location — is
> created, matched, merged, and distributed across systems that each hold their own copy.
>
> One document per master entity. The rules for products and for trading partners are
> different enough that combining them produces a document that fits neither.

---

## 1. Entity

| | |
| --- | --- |
| Master entity | |
| Business definition | |
| Identity criterion | *(what makes two records the same real-world thing)* |
| Record count | |
| Create/change rate | |
| Business criticality | |
| Data Owner | |
| Data Steward | |

---

## 2. Source landscape

```mermaid
flowchart LR
    S1["<Source 1><br/><i>authoritative for: ...</i>"]
    S2["<Source 2><br/><i>authoritative for: ...</i>"]
    S3["<Source 3>"]
    HUB[("<b>Master hub</b><br/>golden records")]
    C1["<Consumer 1>"]
    C2["<Consumer 2>"]

    S1 -->|"<sync mode>"| HUB
    S2 -->|"<sync mode>"| HUB
    S3 -->|"<sync mode>"| HUB
    HUB -->|"<distribution>"| C1
    HUB -->|"<distribution>"| C2

    classDef internal fill:#E8F0FE,stroke:#1A73E8,color:#0B1F3A
    classDef datastore fill:#E6F4EA,stroke:#137333,color:#0B2E16
    class S1,S2,S3,C1,C2 internal
    class HUB datastore
```

| Source | Records | Authoritative for | Sync | Latency | Quality | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| | | *(which attributes)* | | | | |

**Style**

| | |
| --- | --- |
| MDM style | Registry / Consolidation / Coexistence / Centralised |
| Rationale | |
| Where records are created | |
| Where records are edited | |
| Propagation model | Push / Pull / Both |
| Propagation latency | |

---

## 3. Identity and matching

| Aspect | Approach |
| --- | --- |
| Master identifier | |
| Identifier format | |
| Identifier assignment | |
| Identifier reuse | **Prohibited** / *(if permitted, document the historical ambiguity it creates)* |
| Cross-reference storage | |

**Match rules**

| Rule | Attributes | Type | Threshold | Action | Confidence |
| --- | --- | --- | --- | --- | --- |
| M-01 | | Exact / Fuzzy / Probabilistic | | Auto-merge / Queue for review / No match | |

**Match outcomes**

| Score band | Action | Volume/month | Review SLA |
| --- | --- | --- | --- |
| ≥ \<auto\> | Auto-merge | | — |
| \<review\>–\<auto\> | Steward review | | |
| < \<review\> | Treat as distinct | | — |

> Set the auto-merge threshold conservatively. A false merge is far more expensive than a
> false non-merge: merging two real dealers combines their orders, credit limits, and
> incentive attainment, and unpicking it after downstream consumption may be impossible.

---

## 4. Survivorship

> Which source's value wins, per attribute. Do not apply one global rule — recency is right
> for contact details and wrong for a legally registered name.

| Attribute | Rule | Priority order | Rationale |
| --- | --- | --- | --- |
| | Source priority / Most recent / Most complete / Most trusted / Manual | | |

**Conflict handling**

| Situation | Handling |
| --- | --- |
| Two sources disagree, both trusted | |
| Authoritative source has a null | |
| Source provides an invalid value | |
| A manual override exists | *(state whether a later source update overwrites it — the answer must be "no" or overrides are pointless)* |

---

## 5. Golden record

| Attribute | Type | Source | Survivorship | Required | Validation |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

**Lineage of a golden record** — every attribute retains its contributing source and
timestamp, so a consumer can ask "where did this value come from?" without re-running the
match.

| Metadata | Purpose |
| --- | --- |
| `source_system` | Contributing source per attribute |
| `source_record_id` | |
| `last_updated` / `updated_by` | |
| `match_confidence` | |
| `merge_history` | Records previously merged into this one |
| `manual_override_flag` | Per attribute |

---

## 6. Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Pending: created in a source
    Pending --> Matched: match rule hit
    Pending --> New: no match
    Matched --> UnderReview: score in review band
    UnderReview --> Merged: steward confirms
    UnderReview --> New: steward rejects match
    New --> Active: validation passed
    Merged --> Active
    Active --> Suspended: <business condition>
    Suspended --> Active: condition cleared
    Active --> Inactive: no activity for <period>
    Inactive --> Active: reactivated
    Active --> Superseded: merged into another
    Superseded --> [*]
    Inactive --> Archived: retention reached
    Archived --> [*]
```

| State | Meaning | Who may change | Downstream effect |
| --- | --- | --- | --- |
| | | | |

**Deactivation and deletion**

| Aspect | Rule |
| --- | --- |
| Deactivation criteria | |
| Effect on historical transactions | *(must remain resolvable — never hard-delete a master record referenced by history)* |
| Hard deletion permitted | |
| Regulatory erasure handling | |

---

## 7. Stewardship

| Task | Trigger | Owner | SLA | Volume/month |
| --- | --- | --- | --- | --- |
| Review a probable match | | | | |
| Resolve a survivorship conflict | | | | |
| Investigate a duplicate report | | | | |
| Unmerge an incorrect merge | | | | |
| Approve a new record | | | | |
| Recertify inactive records | | | | |

**Unmerge**

| Aspect | Approach |
| --- | --- |
| Supported | Yes/No |
| Procedure | |
| Effect on downstream transactions created against the merged ID | |
| Approval required | |

> If unmerge is not supported, say so prominently — it makes the auto-merge threshold a
> one-way decision and should push it higher.

---

## 8. Distribution

| Consumer | Method | Frequency | Latency | Subset | Behaviour on unknown ID |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

**Change notification**

| Change | Consumers notified | Method | Latency |
| --- | --- | --- | --- |
| New record | | | |
| Attribute change | | | |
| Merge | | | |
| Deactivation | | | |

> **Merges must be notified explicitly.** A consumer holding transactions against a
> superseded identifier needs to know it has been merged, or their reporting silently loses
> the merged entity's history.

---

## 9. Quality

| Metric | Definition | Target | Current |
| --- | --- | --- | --- |
| Duplicate rate | | | |
| Match precision | | | |
| Match recall | | | |
| Completeness of required attributes | | | |
| Records pending review | | | |
| Average age of pending review | | | |
| Manual override rate | | | |

---

## 10. Known issues

| ID | Issue | Impact | Workaround | Remediation | Owner |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
