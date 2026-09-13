---
doc_id: DDC-<SCOPE>-001
title: <Data Domain Name> — Data Domain Charter
doc_type: ddc
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
upstream_docs: [DGC-<SCOPE>-001]
downstream_docs: []
tags: [governance, data, domain]
---

# \<Data Domain Name\> — Data Domain Charter

> **Purpose.** Define one data domain's scope, ownership, authoritative sources, quality
> commitments, and obligations to other domains. The governance charter sets the operating
> model; this applies it to one domain and makes its commitments concrete.

---

## Contents

| Section | Summary |
| --- | --- |
| [1. Domain definition](#1-domain-definition) | Domain name, code, business purpose, boundaries |
| [2. Ownership](#2-ownership) | Data Owner, Steward, and Custodian, with what each is accountable for |
| [3. Authoritative sources](#3-authoritative-sources) | One authoritative source per entity, and the currency of approved copies |
| [4. Data assets](#4-data-assets) | Assets by type, location, volume, classification, CDEs |
| [5. Obligations to other domains](#5-obligations-to-other-domains) | What this domain commits to provide to other domains |
| [6. Dependencies on other domains](#6-dependencies-on-other-domains) | What this domain consumes, and its behaviour when a provider is unavailable |
| [7. Shared and delegated data](#7-shared-and-delegated-data) | Fields defined by one domain and stored by another; dual change approval |
| [8. Quality commitments](#8-quality-commitments) | CDE targets, current values, breach actions, exceptions in force |
| [9. Access](#9-access) | Access classes, approval, review cadence |
| [10. Retention and lifecycle](#10-retention-and-lifecycle) | Retention per asset, basis, purge process, verification |
| [11. Domain risks](#11-domain-risks) | Domain risks with impact, likelihood, mitigation, owner |
| [12. Improvement plan](#12-improvement-plan) | Improvements with driver, effort, priority, target |
| [Change log](#change-log) | Version, date, author, change |

---

## 1. Domain definition

| | |
| --- | --- |
| Domain name | |
| Domain code | |
| Business purpose | |
| Aligned business function | |
| Aligned bounded context | |

**In scope**

| Data category | Entities | Systems |
| --- | --- | --- |
| | | |

**Out of scope** *(adjacent data this domain does not own, and who does)*

| Data | Owned by | Why the boundary sits here |
| --- | --- | --- |
| | | |

---

## 2. Ownership

| Role | Holder (role name) | Accountable for |
| --- | --- | --- |
| Data Owner | | Meaning, access decisions, quality targets |
| Data Steward | | Definitions, DQ triage, remediation |
| Data Custodian | | Storage, controls, retention execution |
| Domain Architect | | Model coherence |

**Deputies and coverage**

| Role | Deputy | Coverage arrangement |
| --- | --- | --- |
| | | |

---

## 3. Authoritative sources

> For every entity the domain owns, exactly one authoritative source. Where a copy is used
> by consumers, say so and state its currency.

| Entity | Authoritative source | Why authoritative | Approved copies | Copy currency |
| --- | --- | --- | --- | --- |
| | | | | |

**Contested sources** *(where more than one system claims authority — the most valuable rows
in this document)*

| Entity | Claimants | Current de facto source | Decision needed | Owner | Target |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 4. Data assets

| Asset | Type | Physical location | Records | Growth | Classification | CDEs | Dictionary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | Master / Transactional / Reference / Derived / Archive | | | | | | |

---

## 5. Obligations to other domains

> What this domain commits to provide. These commitments should be reflected in data
> contracts where the consumer's dependency is material.

| Consumer domain | Data provided | Mechanism | Frequency | Quality commitment | Availability commitment | Contract |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | DCT-… |

## 6. Dependencies on other domains

| Provider domain | Data consumed | Mechanism | Criticality | Behaviour if unavailable | Contract |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 7. Shared and delegated data

| Element | Physical home | Defining domain | Populated by | Consumed by | Change approval |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

> Where this domain's tables carry fields defined by another domain — or vice versa — every
> change needs both Data Owners. Legacy shared schemas make this common; naming it makes it
> manageable.

---

## 8. Quality commitments

| CDE | Dimension | Target | Current | Measurement | Breach action |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

**Quality exceptions in force**

| Exception | Element | Reason | Compensating control | Approved by | Expires |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 9. Access

| Access class | Who | Data | Approval | Review cadence |
| --- | --- | --- | --- | --- |
| Read — internal | | | | |
| Read — confidential | | | | |
| Write | | | | |
| Bulk export | | | | |
| External sharing | | | | |

**Standing grants**

| Grantee | Scope | Granted | Purpose | Last recertified | Expires |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 10. Retention and lifecycle

| Asset | Active retention | Archive | Total | Basis | Purge process | Verified |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

---

## 11. Domain risks

| ID | Risk | Impact | Likelihood | Mitigation | Owner |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 12. Improvement plan

| ID | Item | Driver | Effort | Priority | Owner | Target |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
