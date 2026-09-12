---
doc_id: ADR-<SCOPE>-0001
title: <Decision stated as an imperative — "Externalise hold evaluation from the decoder">
doc_type: adr
status: draft
version: 1.0.0
owner: <Architecture Lead role>
authors: []
approvers: []
created: <YYYY-MM-DD>
review_cycle: on-change
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [TAD-<SCOPE>-001]
downstream_docs: []
supersedes:
superseded_by:
tags: [decision]
---

# ADR-\<NNNN\>: \<Decision stated as an imperative\>

> **Title rule.** State the decision, not the topic. "Externalise hold evaluation from the
> decoder" — not "Hold evaluation". A reader scanning a list of 80 ADR titles should be able
> to reconstruct the architecture from the titles alone.
>
> **Immutability.** Once `accepted`, an ADR is never edited except to change `status` and
> add links. A changed decision is a **new ADR** that supersedes this one. The historical
> record of what was decided and why is the entire value of the format.
>
> **When to write one.** A decision is architecturally significant if reversing it later
> would be expensive, if it affects more than one team, or if it constrains a quality
> attribute. Otherwise do not write an ADR — a corpus diluted with trivia stops being read.

| | |
| --- | --- |
| **Status** | Proposed / Accepted / Rejected / Deprecated / Superseded by ADR-NNNN |
| **Date decided** | |
| **Deciders** | *(roles)* |
| **Consulted** | |
| **Informed** | |
| **Reversal cost** | Low (days) / Medium (weeks) / High (months) / Practically irreversible |

---

## Context

> The forces at play. A reader should finish this section feeling the tension that made the
> decision hard. If the context does not make the decision look difficult, either the
> decision was not significant or the context is incomplete.
>
> Cover: what prompted this now; the constraints in force; what is at stake; what happens if
> nothing is decided.

### Forces

| Force | Pushes toward | Weight |
| --- | --- | --- |
| | | High / Medium / Low |

### Constraints in force at decision time

> Record these explicitly. A future reader needs to know whether a constraint that shaped
> this decision still applies — that is what makes an ADR re-evaluable rather than merely
> historical.

| Constraint | Type | Still expected to hold? |
| --- | --- | --- |
| | Hard / Soft | |

---

## Decision

> One paragraph, present tense, active voice: **"We will …"**. Then the specifics.

We will …

### What this means concretely

| Aspect | Decision |
| --- | --- |
| Scope of application | |
| Components affected | |
| Interfaces affected | |
| Data affected | |
| Timeline | |
| Migration approach for existing state | |

---

## Options considered

> At least two real alternatives, each with a genuine case for it. A straw-man alternative
> is worse than no alternative: it signals that the decision was not actually weighed, and
> it removes the future reader's ability to re-open it honestly.

### Option 1 — \<name\> ⭐ *(chosen)*

**Summary:**

| Pros | Cons |
| --- | --- |
| | |

**Why chosen:**

### Option 2 — \<name\>

| Pros | Cons |
| --- | --- |
| | |

**Why rejected:** *(a reason a proponent of this option would recognise as fair)*

### Option 3 — \<name\>

| Pros | Cons |
| --- | --- |
| | |

**Why rejected:**

### Option evaluation

| Criterion | Weight | Option 1 | Option 2 | Option 3 |
| --- | --- | --- | --- | --- |
| | | | | |

> Use a scored matrix only when it genuinely informed the decision. A matrix
> reverse-engineered to justify a decision already made is visible to readers and corrodes
> trust in the whole ADR set.

---

## Consequences

### Positive

-

### Negative

> Mandatory. Every architectural decision has costs. An ADR with no negative consequences
> has not been thought through, and reviewers should return it.

-

### What becomes harder

> Distinct from "negative": these are the future options this decision closes off or makes
> expensive.

| Now harder | Why | Mitigation |
| --- | --- | --- |
| | | |

### Risks accepted

| Risk | Likelihood | Impact | Accepted by | Trigger for re-evaluation |
| --- | --- | --- | --- | --- |
| | | | | |

---

## Implementation notes

| Item | Detail |
| --- | --- |
| Work required | |
| Sequencing / phasing | |
| Backwards compatibility | |
| Rollback plan | |
| Documents to update | |
| Success criteria | *(how we will know, and by when)* |

---

## Compliance and verification

> How will anyone know, in two years, whether this decision was actually implemented and is
> still being followed? A decision with no verification mechanism drifts silently.

| Aspect | Verification | Frequency | Owner |
| --- | --- | --- | --- |
| | *(architecture fitness function, review checkpoint, automated test, code owner rule)* | | |

---

## Re-evaluation triggers

> Name the conditions under which this decision should be revisited. It converts an ADR from
> a historical artefact into a live control.

| Trigger | Action |
| --- | --- |
| | |

---

## References

| Reference | Location |
| --- | --- |
| Related ADRs | |
| TAD sections | |
| Evidence / spike results | |
| External material | |

---

## Retrospective ADRs

> For reconstructing a decision taken long ago whose rationale is still load-bearing:
>
> - Set `status: accepted` and `date decided: unknown (circa <year>)`.
> - Mark the Context and Options sections `🟡 Inferred` or `🔴 Assumed`, and say what the
>   reconstruction is based on: code archaeology, surviving design notes, SME recollection.
> - Record who reconstructed it and when.
> - Add a re-evaluation trigger, since the original constraints may well have lapsed.
>
> The purpose is not historical tidiness. It is to stop a modernization team removing
> something that exists for a reason nobody wrote down — the most expensive mistake
> available to a legacy re-platforming programme.
