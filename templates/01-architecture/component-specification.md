---
doc_id: CMP-<SCOPE>-001
title: <Component Name> — Component Specification
doc_type: cmp
status: draft
version: 0.1.0
owner: <Owning team role>
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: semi-annual
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [TAD-<SCOPE>-001]
downstream_docs: []
tags: []
---

# \<Component Name\> — Component Specification

> **Purpose.** The contract a component offers the rest of the system, and what it needs in
> return. One per deployable or independently-runnable unit. This is the document an
> engineer reads before calling something they did not write, and the one an SRE reads
> before it wakes them up.

---

## Contents

| Section | Summary |
| --- | --- |
| [1. Identity](#1-identity) | Name, type, repository, owning team, runtime |
| [2. Responsibility](#2-responsibility) | Single-sentence responsibility, plus explicit in and out of scope |
| [3. Provided interfaces](#3-provided-interfaces) | Interfaces offered: consumers, contract, stability |
| [4. Required interfaces](#4-required-interfaces) | Dependencies with hard/soft classification, timeout, fallback |
| [5. Data](#5-data) | Stores accessed, ownership, and what the component is authoritative for |
| [6. Runtime behaviour](#6-runtime-behaviour) | Startup, readiness, concurrency, state, shutdown |
| [7. Configuration](#7-configuration) | Configuration keys and secret references — names and stores only |
| [8. Resource profile](#8-resource-profile) | CPU, memory, I/O, connections at idle, normal, peak, and limit |
| [9. Failure modes](#9-failure-modes) | Failure modes, detection, recovery, and downstream consumer impact |
| [10. Observability](#10-observability) | Metrics, logs, traces, golden signals, alerts |
| [11. Security](#11-security) | Runtime identity, network exposure, authentication, authorisation |
| [12. Change and release](#12-change-and-release) | Release cadence, deployment method, backwards compatibility |
| [13. Knowledge](#13-knowledge) | Bus factor and how many people can change it safely |
| [Change log](#change-log) | Version, date, author, change |

---

## 1. Identity

| | |
| --- | --- |
| Component name | |
| Type | Service / Batch job suite / Library / UI / Adapter / Scheduled task |
| Repository | |
| Deployment artefact | |
| Runtime / platform | |
| Language & version | |
| Owning team | |
| On-call rotation | |
| Criticality | Tier 1 / 2 / 3 |
| Lifecycle stage | Active / Maintenance / Deprecated / Sunset *(with date)* |

---

## 2. Responsibility

**Single-sentence responsibility:**

**In scope**

| Responsibility | Notes |
| --- | --- |
| | |

**Explicitly not this component's job**

| Not responsible for | Which component is |
| --- | --- |
| | |

> A component whose responsibility cannot be stated in one sentence is doing more than one
> job. That is worth recording as technical debt even when it is not worth fixing.

---

## 3. Provided interfaces

| ID | Interface | Type | Consumers | Contract | Stability |
| --- | --- | --- | --- | --- | --- |
| | | API / Event / File / Batch output / Library API | | *(link)* | Stable / Evolving / Deprecated |

### 3.1 \<Interface name\>

| | |
| --- | --- |
| Endpoint / destination | |
| Authentication | |
| Request/payload schema | |
| Response schema | |
| Idempotency | |
| Rate limits | |
| SLA | |
| Error catalog | |

---

## 4. Required interfaces

| Dependency | Type | Purpose | Criticality | Failure behaviour | Timeout | Fallback |
| --- | --- | --- | --- | --- | --- | --- |
| | | | Hard / Soft | | | |

**Hard vs. soft:** a **hard** dependency being unavailable stops the component; a **soft**
one degrades it. State which for every dependency — the distinction determines whether an
outage cascades, and it is usually assumed rather than decided.

---

## 5. Data

| Store | Access | Tables/objects | Owned? | Notes |
| --- | --- | --- | --- | --- |
| | Read / Write / Read-write | | Yes/No | |

**Data this component is authoritative for:**

| Entity/field | Meaning | Consumers |
| --- | --- | --- |
| | | |

**State held**

| State | Location | Durable? | Lost on restart? | Recovery |
| --- | --- | --- | --- | --- |
| | | | | |

---

## 6. Runtime behaviour

| Aspect | Detail |
| --- | --- |
| Startup sequence & duration | |
| Readiness check | |
| Liveness check | |
| Graceful shutdown behaviour | |
| In-flight work on shutdown | |
| Concurrency model | |
| Scaling model | Horizontal / Vertical / Fixed |
| Instance count (per environment) | |
| Scheduled activity | |
| Warm-up / cache-priming needs | |

---

## 7. Configuration

| Key | Purpose | Default | Environment-varying | Restart required |
| --- | --- | --- | --- | --- |
| | | | | |

**Secrets** *(names and stores only)*

| Secret | Store | Used for | Rotation cadence |
| --- | --- | --- | --- |
| | | | |

---

## 8. Resource profile

| Resource | Idle | Normal | Peak | Limit | Behaviour at limit |
| --- | --- | --- | --- | --- | --- |
| CPU | | | | | |
| Memory | | | | | |
| Disk | | | | | |
| Connections (DB) | | | | | |
| Threads / workers | | | | | |

---

## 9. Failure modes

| Failure | Symptom | Detection | Impact | Automatic recovery | Runbook |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

**What breaks downstream when this component is unavailable:**

| Consumer | Impact | Their degradation behaviour |
| --- | --- | --- |
| | | |

---

## 10. Observability

| Signal | Name | Type | Purpose | Alert |
| --- | --- | --- | --- | --- |
| | | Metric / Log / Trace | | |

**Golden signals**

| Signal | Metric | Normal range | Alert threshold |
| --- | --- | --- | --- |
| Traffic | | | |
| Errors | | | |
| Latency | | | |
| Saturation | | | |

---

## 11. Security

| Aspect | Detail |
| --- | --- |
| Runs as (identity) | |
| Network exposure | |
| Inbound authentication | |
| Outbound credentials | |
| Data classification handled | |
| Audit events emitted | |
| Known security debt | |

---

## 12. Change and release

| Aspect | Detail |
| --- | --- |
| Release cadence | |
| Deployment method | |
| Zero-downtime capable | |
| Backwards compatibility policy | |
| Rollback method & window | |
| Database migration coupling | |
| Feature flags in use | |

---

## 13. Knowledge

| Aspect | Detail |
| --- | --- |
| People who can change this safely | *(count, not names)* |
| Bus factor | |
| Onboarding time for a new engineer | |
| Key knowledge gaps | |
| Documentation completeness | |

> A component with a bus factor of 1 is an architectural risk regardless of its technical
> quality, and it belongs in the TAD's debt register with that framing.

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
