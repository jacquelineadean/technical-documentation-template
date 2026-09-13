---
doc_id: FIS-<SCOPE>-001
title: <Interface Name> — File and Batch Interface Specification
doc_type: fis
status: draft
version: 0.1.0
owner: <Integration Lead role>
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: semi-annual
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [ICAT-<SCOPE>-001]
downstream_docs: []
related_interfaces: []
tags: [file, batch, edi, interface]
---

# \<Interface Name\> — File and Batch Interface Specification

> **Purpose.** File-based interfaces — fixed-width, delimited, XML, or EDI — which remain
> the backbone of partner integration in most established platforms. The details that matter
> here are unglamorous and unforgiving: encoding, padding, control totals, and what happens
> when a file arrives twice.

---

## Contents

| Section | Summary |
| --- | --- |
| [1. Overview](#1-overview) | Interface ID, direction, counterparty, business purpose |
| [2. File identification](#2-file-identification) | Filename pattern with every variable part defined; sequence and gap semantics |
| [3. Transport](#3-transport) | Protocol, hosts, directories, credentials, archival |
| [4. File structure](#4-file-structure) | Format, encoding, line terminators, record types, ordering |
| [5. Record layouts](#5-record-layouts) | Field-level header, detail, and trailer layouts with positions and types |
| [6. Control totals and reconciliation](#6-control-totals-and-reconciliation) | Record counts, amount totals, tolerances, and mismatch actions |
| [7. Processing](#7-processing) | Processing model, transaction boundary, duplicate and resend handling |
| [8. Validation](#8-validation) | Validation levels from file to field, with failure action and scope |
| [9. Error codes](#9-error-codes) | Error codes, level, cause, and required action |
| [10. EDI specifics](#10-edi-specifics) | X12/EDIFACT standard, transaction set, envelopes, acknowledgements |
| [11. Volumes](#11-volumes) | Typical and peak record counts, file sizes, processing durations |
| [12. Monitoring](#12-monitoring) | Non-arrival, rejection, and volume-anomaly signals with runbooks |
| [13. Example](#13-example) | Worked example file, including edge cases such as an empty file |
| [14. Operations](#14-operations) | Manual resend, reprocessing an archived file, sequence resets |
| [Change log](#change-log) | Version, date, author, change |

---

## 1. Overview

| | |
| --- | --- |
| Interface ID | IF-… |
| Direction | Outbound / Inbound |
| Counterparty | |
| Business purpose | |
| Criticality | |
| Live since | |

---

## 2. File identification

| | |
| --- | --- |
| Filename pattern | *(with every variable part defined)* |
| Example filename | |
| Sequence number | *(range, reset policy, gap meaning)* |
| Duplicate filename handling | |
| Case sensitivity | |

| Pattern element | Format | Example | Notes |
| --- | --- | --- | --- |
| Prefix | | | |
| Date | | | *(business date or transmission date? state which)* |
| Sequence | | | |
| Extension | | | |

> Whether the date in a filename is the business date or the transmission date matters at
> every period boundary, and the two diverge whenever a file is late or re-sent. State it.

---

## 3. Transport

| | |
| --- | --- |
| Protocol | |
| Host (logical) | |
| Directory — inbound | |
| Directory — outbound | |
| Directory — archive | |
| Authentication | |
| Encryption in transit | |
| File encryption | |
| Signing | |

**Completeness signalling**

| Aspect | Approach |
| --- | --- |
| Method | Trigger file / Temporary name then rename / Size stability / Checksum file |
| Detail | |

> A reader that picks up a file mid-write will process a truncated file. Renaming after a
> complete write is the standard defence; a `.done` trigger file is the alternative. One of
> them must be specified — "we wait a few seconds" is not a mechanism.

**Timing**

| | |
| --- | --- |
| Schedule | *(with timezone and DST behaviour)* |
| Expected arrival window | |
| Late threshold | |
| Cutoff | |
| Missing-file alert | *(at what time, to whom)* |

---

## 4. File structure

| | |
| --- | --- |
| Format | Fixed-width / Delimited / XML / JSON / X12 / EDIFACT |
| Character encoding | |
| Line terminator | |
| Record length | |
| Header records | |
| Trailer records | |
| Maximum records | |
| Maximum size | |
| Compression | |
| Empty file expected? | *(and how a legitimate empty file is distinguished from a failure)* |

**Format-specific**

| Delimited | |
| --- | --- |
| Delimiter | |
| Quote character | |
| Escape character | |
| Embedded delimiter handling | |
| Embedded newline handling | |

| Fixed-width | |
| --- | --- |
| Padding — alphanumeric | |
| Padding — numeric | |
| Sign representation | *(leading, trailing, overpunch)* |
| Implied decimal | *(e.g. `0000012345` = 123.45)* |
| Truncation behaviour | |

---

## 5. Record layouts

### Header

| # | Field | From | To | Len | Type | Req | Value | Example |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Record type | 1 | 2 | 2 | A/N | M | `HD` | `HD` |

### Detail

| # | Field | From | To | Len | Type | Req | Valid values | Example | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | | | | |

### Trailer

| # | Field | From | To | Len | Type | Req | Value | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Record type | 1 | 2 | 2 | A/N | M | `TR` | |
| 2 | Record count | | | | N | M | | Detail records only — state whether header/trailer are included |
| 3 | Control total | | | | N | M | | Sum of `<field>`, absolute value, implied decimals |

**Type codes**

| Code | Meaning |
| --- | --- |
| A | Alphabetic |
| N | Numeric, unsigned |
| S | Numeric, signed |
| A/N | Alphanumeric |
| D | Date, format stated per field |

---

## 6. Control totals and reconciliation

| Control | Definition | Tolerance | On mismatch |
| --- | --- | --- | --- |
| Record count | | 0 | Reject file |
| Amount total | | | Reject file |
| Hash total | | 0 | Reject file |
| Sequence continuity | | 0 | Alert, investigate gap |

> Control totals must be computed independently on the receiving side, from the detail
> records, and compared to the trailer. A receiver that reads the trailer without
> recomputing is not controlling anything.

**Independent reconciliation**

| Aspect | Detail |
| --- | --- |
| What is compared | |
| Against what | |
| Frequency | |
| Tolerance | |
| Owner | |
| Break procedure | |

---

## 7. Processing

| Aspect | Behaviour |
| --- | --- |
| Processing model | All-or-nothing / Record-by-record with error file |
| Transaction boundary | |
| Duplicate file detection | *(by name, sequence, hash — state which)* |
| Duplicate record detection | |
| Out-of-sequence handling | |
| Late file handling | |
| Partial file handling | |
| Reprocessing procedure | |
| Archive location and retention | |

**Duplicate handling** ⚠️

| Scenario | Detection | Action |
| --- | --- | --- |
| Identical file re-sent | | |
| Same sequence, different content | | |
| Same business records in a later file | | |

> Re-sending a dispatch or invoice file that was already processed creates duplicate
> business effect — duplicate shipments, duplicate payments. Detection must be by content
> hash **and** sequence, not by filename alone, because a re-send is often renamed.

---

## 8. Validation

| Level | Check | Failure action | Scope |
| --- | --- | --- | --- |
| File | Naming, size, readability, completeness signal | Reject | File |
| Structure | Header/trailer present, record lengths, counts | Reject | File |
| Control | Totals match | Reject | File |
| Field | Type, length, format, valid values | Reject record | Record |
| Referential | Keys resolve | Reject record | Record |
| Business | Rules | Reject record | Record |

**Error file**

| | |
| --- | --- |
| Produced | |
| Naming | |
| Location | |
| Format | *(original record + error code + description)* |
| Notification | |
| Correction and resubmission | |

---

## 9. Error codes

| Code | Level | Meaning | Cause | Action |
| --- | --- | --- | --- | --- |
| | File / Record / Field | | | |

---

## 10. EDI specifics

> Complete only for X12/EDIFACT interfaces.

| | |
| --- | --- |
| Standard and version | |
| Transaction set | *(850 PO, 855 ack, 856 ASN, 810 invoice, 997 functional ack)* |
| Implementation guide | |
| Interchange sender/receiver IDs | |
| Test/production indicator | |
| Envelope structure | |
| Segment terminator | |
| Element separator | |
| Sub-element separator | |
| Functional acknowledgement (997) required | |
| 997 timeframe | |
| 997 rejection handling | |

**Segment usage**

| Segment | Loop | Req | Max | Purpose | Elements used |
| --- | --- | --- | --- | --- | --- |
| | | M/O/C | | | |

**Code mappings**

| EDI qualifier/code | Our value | Notes |
| --- | --- | --- |
| | | |

---

## 11. Volumes

| | Records | Size | Duration |
| --- | --- | --- | --- |
| Typical | | | |
| Peak | | | |
| Peak driver | | | |
| Maximum supported | | | |

---

## 12. Monitoring

| Signal | Threshold | Alert to | Runbook |
| --- | --- | --- | --- |
| File not received by deadline | | | |
| File rejected | | | |
| Record error rate | | | |
| Volume anomaly | | | |
| Sequence gap | | | |
| Processing overrun | | | |
| Transfer failure | | | |

---

## 13. Example

```
<Complete valid file: header, several detail records, trailer with correct totals.>
```

**Edge cases**

| Case | Example |
| --- | --- |
| Empty file (header + trailer only) | |
| Maximum-length values | |
| Negative amounts | |
| Special characters | |

---

## 14. Operations

| Procedure | Detail |
| --- | --- |
| Manual resend | |
| Reprocess an archived file | |
| Skip a file | *(and the approval needed)* |
| Correct and resubmit records | |
| Sequence number reset | |
| Contact — us | |
| Contact — counterparty | |

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
