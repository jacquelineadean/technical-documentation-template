---
doc_id: RDR-PLR-001
title: Meridian — Reference Data and Code Set Registry
doc_type: rdr
status: approved
version: 2.3.0
owner: Portfolio Data Steward
reviewers: [Order Data Steward, Vendor Integration Lead, Data Architect]
approvers: [Director Portfolio Management]
created: 2025-01-20
last_reviewed: 2026-07-15
next_review: 2026-10-15
review_cycle: quarterly
classification: internal
systems: [MERIDIAN]
domains: [product-launch-readiness]
upstream_docs: [DGC-MER-001]
downstream_docs: [DD-OPS-001]
tags: [reference-data, code-sets, governance]
---

# Meridian — Reference Data and Code Set Registry

> **In a decoding-centric platform, the reference data *is* the business logic.** A new
> option code changes what can be ordered. A changed package composition changes what
> decodes. A retired code changes what fails. These are production behaviour changes, and in
> Meridian they are made by a business analyst through a maintenance screen with no
> approval, no preview, and no rollback.
>
> §6 is the finding this document exists to record.

---

## Contents

| Section | Summary |
| --- | --- |
| [1. Registry](#1-registry) | Seven code sets with volatility, ownership, effective dating, consumers |
| [2. Code set: `PRD_OPT` (CS-001)](#2-code-set-prd_opt-cs-001) | `PRD_OPT`: values, attributes, change process, consumers |
| [3. Effective dating](#3-effective-dating) | Which sets support point-in-time lookup, and the 2014-06 reprocessing boundary |
| [4. External code sets](#4-external-code-sets) | ISO standards in use, their version currency, and manual update processes |
| [5. Mapping between code sets](#5-mapping-between-code-sets) | Cross-set mappings and unmapped-value handling, including excluded packages |
| [6. Governance findings ⚠️](#6-governance-findings-) | Findings: no approval gate and no change preview on high-volatility sets |
| [Change log](#change-log) | Version, date, author, change |

---

## 1. Registry

| ID | Code set | Purpose | Values | Volatility | Owner | Eff-dated | Change process | Consumers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CS-001 | `PRD_OPT` | Option definitions | 14,200 active / 41,800 total | **High** | Portfolio Data Owner | ✅ | Maintenance screen, no gate | Decoder, dispatch, warehouse |
| CS-002 | `PRD_PKG` | Package definitions | 340 active / 4,100 total | **High** | Portfolio Data Owner | ✅ | Maintenance screen, no gate | Decoder, order entry, SPR |
| CS-003 | `PRD_PKG_OPT` | Package composition | 61,000 active rows | **High** | Portfolio Data Owner | ✅ | Maintenance screen, no gate | Decoder |
| CS-004 | `PRD_CMP_RUL` | Compatibility rules | 2,900 active | Medium | Portfolio Data Owner | ✅ | Maintenance screen, no gate | Decoder |
| CS-005 | `REF_HLD_CD` | Hold codes | 14 active / 19 total | Low | Order Data Owner | ❌ | Change request + release | Hold Service, dispatch, invoice |
| CS-006 | `REF_VND_RTE` | Vendor routing | 1,840 rules | Low | Vendor Integration Lead | ❌ | Change request + release | Dispatch |
| CS-007 | `REF_TIER` | Incentive tier curves | 48 (4 tiers × 12 programmes) | Low | Sales Data Owner | ✅ | Change request + release | Incentive calc |
| CS-008 | `REF_PGM` | Programme enrolment | 3,200 dealer × programme | Medium | Sales Data Owner | ❌ ⚠️ | Sales Ops screen | Eligibility, incentive |
| CS-009 | `REF_GL_MAP` | Product line → GL account | 62 | Low | Finance Controller | ❌ | Change request + release | GL interface |
| CS-010 | `REF_CARR_MAP` | Carrier code mapping | 210 | Low | Vendor Integration Lead | ❌ | Change request + release | ASN ingest |
| CS-011 | `REF.TAXCAT` (VSAM) | Tax category | 🔴 ~22 observed | Low | **Unassigned** ⚠️ | ❌ | **Direct VSAM edit by 2 named people** | Decoder → ERP tax |
| CS-012 | `REF_VOL_CLS` | Volumetric class ordering | 45 | Static | Portfolio Data Owner | ❌ | Change request + release | Decoder |
| CS-013 | `REF_ALW` | Allowance definitions | 180 | Medium | Finance Controller | ✅ | Change request + release | Invoicing |
| CS-014 | `REF_DLR_XREF` | Planning ↔ Meridian dealer mapping | 3,200 | Low | Sales Data Owner | ❌ | Sales Ops screen | Objective load |

**Volatility**

| Level | Change frequency | Governance implied | Sets |
| --- | --- | --- | --- |
| Static | Effectively never | A change is a project | CS-012 |
| Low | A few per year | Standard change process | CS-005, 006, 007, 009, 010, 014 |
| Medium | Monthly | Streamlined with notification | CS-004, 008, 013 |
| **High** | Weekly or more | Self-service **with controls and audit** | CS-001, 002, 003 |

> The three High sets have self-service without the controls. That is the gap.

---

## 2. Code set: `PRD_OPT` (CS-001)

| | |
| --- | --- |
| Purpose | Defines every option code that can appear in a package and the attributes that drive derivation |
| Physical location | `MERPROD.PRD_OPT` |
| Value count | 14,200 active, 41,800 total including superseded |
| Owner | Director, Portfolio Management |
| Steward | Portfolio Data Steward |
| Maintained via | PLR maintenance screen `PLR07`, and bulk load `PLR-BULK-010` at changeover |
| Effective-dated | ✅ since 2014-06 |
| Versioned | ✅ via effective ranges |
| Audited | ✅ `PRD_AUD` records user and timestamp — **but no reason** |
| Distribution | Read directly from DB2 by the decoder; no cache |
| Refresh latency | Immediate — a change is live at the next decode of any line |

### 2.1 Structure

| Attribute | Type | Required | Description | Constraints |
| --- | --- | --- | --- | --- |
| `OPT_CD` | `CHAR(8)` | ✅ | Option code | `^OPT-\d{4}$` |
| `OPT_DESC` | `VARCHAR(60)` | ✅ | Description shown to dealers | — |
| `OPT_CLS_CD` | `CHAR(1)` | ✅ | Class, drives volumetric derivation and the EU weight rule | `A`–`J` |
| `WGT` | `DECIMAL(7,2)` | ✅ | Weight in kg | ≥ 0 |
| `LEAD_DAYS` | `SMALLINT` | ✅ | Vendor lead time | 0–365 |
| `PRC_DELTA` | `DECIMAL(9,2)` | ✅ | Price adjustment vs. the base package | — |
| `EFF_FROM_DT` | `DATE` | ✅ | Effective from | — |
| `EFF_TO_DT` | `DATE` | — | Effective to; null = open-ended | — |
| `RESTR_FL` | `CHAR(1)` | ✅ | Restricted — triggers trade-compliance screening | `Y`/`N` |

### 2.2 Behaviour driven by this code set

| Attribute | Behaviour triggered | Implemented in | Rule | Confidence |
| --- | --- | --- | --- | --- |
| `OPT_CLS_CD = 'H'` + EU region | Derived weight × 1.15 | `ORDDRV07` | BR-OPS-062 | ✅ |
| `OPT_CLS_CD` | Volumetric class = max across options | `ORDDRV07` | BR-OPS-063 | ✅ |
| `LEAD_DAYS` | Lead-time band = longest across options | `ORDDRV07` | BR-OPS-066 | ✅ |
| `PRC_DELTA` | Contributes to `NET_AMT` recalculation | `ORDDEC01` | BR-OPS-070 | ✅ |
| `RESTR_FL = 'Y'` | Trade-compliance screening; may apply hold `TC02` | Hold Service | BR-OPS-024 | ✅ |
| **Row absent at `DEC_DT`** | **Decode fails**, exception `EXC-02` | `ORDPKG03` | BR-OPS-005 | ✅ |
| **Row retired before `DEC_DT`** | **Option silently omitted**, line still decodes | `ORDPKG03` | BR-OPS-004 | ✅ |

> The last two rows differ and the difference matters. A *missing* option fails the line
> loudly; a *retired* option disappears from it silently. Retiring an option therefore
> changes what dealers receive without anyone being told, which is exactly what happened in
> INC-2025-0412.

### 2.3 Consumers

| Consumer | How consumed | Cached | TTL | On an unknown code | Notice required |
| --- | --- | --- | --- | --- | --- |
| Decoder (`ORDPKG03`) | Direct DB2 read per line | ❌ | — | Decode fails, `EXC-02` | 0 days — immediate effect |
| Hold Service | DB2 read | ✅ | 5 min | Treated as unrestricted | 0 days |
| Order entry portal | DB2 read | ✅ | 15 min | Not offered to the dealer | 0 days |
| Dispatch (`ORDDSP01`) | DB2 read | ❌ | — | Uses stored decoded rows; unaffected | — |
| Enterprise Warehouse | Nightly dimension extract | ✅ | 24h | **Row loaded with a null description** | 1 day |
| Vendor EDI 850 | Option codes transmitted | — | — | **Vendor rejects with AK9 error** — 7 of 43 vendors validate against their own catalogue | **30 days** ⚠️ |

> The last row is the one that turns a reference data change into an external incident.
> Seven vendors maintain their own option catalogue and reject a code they have not been
> told about. Their contracts require 30 days' notice of a new code. The maintenance screen
> does not know this, and the notification is a manual step that a Portfolio analyst must
> remember.

### 2.4 Change process — current

| Change | Approval | Notice | Lead time | Testing | Effective-dating |
| --- | --- | --- | --- | --- | --- |
| Add an option | **None** | **None** | Immediate | **None** | Analyst sets `EFF_FROM_DT` |
| Change a description | None | None | Immediate | None | New effective range |
| **Change `PRC_DELTA`** | **None** | None | Immediate | None | New effective range |
| **Change `OPT_CLS_CD` or `WGT`** | **None** | None | Immediate | None | New effective range |
| **Retire an option** | None | None | Immediate | None | Analyst sets `EFF_TO_DT` |
| Reuse a retired code | **Prohibited by convention; not enforced** | — | — | — | — |

> **Code reuse is not enforced.** The maintenance screen permits creating a new `PRD_OPT` row
> with a previously-used `OPT_CD` and a fresh effective range. This has happened twice
> (2019, 2022); both times historical decoded rows became ambiguous between the old and new
> meaning. A uniqueness constraint across all effective ranges is a 1-day fix and is
> scheduled with the Q4 2026 remediation.

### 2.5 Change history — recent

| Date | Change | Codes | Reason | Approved by | Historical impact |
| --- | --- | --- | --- | --- | --- |
| 2026-07-02 | 340 added | `OPT-88xx` | 2027 model-year portfolio | *(none recorded)* | None |
| 2026-05-14 | 12 `PRC_DELTA` changes | Various | Mid-year price adjustment | *(none recorded)* | `NET_AMT` recalculated on any re-decode of affected lines |
| 2026-03-08 | 1 retired | `OPT-4419` | Supplier discontinued | *(none recorded)* | Lines decoding after this date silently omit it |
| **2025-04-02** | **1 removed from a package** | `OPT-2207` | **Analyst error — intended to retire the option, removed it from the package instead** | *(none recorded)* | **INC-2025-0412.** 1,840 lines re-decoded without a component the dealers had ordered; USD 310k |

---

## 3. Effective dating

| Code set | Eff-dated | Historical values retained | Point-in-time lookup | Reprocessing accurate |
| --- | --- | --- | --- | --- |
| CS-001 `PRD_OPT` | ✅ | ✅ | ✅ | ✅ **for `DEC_DT` ≥ 2014-06-01** |
| CS-002 `PRD_PKG` | ✅ | ✅ | ✅ | ✅ same caveat |
| CS-003 `PRD_PKG_OPT` | ✅ | ✅ | ✅ | ✅ same caveat |
| CS-004 `PRD_CMP_RUL` | ✅ | ✅ | ✅ | ✅ same caveat |
| CS-007 `REF_TIER` | ✅ | ✅ | ✅ | ✅ |
| CS-013 `REF_ALW` | ✅ | ✅ | ✅ | ✅ |
| **CS-008 `REF_PGM`** | ❌ | ❌ **overwritten** | ❌ | ❌ **Breaks incentive reproducibility** — `DI-2025-031` |
| CS-005 `REF_HLD_CD` | ❌ | ❌ | ❌ | Hold behaviour on a re-run uses current definitions |
| **CS-011 `REF.TAXCAT`** | ❌ | ❌ | ❌ | ❌ **Regulatory data; a re-decode applies today's tax categories** |

**Point-in-time lookup pattern** — used by `ORDPKG03`:

```sql
SELECT o.OPT_CD, o.OPT_CLS_CD, o.WGT, o.LEAD_DAYS, o.PRC_DELTA
FROM   PRD_PKG_OPT po
JOIN   PRD_OPT     o  ON o.OPT_CD = po.OPT_CD
WHERE  po.PKG_CD   = :pkg_cd
AND    :dec_dt    >= po.EFF_FROM_DT
AND    (:dec_dt    < po.EFF_TO_DT OR po.EFF_TO_DT IS NULL)
AND    :dec_dt    >= o.EFF_FROM_DT
AND    (:dec_dt    < o.EFF_TO_DT  OR o.EFF_TO_DT  IS NULL);
```

> Note the half-open interval `[EFF_FROM_DT, EFF_TO_DT)`. Consistency in this convention
> matters: a closed-closed interval elsewhere would double-count on the changeover date.
> `DQ-PLR-007` asserts no overlapping ranges per `(PKG_CD, OPT_CD)`.

---

## 4. External code sets

| Code set | Standard | Source | Version in use | Latest | Update process | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| Country | ISO 3166-1 alpha-2 | ISO | 2020 edition | 2024 | **Manual, ad hoc** | Vendor Integration Lead |
| Currency | ISO 4217 | ISO | 2018 edition | 2024 | Manual, ad hoc | Finance Controller |
| EDI transaction sets | X12 | ANSI ASC X12 | 004010 | 008030 | Frozen — vendor contracts specify 004010 | Vendor Integration Lead |
| Carrier SCAC | NMFTA | NMFTA | 2023 | 2026 | Annual manual refresh | Vendor Integration Lead |

**Local extensions to external standards** ⚠️

| Standard | Extension | Reason | Risk |
| --- | --- | --- | --- |
| ISO 3166 | `XK` used for a territory before it was officially assigned | Needed a code in 2011 | ISO has since assigned `XK` unofficially for the same territory — **coincidentally compatible**, but it was luck |
| X12 `REF` qualifier | `ZZ` sub-qualifiers `ZZ01`–`ZZ09` for Meridian-specific references | X12 has no suitable qualifier | Low — `ZZ` is the designated mutually-defined qualifier |
| SCAC | 6 internal pseudo-carriers `MER1`–`MER6` | Vendor-managed transport with no SCAC | **Medium** — a real SCAC could be assigned these values |

---

## 5. Mapping between code sets

| From | To | Mapping | Cardinality | Maintained by | Unmapped handling |
| --- | --- | --- | --- | --- | --- |
| `PRD_PKG` | SPR reporting package | `SLS_PKG_MAP` | N:1 | Sales Data Steward | **Unmapped packages are excluded from attainment.** 47 unmapped at the 2025 changeover peak |
| Planning dealer id | `DLR_CD` | `REF_DLR_XREF` | 1:1 | Sales Data Steward | Objective row rejected |
| Vendor carrier code | SCAC | `REF_CARR_MAP` | N:1 | Vendor Integration Lead | Stored as `'UNK'` |
| Product line | GL account | `REF_GL_MAP` | N:1 | Finance Controller | **GL posting fails** — halts `FIN-GL-080` |

> `SLS_PKG_MAP` is the anti-corruption layer between PLR and SPR
> ([DMAP-MER-001 §2](../00-foundations/domain-map.md)). It drifts during changeover, when
> PLR adds packages faster than SPR maps them, and every unmapped package silently removes
> volume from dealer attainment. `DQ-SPR-009` alerts above 5 unmapped.

---

## 6. Governance findings ⚠️

| ID | Finding | Code sets | Risk | Remediation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RF-01 | **No approval gate on high-volatility sets.** A single analyst can change decoding behaviour for 3,200 dealers | CS-001, 002, 003, 004 | Caused INC-2025-0412, USD 310k | Approval workflow in the maintenance screen | Portfolio Data Owner | **Funded Q4 2026** |
| RF-02 | **No change preview.** The first test of a change is production | CS-001, 002, 003, 004 | As above | Re-decode the prior night against the proposed change and report the delta | Portfolio Data Owner | **Funded Q4 2026** |
| RF-03 | **No reason recorded.** `PRD_AUD` captures who and when, not why | CS-001–004 | Cannot explain a behaviour change after the fact | Add a mandatory reason field | Portfolio Data Steward | Funded Q4 2026 |
| RF-04 | **Code reuse not enforced** | CS-001, 002 | Historical data permanently ambiguous; happened twice | Uniqueness constraint across effective ranges | Portfolio Data Steward | 1 day, scheduled |
| RF-05 | **`REF.TAXCAT` has no owner** and is edited directly in VSAM by two named individuals | CS-011 | Regulatory data with no governance, no audit, no effective dating | Assign an owner; migrate to DB2 (`TD-04`) | Data Governance Lead | **Open — no owner assigned** |
| RF-06 | **`REF_PGM` not effective-dated** | CS-008 | Breaks incentive reproducibility; failed the 2026-07 audit test | Snapshot enrolment per period | Sales Data Steward | 2027-Q1 |
| RF-07 | **Vendor notification is manual** | CS-001 | A new option code can reach 7 validating vendors with no notice, breaching a 30-day contractual term | Add consumers to the change workflow | Vendor Integration Lead | Part of RF-01 |
| RF-08 | **48th rule type would be silently ignored** | CS-004 | The evaluator's loop bound is a compiled constant of 47 | Fix the constant | Squad 1 Tech Lead | `DEF-2026-0341`, 2 days |

### Checks run 2026-07-15

| Check | Result |
| --- | --- |
| Every code set has a named owner | ❌ **13 of 14** — CS-011 unassigned (RF-05) |
| Every code set's changes are audited | ❌ 12 of 14 — CS-011 and CS-008 not audited |
| Every code set used in a calculation is effective-dated | ❌ 6 of 9 calculation-relevant sets |
| No consumer abends on an unknown code | ⚠️ 7 vendors reject; `FIN-GL-080` halts on an unmapped GL account |
| Retired codes never reused | ⚠️ Convention only; 2 historical violations |
| Values in use match values registered | ✅ — see below |
| Consumer caches have a bounded refresh | ✅ All caches ≤ 24h |

**Undocumented values in production** — run quarterly as a query:

```sql
SELECT DISTINCT d.OPT_CD
FROM   ORD_LIN_DEC d
LEFT   JOIN PRD_OPT o ON o.OPT_CD = d.OPT_CD
WHERE  o.OPT_CD IS NULL;
```

| Run | Undocumented codes found | Notes |
| --- | --- | --- |
| 2026-07-15 | **0** | ✅ |
| 2026-04-12 | 3 | `OPT-9901`–`9903`; created and hard-deleted by an analyst rather than retired. Decoded rows survived the delete |
| 2026-01-14 | 0 | — |

> The April result is instructive: a hard delete from `PRD_OPT` left 2,100 `ORD_LIN_DEC`
> rows referencing codes that no longer exist, and the only reason anyone noticed was this
> query. The maintenance screen now soft-deletes by setting `EFF_TO_DT`; the hard-delete
> path was removed in `R2026.05`.

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 2.3.0 | 2026-07-15 | Portfolio Data Steward | Quarterly review. Added RF-08; recorded the Q2 undocumented-code finding and the hard-delete fix; added the vendor notification consumer risk (RF-07) |
| 2.2.0 | 2026-04-16 | Portfolio Data Steward | Added the undocumented-values query and its results |
| 2.0.0 | 2025-06-11 | Data Governance Office | Added §6 governance findings after INC-2025-0412 |
| 1.0.0 | 2025-01-20 | Portfolio Data Steward | Initial registry |
