---
doc_id: GUIDE-001
title: Documentation Standards
doc_type: guide
status: approved
version: 1.0.0
owner: Documentation Architect
classification: internal
last_reviewed: 2026-09-12
next_review: 2027-03-12
review_cycle: semi-annual
tags: [meta, style]
---

# Documentation Standards

House style for every document in this repository. Reviewers cite section numbers from here
rather than re-litigating style in each PR.

---

## 1. Structure

### 1.1 File naming

`kebab-case.md`, descriptive, no dates, no version numbers in the filename.

| Good | Bad | Why |
| --- | --- | --- |
| `icd-vendor-dispatch-outbound.md` | `ICD_Vendor_Dispatch_v3_FINAL.md` | Version lives in front matter; git holds history |
| `lineage-order-to-cash.md` | `lineage1.md` | Filename should survive out of context |
| `adr-0007-order-hold-externalization.md` | `adr-hold.md` | ADRs are sequenced and immutable |

### 1.2 Headings

One `#` H1 per document, matching the front-matter `title`. Sections numbered when the
document is long enough to be cited by section (TAD, ICD, Lineage, Governance Charter).
Numbering makes "see §7.3" possible in a review comment or an incident bridge.

### 1.3 Length

If a document exceeds ~2,500 words, it is usually two documents. The exceptions — TAD,
Data Lineage, Data Governance Charter, ICD — are exceptions because splitting them would
break a contract or a chain of reasoning.

---

## 2. Voice and tone

- **Present tense, active voice, indicative mood.** "The decoder rejects the line", not
  "the line will be rejected by the decoder".
- **Name the actor.** "Nightly job `ORD-DISPATCH-010` writes...", not "the data is written".
- **Prefer the concrete.** "Fails after 3 retries over 90 seconds" beats "retries a few
  times". If you do not know the number, say so with a confidence tag — do not round to a
  vague adjective.
- **No marketing.** "Robust, scalable, best-in-class" are not properties. Write the NFR.
- **Second person only in runbooks and procedures.** Everywhere else, third person.

---

## 3. Confidence levels

> **This is the single most important convention in this repository.**

Documenting a legacy system means writing down a mix of verified fact, reasonable
inference, and outright guess. When these are visually identical, readers eventually
distrust the whole document and go back to reading code — which is the failure mode this
repository exists to prevent.

Tag any assertion about existing system behaviour that is not trivially observable:

| Tag | Meaning | Evidence required |
| --- | --- | --- |
| `✅ Verified` | Confirmed against a primary source | Code reference, production trace/log sample, test result, or database query — cite it |
| `🟡 Inferred` | Derived logically from indirect evidence | State the evidence and the inference chain |
| `🔴 Assumed` | Believed, but unconfirmed | State who believes it and what would confirm it |

**Usage in prose:**

> Orders on a credit hold are excluded from the nightly dispatch extract.
> `✅ Verified` — `ORDDSP01.CBL:1204-1238`, and confirmed by 2026-08-14 production extract
> (0 of 1,284 held orders present).

**Usage in tables:** add a `Confidence` column.

| Rule | Behaviour | Confidence | Evidence |
| --- | --- | --- | --- |
| BR-OPS-014 | Hold `CR01` blocks dispatch | ✅ Verified | `ORDDSP01.CBL:1204` |
| BR-OPS-015 | Hold `CR01` does not block invoicing | 🟡 Inferred | No hold check in `INVGEN02`; not observed in production because CR01 releases pre-invoice |
| BR-OPS-016 | Hold `CR09` is obsolete | 🔴 Assumed | No rows since 2019-03; original owner has left; confirm with Credit Operations |

**Rules of use:**

- Every `🔴 Assumed` item needs a named person or role who can confirm it, and an open
  action. An assumption with no path to resolution is a defect in the document.
- Promote tags when evidence appears; never silently drop one.
- `✅ Verified` without a citation is not verified. Reviewers should reject it.

---

## 4. Tables

- Header row always. Pipe-aligned source is not required, but columns must be consistent.
- **Every table with more than ~8 rows needs a stable identifier column** (rule ID, field
  ID, interface ID) so rows can be referenced from elsewhere and tracked across versions.
- Empty cells use `—`, never blank. A blank cell is ambiguous between "none" and "unknown";
  use `—` for none and `🔴 Unknown` for unknown.
- Units in the header, not repeated in each cell: `Latency (p99, ms)`.

---

## 5. Identifiers

Identifiers are the backbone of a large corpus: they let a test case cite a business rule,
a code comment cite a decision, and an impact assessment enumerate what it touches.

| Kind | Format | Example |
| --- | --- | --- |
| Document | `<TYPE>-<SCOPE>-<NNN>` | `TAD-OPS-001` |
| Business rule | `BR-<DOMAIN>-<NNN>` | `BR-OPS-014` |
| Non-functional requirement | `NFR-<CATEGORY>-<NNN>` | `NFR-PERF-003` |
| Interface | `IF-<NNN>` | `IF-042` |
| Data element | `DE-<ENTITY>-<NNN>` | `DE-ORDLN-017` |
| Lineage hop | `<LINEAGE-ID>-H<N>` | `DLN-001-H4` |
| Risk | `RISK-<NNN>` | `RISK-011` |
| Assumption | `ASM-<NNN>` | `ASM-006` |
| Open question | `Q-<NNN>` | `Q-019` |

Identifiers are **immutable and never reused**. A retired rule keeps its ID with
`status: retired`; the next rule takes the next number. Reusing `BR-OPS-014` for something
new silently invalidates every test and code comment that cites it.

Scope codes are registered in [`03-front-matter-schema.md`](03-front-matter-schema.md).

---

## 6. Cross-references

- **Link, do not copy.** Duplicated facts diverge. The only acceptable duplication is a
  one-line summary immediately adjacent to a link to the authority.
- Use relative paths (`../02-data/data-dictionary.md`), validated by CI.
- When citing a section, use the document ID and section number: `TAD-OPS-001 §7.3`.
- When a document depends on another, declare it in front matter (`upstream_docs`) so
  impact analysis can traverse the graph mechanically.

### Citing source code

`<repository>/<path>:<line-range>` plus the commit or release the reading was taken at —
line numbers drift:

> `meridian-core/src/decode/ORDDEC01.CBL:412-478` (as of release `R2026.03`)

---

## 7. Numbers, dates, and units

- Dates: ISO-8601 (`2026-09-12`). Never `09/12/26`.
- Times: 24-hour with an explicit timezone (`02:30 UTC`). Batch windows in a legacy system
  are a classic source of timezone defects — always state the zone, and state whether the
  schedule observes daylight saving.
- Currency: ISO-4217 code with the amount (`USD 1,250.00`).
- Data volumes: state the unit and the period (`~1.2M order lines/day, peak 4.1M`).
- Percentiles, not averages, for latency. An average latency figure in an NFR is a defect.

---

## 8. Diagrams

Full conventions in [`02-diagram-conventions.md`](02-diagram-conventions.md). The rules that
belong to *style* rather than notation:

- Every diagram has a caption stating what the reader should conclude from it.
- Every diagram is accompanied by prose. A diagram is never the sole carrier of a fact — it
  cannot be searched, quoted in an incident, or read by a screen reader.
- Maximum ~15 nodes. Beyond that, decompose.

---

## 9. What must never appear in a document

| Never | Instead |
| --- | --- |
| Credentials, tokens, keys, connection strings | Name the secret and where it is stored (`vault://meridian/prod/edi-sftp-key`) |
| Personal data in examples | Synthetic data, clearly labelled |
| Internal hostnames/IPs in partner-facing documents | Logical service names; environment specifics in the deployment document |
| Individual names as owners | Roles. People change jobs; roles persist |
| "TBD" with no owner or date | `🔴 Assumed` / `Q-<NNN>` with an owner and target date |
| Un-scoped superlatives ("real-time", "highly available") | The measured NFR with its budget |

---

## 10. Review expectations

Every document PR is reviewed against [`08-review-checklists.md`](08-review-checklists.md).
Reviewers are asked to check three things above all:

1. **Could a competent newcomer act on this without asking a question that the document
   should have answered?**
2. **Is every claim about existing behaviour either obviously checkable or confidence-tagged
   with evidence?**
3. **Does any fact here belong in a different layer?**
