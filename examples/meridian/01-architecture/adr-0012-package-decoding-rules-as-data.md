---
doc_id: ADR-PLR-0012
title: Hold package decoding rules as reference data rather than code
doc_type: adr
status: approved
version: 1.1.0
owner: Head of Platform Architecture
authors: [Platform Architecture]
approvers: [Head of Platform Architecture]
created: 2025-04-22
review_cycle: on-change
classification: internal
systems: [MERIDIAN]
domains: [product-launch-readiness]
upstream_docs: [TAD-OPS-001]
downstream_docs: [RDR-PLR-001]
tags: [decision, retrospective, reference-data]
---

# ADR-PLR-0012: Hold package decoding rules as reference data rather than code

> ⚠️ **This is a retrospective ADR.** The decision was taken around 2003 during the DB2
> migration. No design record survives. This document reconstructs the decision from code
> archaeology, surviving project documents, and interviews, because the decision is still
> load-bearing and a modernization team could otherwise reasonably reverse it without
> knowing what it was for.
>
> Reconstructed by Platform Architecture, 2025-04. Sections marked 🟡 or 🔴 are inference,
> not record.

| | |
| --- | --- |
| **Status** | Accepted |
| **Date decided** | Unknown — circa 2003 Q2 (DB2 migration project, "Phase 2 — Reference") |
| **Deciders** | 🔴 Unknown. The 2003 project organisation chart names a "Data Architecture" workstream lead; the individual has left and could not be contacted |
| **Reconstructed by** | Platform Architecture, 2025-04-22 |
| **Reversal cost** | **Practically irreversible** — 340 active packages, ~2,900 compatibility rules, and 23 years of effective-dated history depend on the data representation |

---

## Contents

| Section | Summary |
| --- | --- |
| [Context 🟡 *Inferred*](#context--inferred) | Copybook constants and the 17-program recompile, reconstructed from the 2003 analysis |
| [Decision](#decision) | Package composition held as effective-dated reference data, read at decode time |
| [Options considered 🔴 *Assumed*](#options-considered--assumed) | Alternatives reconstructed as inference — explicitly not citable as history |
| [Consequences](#consequences) | Changeover in days rather than weeks, against the observed negative consequences |
| [Subsequent amendment — effective dating (2014-06) ✅ *Verified*](#subsequent-amendment--effective-dating-2014-06--verified) | The 2014 change that added effective dating, and why pre-2014 history is not reproducible |
| [Compliance and verification](#compliance-and-verification) | Re-decode comparison and code review proving the decision still holds |
| [Re-evaluation triggers](#re-evaluation-triggers) | Two of three original constraints have lapsed, so the decision is genuinely re-openable |
| [References](#references) | Surviving source documents, and which did not survive |
| [Change log](#change-log) | Version, date, change |

---

## Context 🟡 *Inferred*

Before the 2003 DB2 migration, package composition was held in COBOL COPYBOOK constants.
Adding a package or changing its option composition required editing a copybook,
recompiling every program that included it (17 programs, per the 2003 impact analysis found
in the project archive), and a full release.

Evidence for the problem this was solving:

| Evidence | Source | Confidence |
| --- | --- | --- |
| Package changes required a full release of 17 programs | `archive/db2-migration-2003/phase2-impact.doc` | ✅ Verified — document survives |
| Model-year changeover took "up to eleven weeks of release activity" | Same document, §3 | ✅ Verified — quoted directly |
| Portfolio Management could not change the catalogue without IT | Interview, retired Portfolio Manager, 2025-03 | 🟡 Inferred — single-source recollection, 22 years after the fact |
| A 1999 audit criticised the lead time for catalogue changes | Referenced in the 2003 document; **the audit itself was not found** | 🔴 Assumed |

The business driver recorded in `SYS-MER-001 §2` as `BD-04` — "portfolio changes must take
effect without a software release" — traces to this period, and the 2003 document's stated
objective is "to permit catalogue maintenance by the business without a program change".

### Forces 🟡 *Inferred*

| Force | Pushes toward | Weight |
| --- | --- | --- |
| Model-year changeover is an annual, high-volume, time-boxed catalogue change | Data | High |
| Release capacity in 2003 was the binding constraint on catalogue agility | Data | High |
| The DB2 migration was already touching every reference structure | Data (opportunistic) | Medium |
| Decoding correctness is financially material; data has no compiler to check it | Code | Medium |
| Business users maintaining production behaviour was novel and unproven in 2003 | Code | 🔴 Unknown whether this was raised |

### Constraints in force at decision time

| Constraint | Type | Still expected to hold? |
| --- | --- | --- |
| Release cycle in 2003 was quarterly | Hard then | ❌ **No longer** — now 6-weekly, with emergency paths |
| Recompiling 17 programs for a copybook change | Hard then | ❌ No longer relevant; the copybooks are gone |
| No configuration-management tooling for non-code artefacts | Hard then | ❌ **No longer** — modern tooling exists and is used elsewhere in the estate |

> Two of the three constraints that motivated this decision have lapsed. That does not make
> the decision wrong — see "Re-evaluation triggers" — but it is exactly the kind of fact a
> retrospective ADR exists to surface.

---

## Decision

**Package composition, option definitions, and compatibility rules are held as
effective-dated reference data in DB2, read at decode time, rather than as compiled
constants or code.**

### What this means concretely

| Aspect | Decision |
| --- | --- |
| Package composition | `PRD_PKG`, `PRD_PKG_OPT` — which options a package contains |
| Option definitions | `PRD_OPT` — option attributes, including those that drive derivation |
| Compatibility rules | `PRD_CMP_RUL` — ~2,900 pairwise and group constraints |
| Evaluation | `ORDPKG03` expands, `ORDCMP04` evaluates. **The evaluator is code; the rules are data.** |
| Effective dating | Added 2014-06, **not in the original 2003 design** — see §"Subsequent amendment" |
| Maintenance | PLR maintenance screens, no release required |
| Change control | None at the time of the original decision |

---

## Options considered 🔴 *Assumed*

> No record of alternatives survives. The options below are reconstructed as what a
> competent team would have weighed in 2003, and are presented as such. **This section is
> inference and should not be cited as history.**

### Option 1 — Rules as effective-dated reference data ⭐ *(chosen)*

| Pros | Cons |
| --- | --- |
| Catalogue changes need no release | No compiler or type system to catch a malformed rule |
| Changeover compressed from weeks to days | Production behaviour becomes editable by non-engineers |
| Historical decoding reproducible *(only after the 2014 amendment)* | Rule evaluation is slower than compiled constants |

### Option 2 — Retain copybook constants, improve the release process

| Pros | Cons |
| --- | --- |
| Compile-time validation retained | Does not address the lead-time problem, which was the driver |
| Familiar to the 2003 team | Release capacity was the binding constraint and could not be expanded |

### Option 3 — Generate COBOL from a catalogue definition

Maintain the catalogue as data, generate and compile constants from it.

| Pros | Cons |
| --- | --- |
| Compile-time validation **and** business-friendly maintenance | Still requires a release to take effect — does not solve the driver |
| Change is reviewable as a diff | Build tooling for generated COBOL was immature in 2003 |

**Why the chosen option probably won** 🟡: it is the only one of the three that removes the
release from the critical path of a catalogue change, which the surviving project document
states as the objective.

---

## Consequences

### Positive — observed, not inferred

- Model-year changeover now takes 4–6 days of catalogue work rather than weeks of release
  activity. ✅ Verified against 2024 and 2025 changeover records.
- Portfolio Management owns the catalogue directly; no IT ticket is required for a package
  change.
- Roughly 40 launches per year are possible; the 2003-era release cadence would have capped
  this at four.
- **Because the rules are data, they became effective-dateable in 2014** — which is why
  post-2014 order history is reproducible at all. The original decision made a later,
  larger benefit possible without intending to.

### Negative — observed

- **Production behaviour is changeable with no approval gate, no review, and no rollback.**
  A portfolio analyst can alter decoding for all 3,200 dealers in a single screen
  transaction. This is `TD-06` in `TAD-OPS-001 §17` and was the root cause of INC-2025-0412
  (USD 310k).
- **No validation equivalent to a compiler.** A rule referencing a retired option code is
  accepted by the maintenance screen and fails at decode time, in production, that night.
- **The code/data split has no stated principle.** Some rules are data and some are COBOL,
  and nobody can predict which without reading code. This is `TD-02`, and NFR-MAINT-01 is
  not met because of it.
- **Reference data changes are invisible to change management.** They do not appear in the
  change calendar, are not counted in change metrics, and are not correlated with incidents
  unless somebody does it by hand.

### What became harder

| Now harder | Why | Mitigation |
| --- | --- | --- |
| Knowing why decode behaviour changed | A change leaves a row edit, not a commit with a message and a reviewer | Audit added 2016; still no reason field |
| Testing a catalogue change before it takes effect | No preview mechanism; the first test is production | **None.** Proposed as the "change preview" control in `TAD-OPS-001 §13` |
| Reasoning about the code/data boundary | No principle, so it is empirical | Rule classification exercise in progress (`TD-02`) |

### Risks accepted 🔴

The 2003 record does not show these risks being identified, let alone accepted. They are
recorded here as risks the decision created, whether or not anyone weighed them at the time.

---

## Subsequent amendment — effective dating (2014-06) ✅ *Verified*

The original design stored a single current version of each package. Reprocessing a
historical order therefore applied current composition to a past transaction, and pre-2014
history is consequently not reproducible under current rules
([DLN-OPS-001 §7](../02-data/lineage-order-to-cash.md)).

Effective dating was added in 2014-06 under change `CHG-2014-0881` following an audit
finding on historical reporting reproducibility. `PRD_PKG`, `PRD_PKG_OPT`, `PRD_OPT`, and
`PRD_CMP_RUL` gained `EFF_FROM_DT` / `EFF_TO_DT`, and `ORDPKG03` was changed to look up
as-at the line's decode date.

**This amendment was never recorded as an ADR at the time.** It materially changed the
decision's consequences and is documented here rather than in a separate record because it
is inseparable from the original.

---

## Compliance and verification

| Aspect | Verification | Frequency | Owner |
| --- | --- | --- | --- |
| Decode reads reference data as-at the line's decode date, not current | Query comparison: re-decode a 2019 sample and compare to stored `ORD_LIN_DEC` | Annual | Order Data Steward |
| No package composition logic reintroduced into COBOL | Code review at each release; no `PRD_PKG` composition constants in source | Per release | Squad 1 Tech Lead |
| Reference data changes are audited | `PRD_AUD` row count reconciles with maintenance-screen transaction count | Monthly | Portfolio Management Lead |

---

## Re-evaluation triggers

> The most important section of a retrospective ADR. Two of the three original constraints
> have lapsed, so this decision is genuinely re-openable — but re-opening it means changing
> the mechanism, not returning to compiled constants.

| Trigger | Action |
| --- | --- |
| A further incident caused by an ungoverned reference data change | Escalate `TD-06`; the governance gap, not the data representation, is the problem |
| The rule classification exercise (`TD-02`) completes | Use the classification to state a principle for the code/data boundary, and record it as a new ADR |
| `ORDCMP04` is replaced or the decoder is rewritten | Re-assess whether the evaluator and the rules should both become data (a rules engine) |
| PLR → OPS versioned contract is delivered (`MOD-MER-001` slice 1) | The contract may supply the approval gate this decision lacks; supersede accordingly |

> **Note for a future modernization team:** the instinct on encountering
> business-user-editable production behaviour is to remove it. Do not. The lack of governance
> is the defect; the data representation is the reason 40 launches a year are possible, and
> the reason any historical decoding is reproducible. Add the gate, keep the mechanism.

---

## References

| Reference | Location | Survives |
| --- | --- | --- |
| DB2 migration Phase 2 impact analysis, 2003 | `archive/db2-migration-2003/phase2-impact.doc` | ✅ |
| Change `CHG-2014-0881` — effective dating | Change system | ✅ |
| 1999 catalogue lead-time audit | Referenced but not located | ❌ |
| INC-2025-0412 postmortem | Incident system | ✅ |
| `RDR-PLR-001` — reference data registry | [reference-data-option-codes.md](../02-data/reference-data-option-codes.md) | ✅ |
| Interview notes, retired Portfolio Manager | `archaeology/interviews/2025-03-plr.md` | ✅ |

---

## Change log

| Version | Date | Change |
| --- | --- | --- |
| 1.1.0 | 2026-01-14 | Added INC-2025-0412 to the observed negative consequences; added the note for a future modernization team |
| 1.0.0 | 2025-04-22 | Retrospective reconstruction |
