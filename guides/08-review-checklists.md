---
doc_id: CHK-008
title: Review Checklists
doc_type: checklist
status: approved
version: 1.0.0
owner: Documentation Architect
classification: internal
last_reviewed: 2026-09-12
next_review: 2027-03-12
review_cycle: semi-annual
tags: [meta, review, quality]
---

# Review Checklists

Per-document-type gates. Copy the relevant block into the PR description and tick it. A
reviewer's job is to check these, not to restyle prose.

---

## Contents

| Section | Summary |
| --- | --- |
| [Universal — applies to every document](#universal--applies-to-every-document) | Front matter, ownership, confidence tags, layer placement, prohibited content |
| [TAD — Technical Architecture Document](#tad--technical-architecture-document) | Scope, C4 reconciliation, NFR measurability, failure modes, debt register |
| [ADR — Architecture Decision Record](#adr--architecture-decision-record) | Decision-stating title, forces in context, rejected options, consequences |
| [ICD — Interface Control Document](#icd--interface-control-document) | Named counterparties, field-level specification, errors, SLA, versioning |
| [Data Lineage](#data-lineage) | Field-level hops, numbered and reconciled across diagram and table |
| [Data Governance Charter](#data-governance-charter) | Decision rights, named data roles, cross-domain ownership resolved |
| [Business Rules Catalog](#business-rules-catalog) | Atomicity, stable IDs, testability, source of authority |
| [Runbook](#runbook) | Written for 03:00 with no context: triggers, prerequisites, verification |
| [Impact Assessment](#impact-assessment) | Mechanical graph traversal first, then judgement; enumerated blast radius |
| [Domain Pack (the six documents together)](#domain-pack-the-six-documents-together) | Cross-document consistency checks for the six domain documents |

---

## Universal — applies to every document

- [ ] Front matter complete and valid (`python3 tools/validate_docs.py <path>` passes)
- [ ] `owner` is a role, not a person
- [ ] H1 matches front-matter `title`
- [ ] `## Contents` table present and linking to every section, back matter included
- [ ] Every claim about existing behaviour is either trivially checkable or carries a
      confidence tag with evidence
- [ ] Every `🔴 Assumed` item has a named owner and a target resolution date
- [ ] Every `✅ Verified` claim cites its source (code + line + release, query, or trace)
- [ ] No credentials, tokens, keys, connection strings, or real personal data
- [ ] Diagrams have captions; prose carries the facts; ≤ 15 nodes per diagram
- [ ] Relative links resolve; document IDs cited in the form `<DOC-ID> §<section>`
- [ ] No fact duplicated from another layer — linked instead
- [ ] `upstream_docs` / `downstream_docs` populated so impact analysis can traverse
- [ ] A newcomer could act on this without asking a question the document should answer

---

## TAD — Technical Architecture Document

- [ ] §1 scope states explicitly what is **out** of scope, not only what is in
- [ ] C4 Level 1 shows every external actor from the Interface Catalog — counts reconcile
- [ ] C4 Level 2 containers each have an owning team and a technology stated
- [ ] Level 3 provided for containers with non-obvious internals; omitted elsewhere with a
      one-line justification
- [ ] Every arrow is labelled with protocol and payload
- [ ] NFRs are measurable with a budget and a measurement method — no adjectives
- [ ] Failure modes cover: upstream unavailable, downstream unavailable, partial batch
      failure, duplicate delivery, data corruption, capacity exhaustion
- [ ] Batch/scheduling covered or explicitly delegated to a `BAT` document
- [ ] Technical debt register present with owner, business impact, and remediation cost
- [ ] Constraints distinguish *cannot change* from *have not changed yet*
- [ ] Current state and target state are visibly separate — no aspirational architecture
      presented as fact
- [ ] Cross-domain coupling and shared-data ownership addressed explicitly
- [ ] Every architecturally significant decision has an ADR, linked

---

## ADR — Architecture Decision Record

- [ ] Title states the decision, not the topic ("Externalise hold evaluation from the
      decoder", not "Hold evaluation")
- [ ] Context describes forces, not just background — a reader should feel the tension
- [ ] ≥ 2 genuine alternatives, each with why it was rejected. A straw man is a defect
- [ ] Consequences include the negative ones and the things now harder
- [ ] Reversal cost stated
- [ ] Status correct; if superseding another ADR, both are cross-linked
- [ ] No edits to an accepted ADR other than status and links — supersede instead

---

## ICD — Interface Control Document

- [ ] Both sides named with an accountable role each
- [ ] Interface version distinct from document version
- [ ] Every field: name, type, length, optionality, domain/valid values, example
- [ ] Character encoding, decimal separators, date formats, and timezone stated explicitly
- [ ] Null/empty/absent semantics distinguished (the three are not the same)
- [ ] Key fields and uniqueness constraints identified
- [ ] Error catalog complete: transport, syntax, semantic, business-rejection
- [ ] Retry policy with counts, intervals, and terminal action
- [ ] Idempotency/duplicate-handling behaviour stated
- [ ] Ordering guarantees stated (or explicitly none)
- [ ] Control totals or reconciliation mechanism defined for batch/file interfaces
- [ ] SLA: availability, latency/cutoff, throughput, and measurement method
- [ ] Volume: normal, peak, and peak *cause* (month-end, model-year changeover)
- [ ] Versioning and deprecation policy with notice period
- [ ] Sequence diagram includes at least one error path, with timeouts
- [ ] Test approach and certification criteria for a new counterparty
- [ ] Security: transport, authentication, and classification of data in transit

---

## Data Lineage

- [ ] Lineage is **field-level**, not system-level, for every critical field
- [ ] Every hop numbered and present in both diagram and table
- [ ] Each hop names the executing job/process and its schedule
- [ ] Transformation logic stated precisely enough to reproduce, or cites a rule ID
- [ ] Filters and joins explicit — especially exclusions, the usual cause of reconciliation
      gaps
- [ ] Grain stated at each hop, with any grain change called out
- [ ] Late-arriving and restatement behaviour described
- [ ] Reconciliation control identified per hop, with owner and frequency
- [ ] Known breaks/gaps listed with issue IDs rather than omitted
- [ ] Retention at each hop stated — lineage that outlives its data is misleading
- [ ] Effective-dating of reference data used in transformations addressed
- [ ] Consumers enumerated, so a change can be impact-assessed

---

## Data Governance Charter

- [ ] Decision rights unambiguous: who decides what, and what happens when parties disagree
- [ ] Data Owner / Steward / Custodian named per domain
- [ ] Cross-domain and shared-table ownership explicitly resolved
- [ ] Policies are enforceable and have a named enforcement mechanism, not aspirations
- [ ] Forums have cadence, membership, quorum, and decision-recording method
- [ ] Escalation path terminates at a role with actual authority
- [ ] Compliance measured with stated metrics and a reporting route
- [ ] Exception process defined, time-boxed, and logged
- [ ] Regulatory drivers mapped to specific controls

---

## Business Rules Catalog

- [ ] Every rule atomic — one condition set, one outcome
- [ ] Every rule has a stable ID, never reused
- [ ] Every rule is independently testable
- [ ] Source of authority cited (policy document, regulation, code location, or "unknown —
      inferred")
- [ ] Effective dates present where a rule has changed over time
- [ ] Exceptions and overrides documented with who may apply them
- [ ] Conflicting rules identified with precedence stated
- [ ] Retired rules retained with `status: retired` and a retirement date
- [ ] Rules cross-referenced from the relevant process flow and state model

---

## Runbook

- [ ] Written for someone with no context, at 03:00
- [ ] Trigger conditions stated: which alert, which symptom
- [ ] Prerequisites listed: access, tools, approvals needed *before* starting
- [ ] Steps are numbered, imperative, and individually verifiable
- [ ] Expected output shown for each step that produces one
- [ ] Decision points have explicit branches
- [ ] Rollback/undo path for every mutating step
- [ ] Escalation criteria and route with actual names/channels
- [ ] Financial or data-integrity risks flagged before the step, not after
- [ ] Verification step confirming the issue is resolved
- [ ] Executed end to end by someone other than the author, and dated

---

## Impact Assessment

- [ ] Started from a mechanical traversal of the `downstream_docs` graph, then extended by
      judgement
- [ ] Components, data elements, interfaces, reports, and jobs enumerated individually
- [ ] External parties identified with required notice periods
- [ ] Historical/restatement impact considered — does this change past data?
- [ ] Reference data and effective dating considered
- [ ] Reversibility stated: can this be rolled back after go-live, and for how long?
- [ ] Documents requiring update listed with owners
- [ ] Test scope derived from the impact, not chosen independently

---

## Domain Pack (the six documents together)

- [ ] Domain boundary matches the Domain Map; overlaps resolved, not ignored
- [ ] Terms used match the Glossary, with context qualifiers where the term is contested
- [ ] Process flows include exception paths and manual steps
- [ ] State model transitions each cite a rule ID
- [ ] Entities distinguish owned from read-only
- [ ] Interface map reconciles with the Interface Catalog — no interface in one and not the
      other
- [ ] Rules, processes, and states are mutually consistent (a state the process cannot reach
      is a defect in one of the three)
