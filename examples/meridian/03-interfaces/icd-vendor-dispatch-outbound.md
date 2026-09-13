---
doc_id: ICD-VND-001
title: Vendor Dispatch Outbound (EDI 850) — Interface Control Document
doc_type: icd
status: approved
version: 4.2.0
owner: Vendor Integration Lead
reviewers: [Integration Lead, Order Management Architecture Lead, SRE Lead]
approvers: [Vendor Integration Lead, VP Order Operations]
created: 2024-05-22
last_reviewed: 2026-07-30
next_review: 2027-01-30
review_cycle: semi-annual
classification: confidential
systems: [MERIDIAN]
domains: [order-processing, vendor-integration]
upstream_docs: [ICAT-MER-001, TAD-OPS-001]
downstream_docs: [DLN-OPS-001, RUN-OPS-001]
related_interfaces: [IF-042, IF-043, IF-044]
tags: [interface, icd, edi, x12, vendor]
---

# Vendor Dispatch Outbound (EDI 850) — Interface Control Document

> **Classification `confidential`:** the payload carries dealer net pricing.
>
> **Two versions.** This document is v4.2.0. The **interface** is v3.1, unchanged since
> 2023-11. Conflating the two makes vendors believe the interface changed when only the
> prose did.

---

## 1. Identification

| | |
| --- | --- |
| Interface ID | `IF-042` |
| Interface name | Vendor Dispatch Outbound |
| **Interface version** | **3.1** (effective 2023-11-06) |
| Status | Live |
| Direction | Outbound |
| Pattern | Batch file (EDI) |
| Criticality | **Tier 1** |
| Live since | 2014-09 |
| Sunset date | — |

### Parties

| | Producer | Consumer |
| --- | --- | --- |
| Organisation | *(this organisation)* | 43 fulfilment vendors |
| System | Meridian OPS Batch Suite | Vendor WMS / ERP |
| Accountable role | Vendor Integration Lead | Each vendor's nominated integration contact |
| Technical contact | `#meridian-edi` | Per vendor, in the partner register |
| Support contact | Meridian SRE on-call | Per vendor, 24×7 for Tier 1 vendors |
| Escalation | Head of Supply Chain Systems | Vendor account manager |
| Change approval | Vendor Integration Lead | Each vendor, individually |

### Business purpose

Instructs a fulfilment vendor to pick, pack, and ship the units on a dispatched order line.
It is the only mechanism by which anything physically ships.

| | |
| --- | --- |
| Business process | Order fulfilment — [DOM-OPS-001 §7](../04-domains/order-processing.md) |
| Impact if unavailable 1 hour | None if within the window; the file is built once nightly |
| Impact if the 03:00 cutoff is missed | **A full fulfilment day lost for ~18,000 orders.** Contractual lead-time breaches with 11 of 43 vendors |
| Impact of bad data transmitted | Wrong goods shipped to dealers. Recovery involves vendor contact, stop-ship where possible, and return logistics. Cannot be recalled once the vendor has picked |

---

## 2. Transport

| | |
| --- | --- |
| Protocol | AS2 (31 vendors) or SFTP (12 vendors) |
| Endpoint | Per vendor; logical names in the partner register. Environment-specific values in `DEP-MER-001` |
| Authentication | AS2: mutual TLS with vendor certificates. SFTP: SSH key pair, IP allowlisted |
| Encryption in transit | AS2: TLS 1.2+ with payload encryption and signature. SFTP: SSH transport |
| Encryption at rest | Archive files encrypted at rest on z/OS |
| IP allowlisting | Both directions, per vendor |
| Certificates | AS2 signing and encryption certificates per vendor; see §2.1 |
| Network path | Via the DMZ vendor gateway (Sterling B2B Integrator) |
| Firewall rules | Per vendor, reviewed annually |

### 2.1 Certificates and keys

| Item | Count | Expiry monitoring | Renewal owner | Oldest |
| --- | --- | --- | --- | --- |
| AS2 signing certificates (vendor) | 31 | ✅ Alert at 60 and 30 days | Vendor Integration Lead | Expires 2026-11-14 |
| AS2 encryption certificates (ours) | 1 | ✅ | Vendor Integration Lead | Expires 2027-04-02 |
| SFTP SSH keys (ours, per vendor) | 12 | ⚠️ **No expiry; rotation is manual** | Vendor Integration Lead | **Created 2021-08** — `TD-09` |

> Three SSH keys are over four years old and there is no rotation schedule. `TD-09` in
> `TAD-OPS-001 §17`. Certificate expiry is the most common cause of established partner
> interfaces failing, and the SSH side of this interface has no automated defence.

### 2.2 Environments

| Environment | Endpoint | Credentials | Vendors available | Notes |
| --- | --- | --- | --- | --- |
| Production | Per vendor | Production certificates | 43 | — |
| Pre-production | Per vendor sandbox | Separate certificates | **4** | Only 4 vendors operate a sandbox |
| Test / certification | Sterling test adapter | Test certificates | 43 (loopback) | Validates our output; does not validate vendor parsing |

> **Only 4 of 43 vendors have a sandbox.** For the other 39, the first real test of a change
> is production. This is the single largest parity gap in the estate and is why the
> certification scenarios in §12 include a loopback validation that at least proves our
> output conforms.

---

## 3. Timing and volume

| | |
| --- | --- |
| Frequency | Once nightly, per vendor |
| Schedule | Built 23:50–00:35 UTC by `ORD-DISPATCH-040`; transmitted 00:35–00:45 by `EDI-TRANSMIT-050` |
| Trigger | Predecessor job completion |
| **Cutoff** | **03:00 UTC** |
| Cutoff driver | Vendor master agreement §7.2 — vendors commit to same-day pick for files received by 03:00 |
| Timezone | UTC. **Daylight saving is not observed**, so the local receipt time shifts by an hour twice a year for European vendors |

| Volume | Records | Size | Notes |
| --- | --- | --- | --- |
| Typical, per vendor | 410 | ~180 KB | Median across 43 vendors |
| Typical, total | 17,600 | ~7.7 MB | |
| Peak, per vendor | 2,900 | ~1.3 MB | Largest vendor at changeover |
| Peak, total | 62,000 | ~27 MB | |
| Peak driver | Model-year changeover coinciding with month-end | | |
| Maximum supported | 9,999 per file | 10 MB per file | `CTT-01` is `N0(6)`; file size is a vendor gateway limit |
| **Zero-volume** | **Expected and permitted** | ~2 KB | ~6 vendors per night have no dispatches. See §3.1 |

### 3.1 Empty file semantics

A vendor with no dispatches receives a file containing `ISA`/`GS`/`ST`, a `BEG` segment, a
`CTT` with counts of zero, and the closing envelopes — **not** an absent file.

> This is deliberate and it is the control that distinguishes "nothing to send" from "the
> job failed". A vendor that receives no file at all knows something is wrong; a vendor that
> receives an empty file knows the night was quiet. Six vendors initially rejected empty
> files during onboarding; all now accept them, and it is a mandatory certification scenario
> (§12, C-04).

### 3.2 Calendar

| Aspect | Detail |
| --- | --- |
| Transmission days | 7 days a week, including holidays |
| Vendor holidays | Vendors' own holiday handling; files are still sent and are processed on their next working day |
| Our holidays | No effect — the batch runs daily |
| Exceptions | 4-day year-end change freeze affects changes, not transmission |

---

## 4. Payload

### 4.1 Structure

| | |
| --- | --- |
| Format | ANSI ASC X12, version 004010, transaction set 850 (Purchase Order) |
| Implementation guide | `edi/meridian-850-v3.1.pdf` |
| Character encoding | ASCII (basic character set) |
| Segment terminator | `~` (0x7E) |
| Element separator | `*` (0x2A) |
| Sub-element separator | `>` (0x3E) |
| Line terminator | None — segments are terminated, not line-delimited |
| Decimal representation | Explicit decimal point where the element permits; implied decimal on `PO1-04` |
| Date format | `CCYYMMDD` |
| Negative numbers | Leading minus. **Not used on this interface** |
| Maximum size | 10 MB |
| Compression | None |

### 4.2 Envelope and structure

```
ISA  Interchange control header          (1)
 GS  Functional group header             (1)
  ST  Transaction set header             (1 per order)
   BEG Beginning segment                 (1)
   REF Reference identification          (1..5)
   DTM Date/time reference               (1..3)
   N1  Ship-to name loop                 (1..2)
   PO1 Baseline item data                (1..9999)
    PID Product description              (0..1)
    MEA Measurements                     (0..2)
    REF Line reference                   (1..3)
   CTT Transaction totals                (1)
  SE  Transaction set trailer            (1)
 GE  Functional group trailer            (1)
IEA  Interchange control trailer         (1)
```

| Level | Occurrence | Purpose |
| --- | --- | --- |
| Interchange (`ISA`/`IEA`) | 1 per file | Sender, receiver, control number, test/production flag |
| Group (`GS`/`GE`) | 1 per file | Functional group |
| Transaction (`ST`/`SE`) | **1 per order** | One 850 per Meridian order, not per file |
| Item (`PO1`) | 1..9999 per transaction | One per dispatched order line |

> One transaction set per **order**, not per line and not per file. A vendor receiving 410
> lines across 180 orders receives 180 `ST`/`SE` transaction sets in one interchange. This
> is the most common misunderstanding during onboarding.

### 4.3 Field specification

**`ISA` — interchange control header**

| # | Element | Pos | Type | Len | Req | Valid values | Example |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Authorization info qualifier | ISA01 | ID | 2 | M | `00` | `00` |
| 5 | Interchange ID qualifier (sender) | ISA05 | ID | 2 | M | `ZZ` | `ZZ` |
| 6 | Interchange sender ID | ISA06 | AN | 15 | M | `MERIDIANPROD  ` (space-padded) | `MERIDIANPROD  ` |
| 7 | Interchange ID qualifier (receiver) | ISA07 | ID | 2 | M | `ZZ` or `01` (DUNS) | `ZZ` |
| 8 | Interchange receiver ID | ISA08 | AN | 15 | M | Per vendor, in the partner register | `VENDOR07      ` |
| 9 | Interchange date | ISA09 | DT | 6 | M | `YYMMDD`, UTC | `260612` |
| 10 | Interchange time | ISA10 | TM | 4 | M | `HHMM`, UTC | `0035` |
| 13 | Interchange control number | ISA13 | N0 | 9 | M | Monotonic per vendor; see §4.6 | `000018472` |
| 14 | Ack requested | ISA14 | ID | 1 | M | `1` — 997 required | `1` |
| 15 | **Test indicator** | ISA15 | ID | 1 | M | `P` production, `T` test | `P` |

**`PO1` — baseline item data** *(one per dispatched order line)*

| # | Element | Pos | Type | Len | Req | Description | Valid values | Example |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Assigned identification | PO1-01 | AN | 20 | M | `DSP_INS.DSP_ID` — the idempotency key for the whole chain | `DSP\d{6}V\d{2}-\d{5}` | `DSP260612V07-00891` |
| 2 | Quantity ordered | PO1-02 | R | 9 | M | `ORD_LIN.QTY` | 1–9999 | `12` |
| 3 | Unit of measure | PO1-03 | ID | 2 | M | Always `EA` | `EA` | `EA` |
| 4 | **Unit price** | PO1-04 | R | 14 | M | `ORD_LIN.NET_AMT` × 100, **implied 2 decimals** | ≥ 0 | `125000` |
| 6 | Product ID qualifier | PO1-06 | ID | 2 | M | `VP` vendor part number | `VP` | `VP` |
| 7 | Product ID | PO1-07 | AN | 48 | M | `ORD_LIN.MDL_PKG_CD` | See [RDR-PLR-001](../02-data/reference-data-option-codes.md) | `MP2026STD-A4471X` |
| 8 | Product ID qualifier | PO1-08 | ID | 2 | C | `ZZ` when option codes follow | `ZZ` | `ZZ` |
| 9 | Product ID | PO1-09 | AN | 48 | C | Option codes, `>`-separated, from `ORD_LIN_DEC` | — | `OPT-4402>OPT-7710>OPT-1120>OPT-9003` |

> **`PO1-04` carries an implied 2-decimal value.** `USD 1,250.00` is transmitted as `125000`.
> Three onboarding defects have been caused by a vendor treating it as a plain decimal,
> producing a 100× price. It is a mandatory certification scenario (§12, C-08).

**`MEA` — measurements**

| # | Element | Pos | Type | Len | Req | Description | Example |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Measurement reference | MEA-01 | ID | 2 | M | `PD` physical dimensions | `PD` |
| 2 | Measurement qualifier | MEA-02 | ID | 3 | M | `G` gross weight | `G` |
| 3 | Measurement value | MEA-03 | R | 20 | M | `ORD_LIN.DRV_WGT`. **Converted kg → lb (× 2.20462) for the 9 US vendors**, 1 decimal | `2755.8` |
| 4 | Unit of measure | MEA-04 | ID | 2 | M | `KG` or `LB` per vendor | `LB` |

**`CTT` — transaction totals**

| # | Element | Pos | Type | Len | Req | Description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Number of line items | CTT-01 | N0 | 6 | M | Count of `PO1` segments in this transaction set |
| 2 | Hash total | CTT-02 | R | 10 | M | Sum of `PO1-02` (quantities) in this transaction set |

**Optionality**

| Code | Meaning |
| --- | --- |
| M | Mandatory — always present with a value |
| O | Optional — may be absent |
| C | Conditional — required when the stated condition holds |

### 4.4 Null, empty, and absent

| State | Representation | Meaning |
| --- | --- | --- |
| Not applicable | Element omitted (consecutive separators) | The data point does not apply to this line |
| Not known | **Never transmitted.** A line with unknown mandatory data is not dispatched | — |
| Zero | `0` | A genuine zero — occurs only on `CTT` for an empty file |
| Absent optional element | Omitted | Same as not applicable |

> **Meridian never transmits an empty mandatory element.** A line missing mandatory data
> fails validation at build time and the whole file aborts, rather than transmitting a
> partial record. This follows from the integrity priority in `TAD-OPS-001 §2.3`.

### 4.5 Semantics

| Field | Semantic definition |
| --- | --- |
| `PO1-01` `DSP_ID` | The dispatch instruction identity. **Echoed exactly in the 997 and the 856**, case-sensitive, no trimming. It is the correlation key for the entire downstream chain |
| `PO1-02` quantity | Units of the **package**, not physical units. For product lines C and E one package contains multiple physical units |
| `PO1-04` price | Dealer net price per package, excluding tax, after portfolio discounts. **Confidential** |
| `PO1-07` product | The model package code as at the line's decode date. A vendor's catalogue lookup must be effective-dated to match |
| `PO1-09` options | The **decoded** option set including auto-added options (`DEC_SRC_CD = 'A'`), not the options the dealer selected |
| `DTM` 002 | Requested delivery date. **Advisory** — not a commitment, and vendors are not measured against it |
| `DTM` 010 | Requested ship date. **This is the committed date** against which vendor lead-time performance is measured |

> `PO1-09` carries the decoded option set, which can include options the dealer did not
> order — the required-option auto-add under BR-OPS-009. Vendors ship what this element says.
> This is correct behaviour and it is stated here because it looks like a defect.

### 4.6 Control numbers

| Aspect | Detail |
| --- | --- |
| `ISA13` interchange control number | Monotonically increasing per vendor, starting from 1 |
| Range | 1 to 999,999,999. At ~365/year per vendor, exhaustion is not a practical concern |
| Reset policy | **Never reset.** A reset would make historical interchanges ambiguous |
| Gap handling | A gap indicates a lost transmission and triggers investigation by both sides |
| Duplicate handling | A repeated control number is **rejected** by the vendor per X12 rules |
| Storage | `EDI_CTL_NO` table, per vendor, updated transactionally with the transmission |

### 4.7 Example payload

```
ISA*00*          *00*          *ZZ*MERIDIANPROD  *ZZ*VENDOR07      *260612*0035*U*00401*000018472*0*P*>~
GS*PO*MERIDIANPROD*VENDOR07*20260612*0035*18472*X*004010~
ST*850*0001~
BEG*00*SA*ORD260610X447**20260610~
REF*ZZ*MERIDIAN~
DTM*010*20260619~
DTM*002*20260626~
N1*ST*DEALER 04471*92*04471~
PO1*DSP260612V07-00891*12*EA*125000**VP*MP2026STD-A4471X*ZZ*OPT-4402>OPT-7710>OPT-1120>OPT-9003~
PID*F****Standard package, model year 2026~
MEA*PD*G*2755.8*LB~
REF*ZZ*LINE0003~
CTT*1*12~
SE*11*0001~
GE*1*18472~
IEA*1*000018472~
```

**Edge-case examples**

| Case | Key characteristics |
| --- | --- |
| Empty file | `ST`/`BEG`/`CTT*0*0`/`SE`; no `PO1` segments |
| Maximum quantity | `PO1*...*9999*EA*...` |
| Zero price | `PO1-04` = `0` — occurs on warranty replacement orders (`ORD_TYP_CD = 'WT'`) |
| Maximum options | `PO1-09` with 5 option codes, 48-character limit reached |
| Multi-line order | One `ST`/`SE` with several `PO1` segments and a `CTT` counting all of them |

---

## 5. Processing semantics

| Aspect | Behaviour |
| --- | --- |
| Delivery guarantee | At-least-once. Transport retries can duplicate a transmission |
| Ordering | **None guaranteed** between transaction sets. Vendors must not rely on `PO1` order |
| Duplicate handling | Vendor de-duplicates on `ISA13`; within a file, on `PO1-01` `DSP_ID` |
| Out-of-order handling | Not applicable — each dispatch is independent |
| **Partial processing** | **Not permitted.** A vendor accepts or rejects the whole interchange |
| Replay | Supported by agreement only — requires a **new** `ISA13` and vendor coordination. Never a bare retransmission |
| Replay window | 7 days from the archive |
| Late arrival | A file arriving after 03:00 is processed on the vendor's next working day; same-day pick is not committed |
| Acknowledgement | Three distinct levels — §5.1 |

### 5.1 Acknowledgement semantics ⚠️

| Ack | Means | Timing | Absence means |
| --- | --- | --- | --- |
| **AS2 MDN / SFTP transfer completion** | **Bytes received.** Nothing about content | Seconds | Transport failure; retry |
| **997 functional acknowledgement** | **Parsed and structurally valid.** Nothing about business acceptance | ≤ 4 hours | Hold `DS07`; retry then escalate |
| **856 ASN** | **Acted upon** — goods handed to a carrier | 4–11 days | Nothing automated today — `FM-05` |

> **These are three different statements and conflating them is the classic cause of "we sent
> it, they say they never got it".** A 997 with `AK5*A` means the vendor's EDI layer parsed
> the file, and nothing more. The dangerous case is a vendor whose EDI layer accepts and
> whose warehouse system rejects: Meridian believes the order is dispatched, no alert fires,
> and the gap surfaces only when no ASN arrives — currently 3–5 days later.

---

## 6. Interaction

```mermaid
sequenceDiagram
    autonumber
    participant M as Meridian Dispatch
    participant G as Vendor Gateway
    participant V as Vendor

    M->>M: Build file; verify CTT totals
    M->>G: SFTP/AS2 transmit (IF-042)
    G->>V: Deliver
    V-->>G: MDN / transfer complete
    G-->>M: transport_ack
    Note over V: parse
    V-->>G: 997 AK5*A (≤ 4h) (IF-043)
    G-->>M: functional_ack
    Note over V: pick, pack, ship (4-11 days)
    V-->>G: 856 ASN (IF-044)
    G-->>M: shipment_confirmed
```

**Error interactions**

```mermaid
sequenceDiagram
    autonumber
    participant M as Meridian Dispatch
    participant V as Vendor

    alt Control total mismatch at build
        M->>M: CTT verification fails
        M->>M: <b>Abort the entire file</b>; nothing transmitted
        M->>M: Page SRE; vendor receives no file
    else Transport failure
        M->>V: transmit
        Note over V: connection refused
        M->>M: Retry ×3 at 20-min intervals
        M->>M: After 3: hold DS07, page Vendor Ops
    else No 997 within 4h
        M->>V: transmit
        Note over V: silence
        M->>M: Apply hold DS07 (BR-OPS-032)
        M->>M: Retry transmission ×3 at 2h, new ISA13 each time
        M->>M: After 3: exception queue, page Vendor Ops
    else 997 rejection
        M->>V: transmit
        V-->>M: 997 AK5*R with AK3/AK4 error detail
        M->>M: Apply hold DS03 (BR-OPS-031)
        M->>M: Route to exception queue EXC-08
    end
```

---

## 7. Validation and errors

### 7.1 Validation

| Level | Check | On failure | Scope |
| --- | --- | --- | --- |
| Build | Every mandatory element populated | **Abort file** | Whole file |
| Build | `CTT-01` = count of `PO1`; `CTT-02` = sum of `PO1-02` | **Abort file** | Whole file |
| Build | File size ≤ 10 MB | Abort; split is **not** supported | Whole file |
| Build | `ISA13` not already used for this vendor | Abort | Whole file |
| Transport | Delivery confirmed | Retry | Whole file |
| Vendor — syntax | X12 004010 conformance | 997 `AK5*R` | Transaction set |
| Vendor — business | Product code known, quantity acceptable | Vendor-specific; usually a 997 rejection or a separate message | Varies |

### 7.2 Error catalog

| Code | Severity | Meaning | Cause | Our action | Retryable |
| --- | --- | --- | --- | --- | --- |
| `MER-850-01` | Abort file | Mandatory element empty | Data defect upstream | Page SRE; no transmission | After fix |
| `MER-850-02` | Abort file | `CTT` mismatch | Build defect | Page SRE | After fix |
| `MER-850-03` | Abort file | File exceeds 10 MB | Volume spike | Page SRE; **manual split by agreement only** | After resolution |
| `MER-850-04` | Retry | Transport failure | Network or vendor endpoint | Retry ×3 at 20 min | ✅ |
| `MER-850-05` | Hold `DS07` | No 997 within 4h | Vendor EDI down, or file lost | Retry ×3 at 2h with a new `ISA13` | ✅ |
| `AK5*R` + `AK3` | Hold `DS03` | Segment-level syntax error | Layout defect | Exception queue `EXC-08`; investigate | After fix |
| `AK5*R` + `AK4` | Hold `DS03` | Element-level error | Data defect | Exception queue; investigate | After fix |
| `AK9*R` | Hold `DS03` | Whole group rejected | Envelope defect | Page Vendor Ops | After fix |

### 7.3 Retry

| Aspect | Policy |
| --- | --- |
| Retryable | Transport failures; missing 997 |
| Non-retryable | Any build-time abort; 997 rejections |
| Attempts | Transport: 3 at 20 min. Missing 997: 3 at 2h |
| Total budget | 1h transport, 6h acknowledgement |
| **New control number per retry** | ✅ Each retransmission uses a fresh `ISA13`. A bare retransmission of the same control number would be rejected as a duplicate |
| Terminal action | Hold `DS07` or `DS03`; exception queue; page Vendor Ops |
| Manual resubmission | [RUN-OPS-001 §5](../05-operations/runbook-nightly-order-cycle.md) — **requires vendor contact first** |

---

## 8. Reconciliation

| | |
| --- | --- |
| Control totals in the payload | `CTT-01` count, `CTT-02` quantity hash, per transaction set |
| Independent reconciliation | `DSP_INS` row count and `NET_AMT` sum vs. the generated file, per vendor, per night |
| Frequency | Every cycle, before transmission |
| Tolerance | **Zero** |
| Break owner | SRE, escalating to Vendor Integration Lead |
| Break procedure | **Abort transmission for that vendor.** Other vendors' files still transmit |
| Evidence retained | 7 years with the archived file |

```sql
-- Control C-04/C-05: run before transmission, per vendor.
SELECT d.VND_CD,
       COUNT(*)          AS dsp_rows,
       SUM(d.NET_AMT)    AS dsp_amount,
       f.file_po1_count,
       f.file_amount
FROM   DSP_INS d
JOIN   EDI_FILE_SUMMARY f
       ON f.CYCLE_ID = d.CYCLE_ID AND f.VND_CD = d.VND_CD
WHERE  d.CYCLE_ID = :cycle_id
GROUP  BY d.VND_CD, f.file_po1_count, f.file_amount
HAVING COUNT(*)       <> f.file_po1_count
    OR SUM(d.NET_AMT) <> f.file_amount;
-- Any row returned aborts that vendor's transmission.
```

---

## 9. Service levels

| Metric | Commitment | Measured by | Measurement point | Reporting |
| --- | --- | --- | --- | --- |
| File delivered by | **03:00 UTC** | Meridian | Transport ack timestamp | Daily; monthly scorecard |
| Availability of the vendor endpoint | ≥ 99.0% monthly | Meridian probes | Connection attempt | Monthly scorecard |
| 997 returned within | 4 hours | Meridian | Receipt timestamp | Monthly scorecard |
| 997 rejection rate | ≤ 0.5% | Meridian | Rejections ÷ transactions | Monthly scorecard |
| Support response, Tier 1 vendors | 1 hour, 24×7 | Both | Ticket timestamps | Quarterly review |

**Current performance, 2026-Q2**

| Metric | Best | Median | Worst | Below commitment |
| --- | --- | --- | --- | --- |
| Delivery by 03:00 | 100% | 100% | **97.3%** | 0 vendors *(the 2.7% is our batch overrun, not theirs)* |
| 997 within 4h | 100% | 99.4% | **86.1%** (V19) | 3 vendors |
| Rejection rate | 0.0% | 0.1% | **1.8%** (V31) | 2 vendors |

**Escalation**

| Level | Trigger | Contact | Response |
| --- | --- | --- | --- |
| 1 | Transport failure after 3 retries | Vendor technical contact | 1h |
| 2 | No 997 after 3 retransmissions | Vendor account manager | 4h |
| 3 | Vendor unavailable > 12h | Head of Supply Chain Systems ↔ vendor executive | Same day |

---

## 10. Monitoring

| Signal | Threshold | Alert to | Runbook |
| --- | --- | --- | --- |
| File build failure | Any | SRE page | [RUN-OPS-001](../05-operations/runbook-nightly-order-cycle.md) §3 |
| Control total mismatch | Any | SRE page | `RUN-OPS-001` §3 |
| Transmission failure after retries | Any | Vendor Ops page | `RUN-OPS-001` §5 |
| **File not transmitted by 02:30** | Any | SRE page | `RUN-OPS-001` §2 |
| 997 overdue > 4h | Any vendor | Vendor Ops ticket | `RUN-OPS-002` |
| Volume anomaly, per vendor | ±25% vs. same weekday last week | Vendor Ops ticket | — |
| Certificate expiring | 60 and 30 days | Vendor Integration Lead | — |
| **SSH key age** | ❌ **Not monitored** | — | `TD-09` |

---

## 11. Versioning and change

| Aspect | Policy |
| --- | --- |
| Versioning scheme | `major.minor`; the version is **not** carried in the payload |
| Version communicated via | The implementation guide and a written change notice |
| Backwards compatibility | New optional elements are non-breaking; everything else is breaking |
| Parallel version support | **Not supported.** All 43 vendors move together |
| Notice — non-breaking | 30 days |
| Notice — breaking | **90 days** (contractual) |
| Deprecation period | 180 days |
| Testing required | Loopback validation for all; sandbox testing for the 4 vendors who have one |
| Approval | Vendor Integration Lead + each vendor individually |

> **No version negotiation, and no parallel version support.** Every change requires all 43
> vendors to move on the same date, which makes any change to this interface a coordination
> exercise measured in quarters. That is why the layout has not changed since 2023-11, and
> why `C-03` in `TAD-OPS-001 §3.2` treats new dispatch fields as effectively impossible. See
> ADR-OPS-0031, now under review (`Q-003`).

**Version history**

| Interface version | Effective | Change | Breaking | Notice given |
| --- | --- | --- | --- | --- |
| 3.1 | 2023-11-06 | Added `MEA` gross weight for freight cost allocation | **Yes** — new mandatory segment | 120 days |
| 3.0 | 2021-04-12 | `PO1-09` extended from 3 to 5 option codes | **Yes** — length change | 90 days |
| 2.2 | 2019-08-19 | Added `DTM` 010 requested ship date | Yes | 90 days |
| 2.0 | 2016-02-01 | Moved from one transaction set per file to one per order | Yes | 180 days |
| 1.0 | 2014-09-15 | Initial | — | — |

---

## 12. Testing and certification

| # | Scenario | Expected | Mandatory |
| --- | --- | --- | --- |
| C-01 | Connectivity and authentication both directions | Success | ✅ |
| C-02 | Single-line order, typical values | 997 `AK5*A`; correct pick | ✅ |
| C-03 | Multi-line order, 50 lines across 20 transaction sets | As above | ✅ |
| C-04 | **Empty file** (`CTT*0*0`) | 997 `AK5*A`; no pick | ✅ |
| C-05 | Maximum-size file (9,999 `PO1`) | 997 `AK5*A` within 4h | ✅ |
| C-06 | Structurally invalid (missing `SE`) | 997 `AK5*R` with `AK3` | ✅ |
| C-07 | Invalid product code | 997 rejection or a documented business rejection | ✅ |
| C-08 | **Implied-decimal price** — `PO1-04` = `125000` | Vendor records USD 1,250.00, **not** USD 125,000.00 | ✅ |
| C-09 | Maximum-length `PO1-09` with 5 option codes | All 5 recorded | ✅ |
| C-10 | Duplicate `ISA13` | Vendor rejects as a duplicate | ✅ |
| C-11 | Retransmission with a new `ISA13` | Accepted; **no duplicate pick** | ✅ |
| C-12 | 997 timeout simulation | Meridian applies `DS07` and retries | ✅ |
| C-13 | `MEA` in LB for a US vendor, KG otherwise | Correct unit recorded | ✅ |
| C-14 | End-to-end: 850 → 997 → pick → 856 | Full cycle completes and reconciles | ✅ |

**Certification record — example**

| Vendor | Environment | Date | Tests passed | Signed — us | Signed — them |
| --- | --- | --- | --- | --- | --- |
| V41 (onboarded 2026-05) | Production loopback + live pilot | 2026-05-28 | 14 of 14 | Vendor Integration Lead | Vendor integration manager |

> C-08 and C-11 catch the two defects that have most often reached production during
> onboarding: the 100× price error, and a vendor treating a legitimate retransmission as a
> new order and shipping twice.

---

## 13. Operations

| Aspect | Detail |
| --- | --- |
| Runbook | [RUN-OPS-001](../05-operations/runbook-nightly-order-cycle.md) |
| Manual resubmission | §7.3 — **contact the vendor first**; never a bare retransmission |
| Data correction | Correct in `ORD_LIN`, re-run `ORD-DISPATCH-040` after deleting the cycle's `DSP_INS` rows, transmit with a new `ISA13` |
| Planned outage notification | 5 business days to all vendors |
| Emergency contact — us | Meridian SRE on-call; `#meridian-edi` |
| Emergency contact — vendor | Partner register; 24×7 for the 11 Tier 1 vendors |
| Support hours | Us: 24×7. Vendors: varies, 11 are 24×7 |

---

## 14. Open items

| ID | Item | Owner | Target |
| --- | --- | --- | --- |
| OI-01 | SSH key rotation has no schedule or monitoring (`TD-09`) | Vendor Integration Lead | 2026-10-31 |
| OI-02 | Only 4 of 43 vendors have a sandbox | Vendor Integration Lead | Ongoing commercial discussion |
| OI-03 | Revisit ADR-OPS-0031 — two vendors want API dispatch (`Q-003`) | Vendor Integration Lead | 2026-11-30 |
| OI-04 | File-splitting for >10 MB is by agreement only; no automated path | Integration Lead | 2027-Q1 |

---

## Change log

| Doc version | Date | Author | Change | Interface version |
| --- | --- | --- | --- | --- |
| 4.2.0 | 2026-07-30 | Vendor Integration Lead | Semi-annual review. Added §5.1 acknowledgement semantics after a dispute with V19; added C-11 retransmission certification; recorded Q2 performance | 3.1 (unchanged) |
| 4.1.0 | 2026-02-12 | Vendor Integration Lead | Added §2.1 certificate and key register after `TD-09` was raised | 3.1 (unchanged) |
| 4.0.0 | 2025-08-06 | Vendor Integration Lead | Added §3.1 empty-file semantics and C-04 after 6 vendors rejected empty files | 3.1 (unchanged) |
| 2.0.0 | 2023-11-06 | Vendor Integration Lead | Interface v3.1 — `MEA` segment added | **3.1** |
