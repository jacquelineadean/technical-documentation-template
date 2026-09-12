---
doc_id: GUIDE-007
title: Documentation Glossary
doc_type: guide
status: approved
version: 1.0.0
owner: Documentation Architect
classification: internal
last_reviewed: 2026-09-12
next_review: 2027-09-12
review_cycle: annual
tags: [meta, glossary]
---

# Documentation Glossary

Terms used by **this documentation system**. For business terms belonging to a system you
are documenting, use [`templates/00-foundations/glossary-and-taxonomy.md`](../templates/00-foundations/glossary-and-taxonomy.md)
— do not add domain vocabulary here.

---

## Document types

| Term | Definition |
| --- | --- |
| **ADR** — Architecture Decision Record | A record of one architecturally significant decision: context, options, choice, consequences. Immutable once accepted; superseded rather than edited. |
| **BRD** — Business Requirements Document | States the business problem, desired outcomes, and acceptance criteria. Does not prescribe a solution. |
| **Data Contract** | A binding agreement between a data producer and consumer covering schema, semantics, quality, SLA, and change process. Distinguished from an ICD by being about *data meaning and guarantees* rather than *transport mechanics*. |
| **Domain Pack** | The six domain-layer documents produced together for one bounded context. |
| **HLD** — High-Level Design | Solution shape for one initiative: components affected, data flows, interfaces, major decisions. |
| **ICD** — Interface Control Document | The definitive contract for one interface: payloads, semantics, errors, SLA, versioning, ownership on both sides. |
| **LLD** — Low-Level Design | Implementation-grade detail: schemas, algorithms, class/module structure, error handling. |
| **Runbook** | Executable operational procedure written for someone with no context at 03:00. |
| **TAD** — Technical Architecture Document | The anchor architecture artefact for a system or major subsystem: context, structure, data, interfaces, NFRs, failure modes, constraints, debt. |

## Architecture terms

| Term | Definition |
| --- | --- |
| **Architecturally significant** | A decision is architecturally significant if reversing it later would be expensive, if it affects more than one team, or if it constrains a quality attribute. These get ADRs; others do not. |
| **Blast radius** | The set of components, data, interfaces, and business processes affected when a given thing fails or changes. |
| **Bounded context** | A boundary within which a set of terms has one consistent meaning. The unit of a domain pack. |
| **C4 model** | Context → Container → Component → Code. This repository uses levels 1–3 and deliberately omits level 4. |
| **Critical path** | The longest dependency chain through a batch schedule; determines the earliest possible completion time and therefore where slack does not exist. |
| **Disaggregated system** | A system whose function is spread across many loosely-coupled components, teams, and external parties, with no single place where the whole behaviour is visible. |
| **Quality attribute scenario** | A testable NFR statement: source, stimulus, environment, artefact, response, response measure. |
| **Seam** | A place in a legacy system where behaviour can be intercepted or replaced without editing the surrounding code. The unit of strangler-pattern decomposition. |
| **Strangler pattern** | Incrementally replacing a legacy system by routing slices of traffic to new implementations until the old system carries none. |
| **Trust boundary** | A line across which data or requests change privilege level, requiring authentication, authorisation, or validation. |

## Data terms

| Term | Definition |
| --- | --- |
| **Authoritative source** | The system designated as correct for a data element. Not necessarily where it was first captured, and not necessarily where most consumers read it. |
| **Canonical data model** | A shared conceptual/logical model used to mediate between systems, each of which has its own physical model. |
| **Data custodian** | Technical role operating the store and enforcing controls. |
| **Data domain** | A grouping of related data under one accountable owner. |
| **Data lineage** | The documented path of a data element from origin through every transformation to every consumption point. *Field-level* lineage names source and target attributes; *system-level* lineage names only the systems. |
| **Data owner** | Business role accountable for meaning, access, and quality targets. |
| **Data steward** | Operational role maintaining definitions and remediating quality issues. |
| **Derived field** | A field computed from others rather than captured. The highest-risk category in any corpus: meaning is lost at the point of derivation. |
| **Effective dating** | Attaching validity periods to reference data so that historical records decode using the rules in force at the time. Its absence is the single most common cause of unreproducible historical reports. |
| **Golden record** | The surviving, reconciled version of a master entity assembled from multiple sources under a survivorship policy. |
| **Grain** | The level of detail one row represents (e.g. "one order line per day per hold state"). Mis-stated grain is the most common cause of double counting. |
| **Late-arriving data** | Data that arrives after the period it belongs to has been reported, forcing either restatement or a mismatch. |
| **Provenance** | Where a value came from *and under what authority*. Broader than lineage, which is the mechanical path. |
| **Reference data** | Controlled code sets that classify transactional data (hold codes, option codes, status codes). Changes to reference data change system behaviour. |
| **Restatement** | Revising a previously published figure after late or corrected data arrives. |
| **Survivorship rule** | The rule deciding which source's value wins when sources conflict in an MDM match. |

## Data quality dimensions

| Dimension | Question | Example measure |
| --- | --- | --- |
| **Completeness** | Are required values present? | % of order lines with a non-null `model_package_cd` |
| **Validity** | Do values conform to their domain? | % of `hold_cd` values present in the hold code set |
| **Accuracy** | Do values reflect reality? | % of ship dates matching carrier records |
| **Consistency** | Do related values agree across stores? | Order line count in core DB vs. warehouse |
| **Timeliness** | Is data available when needed? | % of ASNs received within the 4h SLA |
| **Uniqueness** | Are there unintended duplicates? | Duplicate `dispatch_id` count |
| **Integrity** | Do relationships hold? | Orphaned order lines with no parent order |

## Interface terms

| Term | Definition |
| --- | --- |
| **Control total** | A count or sum transmitted alongside a batch file so the receiver can prove nothing was lost. |
| **EDI** — Electronic Data Interchange | Standardised B2B document formats (X12, EDIFACT). Common transaction sets in an order-to-cash platform: 850 purchase order, 855 acknowledgement, 856 ASN, 810 invoice, 997 functional acknowledgement. |
| **Functional acknowledgement (997)** | Confirms a partner's system parsed and accepted a transmission. Distinct from a business acceptance. |
| **Idempotency key** | A caller-supplied identifier letting a receiver safely de-duplicate retried requests. |
| **ASN** — Advance Shipping Notice | EDI 856; notifies the receiver what has shipped, when, and how. |
| **Poison message** | A message that fails processing repeatedly and must be quarantined to avoid blocking a queue. |
| **Reconciliation** | Independent comparison of two systems' records of the same events to detect silent loss or duplication. |

## Operations terms

| Term | Definition |
| --- | --- |
| **Batch window** | The wall-clock period in which a batch chain must complete, bounded by an upstream data availability time and a downstream cutoff. |
| **Error budget** | The permitted amount of unreliability implied by an SLO, spent by incidents and risky changes. |
| **Restart semantics** | What happens when a failed job is re-run: from the beginning, from a checkpoint, or not at all without manual cleanup. Must be stated per job — assuming re-runnability is a leading cause of duplicate financial postings. |
| **RTO / RPO** | Recovery Time Objective: how quickly service must be restored. Recovery Point Objective: how much data loss is tolerable. |
| **Runbook drift** | Divergence between a documented procedure and current reality. Detected by execution, not by reading. |

## Confidence conventions

| Term | Definition |
| --- | --- |
| **✅ Verified** | Confirmed against a primary source, with the source cited. |
| **🟡 Inferred** | Derived from indirect evidence, with the evidence and reasoning stated. |
| **🔴 Assumed** | Believed but unconfirmed, with a named owner and a path to confirmation. |
| **Assumption burn-down** | The practice of tracking and resolving `🔴 Assumed` items on a schedule rather than leaving them indefinitely. |
