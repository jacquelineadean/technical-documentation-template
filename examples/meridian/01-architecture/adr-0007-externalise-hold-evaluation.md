---
doc_id: ADR-OPS-0007
title: Externalise hold evaluation from the decoder
doc_type: adr
status: approved
version: 1.2.0
owner: Order Management Architecture Lead
authors: [Meridian Squad 1]
approvers: [Head of Platform Architecture, VP Order Operations]
created: 2021-11-08
review_cycle: on-change
classification: internal
systems: [MERIDIAN]
domains: [order-processing]
upstream_docs: [TAD-OPS-001]
downstream_docs: []
related_rules: []
tags: [decision, decomposition, strangler]
---

# ADR-OPS-0007: Externalise hold evaluation from the decoder

| | |
| --- | --- |
| **Status** | Accepted |
| **Date decided** | 2021-11-08 |
| **Implemented** | 2022-03-14 (shadow run) → 2022-06-20 (cutover) |
| **Deciders** | Head of Platform Architecture, Order Management Architecture Lead, VP Order Operations |
| **Consulted** | Credit Operations Lead, Sales Operations Lead, SRE Lead, Squad 1 Tech Lead |
| **Informed** | Vendor Integration Lead, Data Governance Lead |
| **Reversal cost** | **High** (months) — reverting requires re-embedding the rules into `ORDDEC01` and re-testing all 14 hold classes |

---

## Context

Hold evaluation lived inside `ORDDEC01`, the COBOL decoding engine, interleaved with package
expansion and compatibility validation. Fourteen hold classes were evaluated across roughly
2,400 lines spread over four paragraphs of a 41,000-line program, with no clear boundary
between hold logic and decode logic.

This was causing three distinct problems, each with evidence:

**Hold rules change frequently; decode rules do not.** Over the preceding 36 months there
were 31 changes to hold behaviour — new credit conditions, a trade-compliance hold added in
2020, two changes to inventory-shortfall thresholds — against 4 changes to decode logic.
Every hold change required regression-testing the entire decoder, at a median lead time of
34 days for what were often one-line policy changes.

**The decoder is the system's highest-risk component.** It sits on the critical path to the
03:00 vendor cutoff, two engineers can safely modify it, and a defect in it stops all
dispatch. Concentrating the most frequently-changing logic in the least changeable component
is the wrong way round.

**Holds could not be evaluated outside a decode run.** Order Operations needed to re-evaluate
holds after a credit status change without re-decoding the line — re-decoding is expensive
and can produce a different result if reference data has moved. The workaround was a
separate, partially-duplicated COBOL routine, `ORDHLD09`, whose logic had drifted from the
decoder's. Two incidents (INC-2020-0644, INC-2021-0288) were traced to that divergence.

The immediate prompt was a regulatory change requiring trade-compliance screening to be
re-run on any order amendment. Implementing it inside the decoder would have meant a full
decode on every amendment — roughly a 4× increase in decode volume, which the batch window
could not absorb.

### Forces

| Force | Pushes toward | Weight |
| --- | --- | --- |
| Hold rules change ~8× more often than decode rules | Separation | High |
| The decoder is the batch critical path; changes there are expensive to validate | Separation | High |
| Holds must be evaluable outside a decode run (regulatory) | Separation | High |
| Two implementations of hold logic already exist and have diverged | Consolidation, either way | High |
| Adding a synchronous call inside a batch loop risks throughput | Keep in-process | High |
| No prior successful extraction from the COBOL core; the team has not done this before | Keep in-process | Medium |
| A network dependency inside the critical path introduces a new failure mode | Keep in-process | Medium |
| Mainframe MIPS budget is constrained; distributed compute is cheaper | Separation | Medium |

### Constraints in force at decision time

| Constraint | Type | Still expected to hold? |
| --- | --- | --- |
| Decode must sustain ≥ 1,100 lines/min to meet the 03:00 cutoff | Hard | ✅ Yes |
| No increase in the mainframe MIPS budget | Soft | ✅ Yes (reaffirmed 2025) |
| Trade-compliance re-screening on amendment is mandatory from 2022-07 | Hard | ✅ Yes |
| Team has no production experience extracting from COBOL | Soft | ❌ No longer — this decision created that experience |

---

## Decision

**We will extract hold evaluation from `ORDDEC01` into a separate Hold Service, called
synchronously over REST from a thin COBOL client, and retire the duplicate `ORDHLD09`
routine.**

### What this means concretely

| Aspect | Decision |
| --- | --- |
| Scope | All 14 hold classes; both the decode-time and the on-demand evaluation paths |
| New component | Hold Service — Java 17, Spring Boot, deployed in the application zone |
| Call boundary | `ORDHLC11`, a new ~900-line COBOL client program calling `POST /holds/evaluate` per line |
| Data ownership | `ORD_HLD` remains OPS-owned; the Hold Service becomes its only writer |
| Retired | `ORDHLD09`, and the ~2,400 lines of hold logic in `ORDDEC01` |
| Failure behaviour | **Fail closed** — if the service is unavailable, the line is marked `HoldEvalFailed` and excluded from dispatch. Formalised separately as ADR-OPS-0019. |
| Performance budget | p99 ≤ 400ms per line; the decoder issues calls in a 16-way parallel window to stay within the throughput requirement |
| Migration | Shadow run for 14 weeks: both implementations evaluate every line, outputs compared, divergence investigated to zero before cutover |
| Existing holds | Untouched. `ORD_HLD` rows written before cutover remain valid; the new service reads and releases them normally |

---

## Options considered

### Option 1 — Extract to a synchronous service ⭐ *(chosen)*

A separate service called per line during decode, and callable independently by Order
Operations and by the amendment path.

| Pros | Cons |
| --- | --- |
| Hold rules change independently of the decoder; lead time drops from 34 days to a normal release cycle | Introduces a network dependency inside the batch critical path |
| One implementation, eliminating the `ORDHLD09` divergence | Per-line synchronous calls add latency; needs parallelism to stay within budget |
| Evaluable outside a decode run, satisfying the regulatory requirement | New failure mode: service unavailability during the batch window |
| Runs on distributed compute, off the MIPS budget | Two runtimes to operate and monitor |
| Creates a reusable extraction pattern for later slices | Team has no prior experience; execution risk |

**Why chosen:** it was the only option that satisfied the regulatory requirement without
increasing decode volume, and it addressed all three stated problems rather than one. The
throughput risk was the principal objection and it was answerable with a measurement: a
spike in February 2021 showed 16-way parallel calls sustaining 1,340 lines/min against the
1,100 requirement, with p99 at 310ms.

### Option 2 — Extract to an asynchronous service with a queue

Decode publishes hold-evaluation requests; the service consumes and writes results
independently.

| Pros | Cons |
| --- | --- |
| No latency inside the decode loop | Dispatch cannot proceed until evaluation completes, so the asynchrony buys nothing on the critical path |
| Natural backpressure handling | Introduces a second synchronisation point before `ORD-DISPATCH-040`, and a new class of "evaluation not yet complete" state |
| Service outage does not stall decode | Adds an eventual-consistency window to a decision that must be made before dispatch, with no business tolerance for getting it wrong |

**Why rejected:** the asynchrony is illusory. Dispatch is gated on hold evaluation, so the
work has to complete inside the same window regardless; all the queue adds is a state to
manage and a way for the two halves to disagree about whether evaluation finished. A
proponent's fair case — that it isolates decode from service outages — is real, but the
fail-closed behaviour in Option 1 achieves the same protection for dispatch integrity
without the extra state.

### Option 3 — Refactor in place: isolate hold logic into COBOL subprograms

Keep everything in COBOL, but move the 2,400 lines into dedicated subprograms with a clean
call interface.

| Pros | Cons |
| --- | --- |
| No new runtime, no network dependency, no new failure mode | Hold changes still require a decoder release and full regression |
| Lowest execution risk; the team does this routinely | Still on the MIPS budget |
| Solves the `ORDHLD09` divergence | Does not satisfy the regulatory requirement without a 4× decode increase |
| Delivers in ~6 weeks rather than ~9 months | Leaves the highest-churn logic in the least changeable component |

**Why rejected:** it solves the divergence problem and nothing else. Specifically, it does
not make holds evaluable outside a decode run, which was the regulatory driver. It was the
right answer to a narrower question, and a genuinely attractive option on risk and cost — if
the compliance deadline had not existed, this is what we would have done.

### Option evaluation

| Criterion | Weight | Opt 1 | Opt 2 | Opt 3 |
| --- | --- | --- | --- | --- |
| Satisfies the regulatory requirement | Must | ✅ | ✅ | ❌ |
| Reduces hold-change lead time | High | ✅ | ✅ | ❌ |
| Eliminates duplicate implementations | High | ✅ | ✅ | ✅ |
| Protects decode throughput | High | ✅ (measured) | ✅ | ✅ |
| Execution risk | Medium | Medium | High | Low |
| Operational complexity added | Medium | Medium | High | None |
| Establishes a reusable pattern | Medium | ✅ | Partly | ❌ |

---

## Consequences

### Positive

- Hold-change lead time fell from a 34-day median to 9 days (measured over the 24 months
  after cutover, 22 changes).
- `ORDHLD09` retired; one implementation, no divergence. No hold-logic divergence incident
  since cutover.
- Trade-compliance re-screening on amendment delivered on time, without a decode volume
  increase.
- `ORDDEC01` reduced from 43,400 to 41,000 lines, and the hold paragraphs — previously the
  most-modified part of the program — stopped changing entirely.
- **The extraction pattern is now reusable.** Shadow-run-then-cutover became the standard
  approach, and `MOD-MER-001` is built on it. This turned out to be the most valuable
  consequence, and it was not the reason for the decision.

### Negative

- **A network dependency now sits inside the batch critical path.** `FM-09` in `TAD-OPS-001
  §13` exists because of this decision. It has fired twice (2023-02, 2024-09), each time
  handled correctly by failing closed, but each time costing a re-decode.
- **Two runtimes to operate.** SRE now needs mainframe and container skills for one
  functional area. Onboarding for the on-call rota lengthened by roughly a week.
- **Debugging spans a boundary.** Tracing why a line was held requires correlating COBOL job
  output with Hold Service logs, and there is no shared correlation ID (`TD-12`). This is a
  direct consequence and remains unfixed.
- **The 14-week shadow run cost roughly 40 engineer-days** of comparison and investigation
  effort beyond the build. It found 7 genuine divergences, all in the `ORDHLD09` path, so it
  was worth it — but it is a real cost that later slices must budget for.

### What becomes harder

| Now harder | Why | Mitigation |
| --- | --- | --- |
| Reasoning about decode performance | Throughput now depends on a remote service's latency distribution, not just mainframe capacity | Hold Service p99 is an explicit NFR with its own alert |
| Disaster recovery | The decoder and the Hold Service must be recovered together and in a compatible version | Joint DR runbook; version compatibility asserted at startup |
| Changing the hold data model | `ORD_HLD` is now written by a distributed service and read by COBOL; schema changes need both sides | Expand/contract migrations, documented in the deployment guide |

### Risks accepted

| Risk | Likelihood | Impact | Accepted by | Re-evaluation trigger |
| --- | --- | --- | --- | --- |
| Hold Service unavailability stalls dispatch for affected lines | Medium | Medium | VP Order Operations | If it occurs more than twice per year |
| Per-line call latency becomes the throughput constraint as volume grows | Low | High | Head of Platform Architecture | If p99 exceeds 350ms or decode throughput falls below 1,200 lines/min |
| Distributed/mainframe skills split raises operational cost | Medium | Low | SRE Lead | Annual on-call review |

---

## Implementation notes

| Item | Detail |
| --- | --- |
| Work required | ~9 months elapsed, ~320 engineer-days |
| Sequencing | Build service → shadow run 14 weeks → compare and converge → cut over per hold class, credit holds last |
| Backwards compatibility | `ORD_HLD` schema unchanged; pre-cutover rows remain valid and are released by the new service |
| Rollback plan | `ORDDEC01` retained the original hold paragraphs behind a feature switch for 6 months post-cutover; removed 2022-12 |
| Documents updated | `TAD-OPS-001` §5, §6.2, §13; `DOM-OPS-001` §8; `RUN-OPS-001`; new `CMP-OPS-005` |
| Success criteria | Zero output divergence for 4 consecutive weeks; decode throughput ≥ 1,100 lines/min at p95 volume; hold-change lead time ≤ 15 days measured over 12 months |

**Outcome against success criteria** *(assessed 2023-06)*

| Criterion | Result |
| --- | --- |
| Zero divergence for 4 weeks | ✅ Achieved 2022-05-30 |
| Throughput ≥ 1,100 lines/min | ✅ 1,150 typical, 1,480 peak |
| Hold-change lead time ≤ 15 days | ✅ 9-day median over 22 changes |

---

## Compliance and verification

| Aspect | Verification | Frequency | Owner |
| --- | --- | --- | --- |
| No hold logic reintroduced into `ORDDEC01` | Static check in CI: the decoder source must contain no reference to `ORD_HLD` | Per build | Squad 1 Tech Lead |
| Hold Service remains the only writer of `ORD_HLD` | DB2 authorisation: no other ID holds INSERT/UPDATE on the table | Quarterly access review | Order Data Steward |
| Fail-closed behaviour intact | Chaos test: Hold Service made unavailable in pre-prod during a decode run; assert zero lines dispatched without evaluation | Per release | SRE Lead |
| Throughput budget maintained | Decode rate tracked against the 1,100 lines/min floor | Nightly | SRE Lead |

---

## Re-evaluation triggers

| Trigger | Action |
| --- | --- |
| Decode throughput falls below 1,200 lines/min | Re-assess the per-line call pattern; consider batching evaluation requests |
| Hold Service unavailability affects dispatch more than twice in a year | Re-assess fail-closed vs. a cached last-known-good evaluation |
| The decoder itself is replaced | This ADR's boundary becomes an internal one; supersede |
| Nightly volume exceeds 400,000 lines | Re-run the throughput spike; the 2021 measurement no longer bounds the problem |

---

## References

| Reference | Location |
| --- | --- |
| `TAD-OPS-001` §5, §6.2, §13 | [tad-order-processing.md](tad-order-processing.md) |
| ADR-OPS-0019 — fail closed on hold evaluation unavailability | *(not instantiated in this example)* |
| Throughput spike results, 2021-02 | `spikes/hold-service-throughput-2021-02.md` |
| INC-2020-0644, INC-2021-0288 — `ORDHLD09` divergence | Incident system |
| Shadow-run divergence log | `migration/hold-service-shadow-run.xlsx` |

---

## Change log

| Version | Date | Change |
| --- | --- | --- |
| 1.2.0 | 2023-06-30 | Added the outcome-against-success-criteria table after the 12-month assessment. Decision text unchanged. |
| 1.1.0 | 2022-12-15 | Recorded removal of the `ORDDEC01` feature-switch fallback. Decision text unchanged. |
| 1.0.0 | 2021-11-08 | Accepted |

> An accepted ADR's decision text is never edited. Both changes above add outcome records
> alongside the original decision; the reasoning as it stood in 2021 remains readable.
