---
doc_id: MON-<SCOPE>-001
title: <System Name> — Monitoring and Alerting
doc_type: mon
status: draft
version: 0.1.0
owner: <SRE Lead role>
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: quarterly
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [NFR-<SCOPE>-001, RES-<SCOPE>-001]
downstream_docs: []
tags: [monitoring, observability]
---

# \<System Name\> — Monitoring and Alerting

> **Purpose.** What is watched, what fires, where it goes, and what the recipient does about
> it.
>
> **Principle.** Alert on **symptoms the business would notice**, not on causes. A CPU alert
> that fires nightly and is always ignored trains people to ignore alerts. An alert that
> orders have not been dispatched by the vendor cutoff is worth waking someone for.

---

## Contents

| Section | Summary |
| --- | --- |
| [1. Coverage summary](#1-coverage-summary) | Platforms, routing, dashboards, and coverage ratio |
| [2. Service level indicators](#2-service-level-indicators) | SLIs with measurement, SLO target, current attainment, error budget |
| [3. Alerts](#3-alerts) | Alert register: signal, condition, severity, route, runbook, business symptom |
| [4. Alert detail](#4-alert-detail) | Per-alert detail: what it detects, impact if unaddressed, tuning history |
| [5. Coverage against failure modes](#5-coverage-against-failure-modes) | Alert coverage cross-checked against the FMEA — the gaps are the point |
| [6. "Did not happen" monitoring ⚠️](#6-did-not-happen-monitoring-) | Absence-of-event alerting: files that never arrive, jobs that never start |
| [7. Data quality and reconciliation monitoring](#7-data-quality-and-reconciliation-monitoring) | Reconciliation breaks and critical DQ rule breaches |
| [8. Business monitoring](#8-business-monitoring) | Business-meaningful signals that detect a silent failure |
| [9. Dashboards](#9-dashboards) | Dashboards by audience, and the single health screen |
| [10. Logging](#10-logging) | Log destinations, retention, correlation IDs, sensitive-data exclusion |
| [11. On-call](#11-on-call) | Rotation, hours, escalation, handover |
| [12. Alert hygiene](#12-alert-hygiene) | Fire rates, action rates, and the keep/tune/downgrade/delete verdict |
| [Change log](#change-log) | Version, date, author, change |

---

## 1. Coverage summary

| | |
| --- | --- |
| Monitoring platform(s) | |
| Alert routing | |
| Dashboards | |
| Failure modes with automated detection | |
| Failure modes with **no** detection | |
| Alerts firing per week | |
| Alerts actioned vs. ignored | |
| Alerts with a runbook | |

> Track "actioned vs. ignored". A high ignore rate is the single best predictor that a real
> alert will be missed, and it is a stronger argument for tuning than any amount of
> advocacy.

---

## 2. Service level indicators

| SLI | Definition | Measurement | Target (SLO) | Current | Error budget |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 3. Alerts

| ID | Alert | Signal | Condition | Severity | Route | Runbook | Business symptom |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AL-001 | | | | P1/P2/P3 | | | |

**Severity and routing**

| Sev | Meaning | Route | Response | Hours |
| --- | --- | --- | --- | --- |
| P1 | Business impact now or imminent | Page | \<N\> min | 24×7 |
| P2 | Degradation; will become P1 if unaddressed | Page in hours / ticket out of hours | \<N\> min | |
| P3 | Needs attention, not urgent | Ticket | Next business day | |
| P4 | Informational | Dashboard only | — | |

---

## 4. Alert detail

### AL-\<NNN\>: \<name\>

| | |
| --- | --- |
| What it detects | |
| Business impact if unaddressed | |
| Signal | |
| Condition | |
| Evaluation window | |
| Severity | |
| Route | |
| Runbook | |
| False positive rate | |
| Fired in the last 90 days | |
| Actioned | |
| Tuning history | |

---

## 5. Coverage against failure modes

> Cross-check against the [FMEA](../01-architecture/resilience-and-failure-mode-analysis.md).
> The gaps are the point of this table.

| Failure mode | Alert | Time to detect | Gap |
| --- | --- | --- | --- |
| FM-01 | AL-… | | |

**Uncovered failure modes**

| Failure mode | Current detection | Time to detect | Proposed alert | Effort | Priority |
| --- | --- | --- | --- | --- | --- |
| | *("a consumer complains", "at month-end close" — write it plainly)* | | | | |

---

## 6. "Did not happen" monitoring ⚠️

> The class of alert most often missing. Absence of an event raises no error: a file that
> never arrives, a job that never starts, a partner that stops transmitting. The system
> simply goes quiet, and the failure surfaces downstream hours later.

| Expected event | Expected by | Alert if absent at | Route | Runbook |
| --- | --- | --- | --- | --- |
| Inbound file \<name\> | | | | |
| Job \<id\> start | | | | |
| Job \<id\> completion | | | | |
| Partner transmission | | | | |
| Acknowledgement | | | | |
| Periodic reconciliation result | | | | |

---

## 7. Data quality and reconciliation monitoring

| Check | Frequency | Threshold | Alert | Owner |
| --- | --- | --- | --- | --- |
| Reconciliation break | | | | |
| DQ rule breach (critical) | | | | |
| Volume anomaly | | | | |
| Duplicate detection | | | | |
| Referential integrity | | | | |

---

## 8. Business monitoring

> Signals meaningful to the business, not only to engineers. These are what actually detect
> a silent failure — a correct-looking system producing no work.

| Metric | Normal range | Alert | Owner | Rationale |
| --- | --- | --- | --- | --- |
| Orders received per hour | | | | Zero during business hours means intake has stopped |
| Orders dispatched per night | | | | Low means a hold or decode problem |
| Exception queue depth | | | | Growing means a systemic rejection |
| Held items ageing | | | | |
| Straight-through rate | | | | A drop means a rule or reference data change |
| Interface volumes vs. same day last week | | | | |

---

## 9. Dashboards

| Dashboard | Audience | Contents | Refresh | Location |
| --- | --- | --- | --- | --- |
| | | | | |

**Operational overview** — the single screen that answers "is the system healthy?":

| Panel | Shows | Healthy looks like |
| --- | --- | --- |
| | | |

---

## 10. Logging

| Component | Destination | Retention | Searchable | Correlation ID | Sensitive data excluded |
| --- | --- | --- | --- | --- | --- |
| | | | | ✅/❌ | ✅/❌ |

**Key log events**

| Event | Level | Fields | Used for |
| --- | --- | --- | --- |
| | | | |

---

## 11. On-call

| Aspect | Detail |
| --- | --- |
| Rotation | |
| Hours | |
| Paging tool | |
| Acknowledgement expectation | |
| Escalation if unacknowledged | |
| Handover process | |

**Alert load**

| Period | P1 | P2 | P3 | Out-of-hours pages | Actioned |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 12. Alert hygiene

| Alert | Fires/week | Actioned | Verdict | Action |
| --- | --- | --- | --- | --- |
| | | | Keep / Tune / Downgrade / Delete | |

**Review**

| Check | Cadence |
| --- | --- |
| Alerts that fired but were never actioned | Monthly |
| Incidents with no alert | Per incident |
| Alerts with no runbook | Quarterly |
| Thresholds against current baselines | Quarterly |

> "Incidents with no alert" is the highest-value review. Every incident detected by a human
> is a monitoring gap, and reviewing it at the postmortem while the detail is fresh is how
> coverage actually improves.

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
