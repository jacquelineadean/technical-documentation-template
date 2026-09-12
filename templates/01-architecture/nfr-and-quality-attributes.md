---
doc_id: NFR-<SCOPE>-001
title: <System Name> — Non-Functional Requirements and Quality Attributes
doc_type: nfr
status: draft
version: 0.1.0
owner: <Architecture Lead role>
approvers: []
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: semi-annual
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [TAD-<SCOPE>-001]
downstream_docs: []
tags: [nfr]
---

# \<System Name\> — Non-Functional Requirements and Quality Attributes

> **Purpose.** Turn adjectives into budgets. Every entry must have a number, a measurement
> method, and a current measured value. An NFR you are not measuring is an aspiration, and
> should be labelled as one.
>
> **Format.** Use quality attribute scenarios — source, stimulus, environment, artefact,
> response, response measure. The discipline forces you to state conditions, which is where
> vague requirements hide.

---

## 1. Priorities

> Ranked. Architecture is the practice of deciding which qualities lose when they conflict,
> and an unranked list defers that decision to whoever is implementing at the time.

| Rank | Attribute | Why this rank | What we trade away for it |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

**Known conflicts**

| Attribute A | Attribute B | Conflict | Resolution |
| --- | --- | --- | --- |
| | | | |

---

## 2. Scenario template

Every requirement below follows this structure:

| Element | Meaning |
| --- | --- |
| **Source** | Who or what initiates the stimulus |
| **Stimulus** | The condition that arrives |
| **Environment** | The state of the system when it arrives (normal, peak, degraded) |
| **Artefact** | What is stimulated |
| **Response** | What the system does |
| **Response measure** | The number that makes it testable |

---

## 3. Performance

| ID | Scenario | Response measure | Current | Met | Measurement |
| --- | --- | --- | --- | --- | --- |
| NFR-PERF-01 | A user submits an order during business hours under normal load | p95 ≤ \<N\> ms, p99 ≤ \<N\> ms | | | |
| NFR-PERF-02 | The same, at peak (\<define peak\>) | p99 ≤ \<N\> ms | | | |
| NFR-PERF-03 | Nightly decode processes \<N\> lines | Completes within \<N\> min | | | |
| NFR-PERF-04 | A partner queries order status | p99 ≤ \<N\> ms | | | |

**Rules**

- Percentiles only. An average latency requirement is unsatisfiable and unfalsifiable.
- State the load under which the percentile holds. "p99 ≤ 300ms" without a load figure is
  not a requirement.
- Distinguish **normal** from **peak** and define peak concretely — a date, an event, a
  multiplier.

---

## 4. Throughput and capacity

| ID | Scenario | Response measure | Current | Headroom | Scaling limit |
| --- | --- | --- | --- | --- | --- |
| NFR-CAP-01 | Sustained order intake | ≥ \<N\>/hour | | | |
| NFR-CAP-02 | Peak-day order intake | ≥ \<N\>/day | | | |
| NFR-CAP-03 | Concurrent users | ≥ \<N\> | | | |
| NFR-CAP-04 | Outbound file generation | \<N\> records in \<N\> min | | | |

**Growth assumptions**

| Dimension | Current | +1 year | +3 years | Basis | First constraint hit |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 5. Availability and reliability

| ID | Scenario | Response measure | Current | Met | Measurement |
| --- | --- | --- | --- | --- | --- |
| NFR-AVAIL-01 | Order entry during business hours | ≥ \<N\>% excluding planned maintenance | | | |
| NFR-AVAIL-02 | Batch chain completes by cutoff | ≥ \<N\>% of nights | | | |
| NFR-AVAIL-03 | Partner-facing interface | ≥ \<N\>% | | | |

**Availability definitions**

| Term | Definition for this system |
| --- | --- |
| Available | *(what specifically must work — be precise; "the system is up" is not measurable)* |
| Planned maintenance | |
| Measurement window | |
| Measurement point | *(synthetic probe, real user, server-side — each gives a different number)* |

**Error budget**

| Target | Allowed downtime/month | Consumed YTD | Policy when exhausted |
| --- | --- | --- | --- |
| | | | |

---

## 6. Recoverability

| ID | Scenario | RTO | RPO | Current tested | Last test |
| --- | --- | --- | --- | --- | --- |
| NFR-REC-01 | Primary database loss | | | | |
| NFR-REC-02 | Site loss | | | | |
| NFR-REC-03 | Data corruption detected \<N\> hours later | | | | |
| NFR-REC-04 | Accidental mass deletion | | | | |

> RTO/RPO that have never been tested are estimates. Record the last successful test date;
> an untested recovery objective is a `🔴 Assumed` claim in a document that people will rely
> on during their worst day.

---

## 7. Data integrity and consistency

| ID | Scenario | Response measure | Control |
| --- | --- | --- | --- |
| NFR-DATA-01 | An inbound file is delivered twice | Zero duplicate business effect | |
| NFR-DATA-02 | A batch job fails mid-run | No partial financial postings survive | |
| NFR-DATA-03 | Two systems hold the same figure | Reconcile within \<tolerance\> daily | |
| NFR-DATA-04 | A transformation loses records | Detected within \<N\> hours | |

---

## 8. Security

| ID | Scenario | Response measure | Current |
| --- | --- | --- | --- |
| NFR-SEC-01 | Credentials at rest | \<standard\> | |
| NFR-SEC-02 | Data in transit externally | \<standard\> | |
| NFR-SEC-03 | Privileged access | Approved, time-bound, logged | |
| NFR-SEC-04 | Audit trail retention | \<period\>, tamper-evident | |
| NFR-SEC-05 | Vulnerability remediation | Critical within \<N\> days | |

---

## 9. Maintainability and changeability

> These are usually left out, which is why legacy systems become unchangeable without anyone
> deciding that they should. Measure them.

| ID | Scenario | Response measure | Current |
| --- | --- | --- | --- |
| NFR-MAINT-01 | A business rule changes | Deployed within \<N\> days | |
| NFR-MAINT-02 | A new reference code is added | Configurable without a release | |
| NFR-MAINT-03 | A new partner is onboarded | \<N\> weeks from contract to production | |
| NFR-MAINT-04 | A new engineer joins | Productive on a small change within \<N\> weeks | |
| NFR-MAINT-05 | A defect is found in production | Diagnosable from logs without code reading in \<N\>% of cases | |

---

## 10. Observability

| ID | Scenario | Response measure | Current |
| --- | --- | --- | --- |
| NFR-OBS-01 | A batch job fails | Alert within \<N\> min | |
| NFR-OBS-02 | An expected inbound file does not arrive | Alert within \<N\> min of the deadline | |
| NFR-OBS-03 | An order is stuck | Locatable by ID with current state and reason | |
| NFR-OBS-04 | Silent data loss in an interface | Detected by reconciliation within \<N\> hours | |
| NFR-OBS-05 | A user reports a problem | Their transaction traceable end to end | |

---

## 11. Compliance and audit

| ID | Requirement | Source | Control | Evidence | Frequency |
| --- | --- | --- | --- | --- | --- |
| NFR-COMP-01 | | *(name the regulation or policy clause)* | | | |

---

## 12. Usability and accessibility

| ID | Scenario | Response measure | Current |
| --- | --- | --- | --- |
| NFR-USE-01 | A trained user completes \<key task\> | ≤ \<N\> min, ≤ \<N\> errors | |
| NFR-USE-02 | Accessibility conformance | \<standard/level\> | |

---

## 13. Portability and operability

| ID | Requirement | Rationale | Current |
| --- | --- | --- | --- |
| NFR-PORT-01 | | | |

---

## 14. Compliance summary

| Category | Requirements | Met | Partially met | Not met | Not measured |
| --- | --- | --- | --- | --- | --- |
| Performance | | | | | |
| Capacity | | | | | |
| Availability | | | | | |
| Recoverability | | | | | |
| Data integrity | | | | | |
| Security | | | | | |
| Maintainability | | | | | |
| Observability | | | | | |

**Not measured** is the column that matters most on a first pass. A large "not measured"
count is the honest starting position for a legacy platform, and it is a better input to
planning than a set of confident guesses.

### Gaps requiring action

| NFR | Gap | Business risk | Remediation | Effort | Owner | Target |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
