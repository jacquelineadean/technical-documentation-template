---
doc_id: CHK-101
title: Architecture Review Checklist
doc_type: checklist
status: draft
version: 0.1.0
owner: <Head of Architecture role>
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: annual
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: []
downstream_docs: []
tags: [review, governance]
---

# Architecture Review Checklist

> **Purpose.** Gate criteria applied before a TAD, HLD, or significant ADR is approved.
> Copy into the review record, complete, and attach the outcome.
>
> **Posture.** A review is not a quality inspection of the document's prose. It asks four
> questions: is the problem understood, is the solution sound, are the consequences
> accepted by the people who will bear them, and can it be operated?

---

## Review record

| | |
| --- | --- |
| Subject | |
| Document(s) | |
| Review type | TAD / HLD / ADR / Interface / Data |
| Date | |
| Chair | |
| Reviewers | |
| Outcome | Approved / Approved with conditions / Rework / Rejected |
| Conditions | |
| Next review | |

---

## 1. Problem and drivers

- [ ] The business problem is stated in business terms with evidence, not as a technology preference
- [ ] Requirements are traceable to a BRD or an equivalent authority
- [ ] Quality attributes are **ranked**, and the trade-offs accepted are stated
- [ ] Constraints distinguish hard from soft, with the soft ones challenged
- [ ] "Do nothing" was considered and its cost quantified

## 2. Scope

- [ ] In scope and out of scope both stated explicitly
- [ ] Affected domains identified, and their owners consulted
- [ ] Affected external parties identified, with notice periods established
- [ ] Interactions with in-flight initiatives identified

## 3. Solution

- [ ] At least two genuine alternatives considered, with fair reasons for rejection
- [ ] The solution is consistent with stated architecture principles; deviations are explicit and accepted
- [ ] Integration patterns follow the [integration architecture](integration-architecture.md); deviations justified
- [ ] Complexity is proportionate to the problem
- [ ] Nothing is built that could reasonably be bought or reused
- [ ] Standard components are used where they exist

## 4. Data

- [ ] Data ownership is clear for every entity created or modified
- [ ] No cross-domain writes introduced without explicit dual approval
- [ ] Authoritative source identified for each data element
- [ ] Data lineage impact assessed and documented
- [ ] Data classification assessed; controls match the classification
- [ ] Retention and disposal addressed
- [ ] Historical data impact considered — does this change the meaning of existing rows?
- [ ] Reference data changes are effective-dated
- [ ] Data quality controls defined for new data flows
- [ ] Reconciliation defined for any new data movement

## 5. Interfaces

- [ ] Every new or changed interface has a drafted ICD
- [ ] Both sides have a named accountable owner
- [ ] Versioning and backwards-compatibility approach stated
- [ ] Error handling, retries, and idempotency defined
- [ ] Delivery semantics and ordering guarantees stated
- [ ] Partner notice periods reflected in the delivery plan
- [ ] Volumes stated for normal and peak, with the peak driver named

## 6. Non-functional

- [ ] Every NFR has a number and a measurement method
- [ ] Performance targets are percentile-based, with the load stated
- [ ] Capacity headroom assessed against 12-month growth
- [ ] **Batch window impact assessed** — new or extended jobs fit within available slack
- [ ] Availability target stated with its definition of "available"
- [ ] RTO/RPO stated and achievable with the proposed design
- [ ] Cost impact estimated

## 7. Resilience

- [ ] Failure modes enumerated across availability, data, processing, and capacity
- [ ] **Silent failure modes identified**, with detection time stated
- [ ] Behaviour when each dependency is unavailable is defined
- [ ] Hard vs. soft dependencies distinguished
- [ ] Retry policies bounded end to end; no retry storm across layers
- [ ] Partial-failure state is defined and recoverable
- [ ] Duplicate processing cannot produce duplicate business effect
- [ ] No new single point of failure, or it is explicitly accepted with a named accepter

## 8. Security and privacy

- [ ] Trust boundaries identified; controls stated at each crossing
- [ ] Authentication and authorisation designed, including data-level restrictions
- [ ] Sensitive data identified; protection at rest, in transit, and in non-prod stated
- [ ] Secrets managed through the approved store; no new hard-coded credentials
- [ ] Audit events defined for privileged and data-modifying actions
- [ ] Privacy impact assessed; subject rights supportable
- [ ] Security review completed for anything crossing an external boundary

## 9. Operability

- [ ] Monitoring signals defined, including a "did not happen" check for scheduled work
- [ ] Alerts have thresholds, routes, and runbooks
- [ ] Runbook created or updated
- [ ] Deployment and rollback procedures defined, with a stated rollback window
- [ ] Database changes use expand/contract where the schema is shared
- [ ] Job schedule changes version-controlled and tested
- [ ] Support model agreed; the receiving team has accepted it
- [ ] DR plan updated

## 10. Delivery and risk

- [ ] Delivery is sliced so that value arrives before the end
- [ ] Each slice is independently reversible, or the irreversibility is explicit
- [ ] Dependencies on other teams identified and agreed
- [ ] Test approach covers interfaces, data migration, and non-functional aspects
- [ ] Risks registered with owners and triggers
- [ ] Assumptions listed with verification plans

## 11. Documentation

- [ ] TAD updated or scheduled for update
- [ ] ADRs written for decisions that are expensive to reverse
- [ ] Business rules catalogued with IDs
- [ ] Data dictionary and lineage updated
- [ ] Interface catalog updated
- [ ] Impact assessment lists every document requiring change, with owners

---

## Conditions and actions

| # | Condition / action | Owner | Due | Blocking approval | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | Yes/No | |

## Dissenting views

> Record disagreement that was not resolved. A review that never records dissent is not
> reviewing anything, and the record is what allows a later reader to understand why a
> known objection was overridden.

| Reviewer | Concern | Response | Accepted by |
| --- | --- | --- | --- |
| | | | |
