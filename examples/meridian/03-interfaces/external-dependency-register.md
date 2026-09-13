---
doc_id: EDR-MER-001
title: Meridian — External Dependency Register
doc_type: edr
status: approved
version: 3.1.0
owner: Service Management Lead
reviewers: [Vendor Integration Lead, Head of Platform Architecture, Procurement]
approvers: [Head of Supply Chain Systems]
created: 2024-10-21
last_reviewed: 2026-08-06
next_review: 2026-11-06
review_cycle: quarterly
classification: confidential
systems: [MERIDIAN]
domains: [cross-domain]
upstream_docs: [ICAT-MER-001]
downstream_docs: []
tags: [dependencies, vendors, risk]
---

# Meridian — External Dependency Register

> Broader than the interface catalog. Some dependencies have no technical footprint at all —
> a portal someone logs into monthly, an industry code list emailed quarterly, a consultant
> who maintains one adapter. They are dependencies, and they fail.

---

## 1. Summary

| | Count |
| --- | --- |
| Total external dependencies | 51 |
| Critical (Tier 1) | 14 |
| With a contractual SLA | 47 |
| **With no alternative supplier** | **6** |
| **With no tested failover** | **11** |
| Contracts expiring within 12 months | 7 |
| Single points of failure | 4 |
| Dependencies with no technical footprint | 8 |

---

## 2. Register — Tier 1

| ID | Dependency | Type | Provides | Interfaces | Owner | Contract expiry | SLA | Alternative | Failover tested |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ED-001 | Vendor V07 (largest fulfilment vendor) | Vendor | 18% of fulfilment volume | IF-042/043/044 | Vendor Integration Lead | 2028-03 | ✅ | Partial — 3 vendors could absorb ~60% | ❌ |
| ED-002 | Vendor V12 | Vendor | 11% | IF-042/043/044 | Vendor Integration Lead | 2027-06 | ✅ | Partial | ❌ |
| ED-003 | Vendor V19 | Vendor | 9% | IF-042/043/044 | Vendor Integration Lead | **2026-12** ⚠️ | ✅ | Partial | ❌ |
| ED-044 | Compliance screening SaaS | SaaS | Trade compliance screening for every order line | IF-112 | Integration Lead | 2027-09 | ✅ | **None qualified** | ✅ 2026-04 |
| ED-045 | Settlement Bank | Bank | Incentive payment execution | IF-063 | Finance Systems Lead | 2029-01 | ✅ | Corporate banking alternative exists | ❌ |
| ED-047 | IBM — z/OS, DB2, CICS, MQ | Platform | The mainframe estate | All | Platform Engineering Lead | 2029-12 | ✅ | **None** | n/a |
| ED-048 | IBM Sterling B2B Integrator | Platform | All 43 vendor integrations | IF-042/043/044 | Vendor Integration Lead | 2027-12 **EOL** ⚠️ | ✅ | Alternatives exist; migration ~9 months | ❌ |
| ED-049 | IBM Workload Scheduler | Platform | All 210 nightly jobs | All batch | Platform Engineering Lead | **2028-06 EOL** ⚠️ | ✅ | Alternatives exist; migration ~12 months | ❌ |
| ED-050 | AS2 certificate authority | Security | Vendor AS2 certificates | IF-042/043/044 | Security Architect | 2027-03 | ✅ | Alternative CAs exist | ✅ |
| ED-051 | Corporate network provider (vendor VPNs) | Infrastructure | Connectivity to 12 SFTP vendors | IF-042 subset | Network Lead | 2027-08 | ✅ | Internet fallback exists, not configured | ❌ |
| *(4 further Tier 1)* | | | | | | | | | |

---

## 3. Dependency detail

### ED-044: Compliance screening SaaS

| | |
| --- | --- |
| Provides | Trade compliance and denied-party screening for every order line |
| Type | SaaS |
| Criticality | **Tier 1** |
| Business processes dependent | Order dispatch — a line cannot dispatch without a screening result |
| Interfaces | IF-112 |
| Relationship owner | Integration Lead |
| Technical owner | Squad 1 Tech Lead |
| Annual cost | USD 340k |
| Contract expiry | 2027-09-30 |
| Notice period | 90 days |
| Renewal owner | Procurement + Integration Lead |

**Service commitments**

| Metric | Commitment | Measured | Remedy | Actual, 12 months |
| --- | --- | --- | --- | --- |
| Availability | 99.9% | Their status page + our probes | Service credits | 99.94% |
| Response time | p99 ≤ 800ms | Our APM | None | p99 620ms |
| Support response, P1 | 1 hour | Ticket timestamps | Credits | 42 min median |
| Watch-list currency | Updated within 24h of publication | Their attestation | Contractual | ✅ Attested quarterly |
| Change notice | 60 days | — | Contractual | ✅ |

**Failure impact**

| Duration | Impact | Workaround | Capacity |
| --- | --- | --- | --- |
| 1 hour | None if outside the batch window | — | — |
| **During the batch window** | **Dispatch stops entirely** — no line can be screened, and lines fail closed | Manual screening | **~200 lines/day vs. 95,000 normal.** Not a workaround at scale |
| 1 day | A full fulfilment day lost | As above | — |
| Permanent | Cannot dispatch at all until an alternative is integrated | — | — |

**Contingency**

| Aspect | Detail |
| --- | --- |
| Alternative provider | **None qualified.** Two candidates evaluated 2025; neither covers all three required jurisdictions |
| Switching time | Estimated 6–9 months including re-certification |
| Switching cost | Estimated USD 400k |
| Manual fallback | Compliance team screens manually against published lists |
| **Manual fallback capacity** | **~200 lines/day.** Normal volume is 95,000. The fallback covers 0.2% |
| Data held by them | Dealer name, address, option codes. 90-day retention |
| Data retrievable on exit | ✅ Contractual; format agreed |
| Exit plan | Documented, not rehearsed |
| Last tested | 2026-04 — a simulated outage confirmed fail-closed behaviour |

> The manual fallback number is the honest one. "We have a manual process" implies continuity;
> "the manual process handles 0.2% of volume" is the fact a continuity plan needs. Stating it
> is what turned this from a green row into a funded risk item.

**Contacts**

| Purpose | Contact | Hours | Escalation |
| --- | --- | --- | --- |
| Operational | Their support portal | 24×7 | P1 phone line |
| Incident | Named CSM | Business hours | VP Customer Success |
| Commercial | Account executive | Business hours | Procurement |
| Technical change | Integration team alias | Business hours | CSM |

---

### ED-048: IBM Sterling B2B Integrator

| | |
| --- | --- |
| Provides | EDI translation and transport for all 43 vendors |
| Criticality | **Tier 1** |
| Version | 6.1 |
| **End of support** | **2027-12** |
| Interfaces | IF-042, IF-043, IF-044 — 129 of 187 interfaces |
| Annual cost | USD 210k licence + support |

**Failure impact**

| Duration | Impact | Workaround |
| --- | --- | --- |
| 1 hour, outside the window | None | — |
| During transmission | Dispatch files cannot be sent; 03:00 cutoff missed | **None.** Manual SFTP for 12 vendors is theoretically possible but untested and would not cover the 31 AS2 vendors |
| 1 day | Full fulfilment day lost for all 43 vendors | — |

**Contingency**

| Aspect | Detail |
| --- | --- |
| Alternative provider | Alternatives exist (several commercial and open-source EDI platforms) |
| Switching time | ~9 months including re-certification with all 43 vendors |
| Manual fallback | Untested; would cover at most the 12 SFTP vendors |
| **Failover tested** | ❌ **Two nodes, one site.** Site failover for Sterling has never been tested |
| Exit plan | Not documented |

**Status:** upgrade to 7.x in flight, target 2027-06, ahead of the 2027-12 EOL. The
re-certification of 43 vendors is the long pole and is the reason the programme started 18
months ahead.

---

## 4. Concentration risk

| Provider | Dependencies | Combined criticality | Combined annual spend | Concentration risk |
| --- | --- | --- | --- | --- |
| **IBM** | ED-047 (z/OS, DB2, CICS, MQ), ED-048 (Sterling), ED-049 (Workload Scheduler) | **Tier 1 × 3** | ~USD 4.1M | **High.** The platform, the integration layer, and the scheduler all come from one vendor. A commercial dispute or a strategic product retirement affects all three simultaneously |
| Fulfilment vendors | 43 dependencies | Tier 1 | ~USD 180M | Low — no single vendor exceeds 18% |
| Corporate network provider | ED-051 + corporate WAN | Tier 1 | Shared corporate cost | Medium |

**Shared underlying dependencies (fourth-party)**

| Underlying provider | Our dependencies relying on it | Visible to us? | Risk |
| --- | --- | --- | --- |
| A single public cloud region | ED-044 compliance SaaS; **and, per their disclosure, 3 of our fulfilment vendors' WMS platforms** | ⚠️ Partially — disclosed for 4 of 51 | **Medium.** A regional outage could simultaneously stop screening and three vendors' ability to receive dispatch |
| One AS2 certificate authority | 31 vendor AS2 relationships | ✅ | Medium — a CA compromise would require re-issuing 31 certificates |
| One carrier data provider | Carrier code mapping for all vendors | ✅ | Low |

> Fourth-party risk is the part that surprises people during an outage. We asked all 14 Tier
> 1 dependencies who *they* depend on; 4 answered substantively, 6 gave partial answers, and
> 4 declined. The answer for 10 of 14 is therefore incomplete, and that incompleteness is
> itself the finding.

---

## 5. Contract and commercial

| ID | Provider | Expiry | Notice deadline | Auto-renew | Annual value | Decision owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ED-003 | Vendor V19 | **2026-12-31** | **2026-10-02** | No | USD 16.2M | Head of Supply Chain Systems | ⚠️ **Renewal decision overdue** |
| ED-048 | IBM Sterling | 2027-12 (EOL) | n/a | — | USD 210k | Platform Engineering Lead | Upgrade in flight |
| ED-002 | Vendor V12 | 2027-06-30 | 2027-03-31 | Yes, 12 months | USD 19.8M | Head of Supply Chain Systems | Review scheduled |
| ED-044 | Compliance SaaS | 2027-09-30 | 2027-07-02 | Yes, 12 months | USD 340k | Integration Lead | Review scheduled |
| ED-051 | Network provider | 2027-08-31 | 2027-05-31 | No | Shared | Network Lead | — |
| *(2 further within 12 months)* | | | | | | | |

> **ED-003's notice deadline is 2026-10-02 and today is 2026-08-06.** V19 is 9% of volume,
> has the worst 997 timeliness in the estate (86.1%), and has not signed the ASN data
> contract. The renewal decision needs to be made in the next eight weeks and is flagged at
> every quarterly review until it is.

---

## 6. Compliance

| ID | Provider | Data shared | Classification | Personal data | DPA | Location | Certifications | Last assessment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ED-044 | Compliance SaaS | Dealer name, address, option codes | **Restricted** | ✅ | ✅ | EU + US | ISO 27001, SOC 2 Type II | 2026-04 |
| ED-045 | Settlement Bank | Dealer bank details, payment amounts | **Restricted** | ✅ | ✅ | Domestic | Regulated entity | 2026-01 |
| ED-001–043 | Fulfilment vendors | Order lines, dealer codes, **net pricing** | Confidential | ❌ | n/a | Various | Varies — 31 of 43 hold ISO 27001 | Annual attestation |
| ED-046 | Carrier data provider | None outbound | Public | ❌ | n/a | US | — | 2025-11 |

---

## 7. Performance

| ID | Provider | SLA | Actual (12m) | Breaches | Credits claimed | Trend | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ED-001 | V07 | 99.0% endpoint availability | 99.7% | 0 | — | ▲ | — |
| ED-003 | **V19** | 99.0%; 997 within 4h | 98.2%; **86.1%** | **7** | USD 41k | ▼ | **Renewal review** |
| ED-044 | Compliance SaaS | 99.9% | 99.94% | 0 | — | — | — |
| ED-048 | Sterling | 99.5% | 99.81% | 1 | — | — | Upgrade in flight |
| ED-049 | Workload Scheduler | 99.5% | 99.6% | 1 | — | — | Replacement assessment |

**Incident history — Tier 1, last 24 months**

| Date | Provider | Duration | Our impact | Their root cause | Remedy | Action taken |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-03-14 | V19 | 11h | 1,640 orders' dispatch delayed a day | WMS upgrade overran | Credits USD 18k | Added to the renewal review |
| 2025-11-02 | ED-049 Scheduler | 4h | **Whole nightly chain missed**; INC-2025-0733 | Corrupted job database | None | Standby requirement raised (`TD-01`) |
| 2025-08-19 | ED-044 Compliance | 2h | Dispatch stopped; 4,100 lines failed closed | Their regional outage | Credits USD 8k | Fail-closed behaviour validated; manual fallback capacity measured |
| 2025-04-07 | ED-051 Network | 6h | 12 SFTP vendors unreachable | Provider routing change | Credits | Internet fallback designed, **not implemented** |

---

## 8. Risks

| ID | Risk | Dependency | Likelihood | Impact | Mitigation | Owner | Review |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DR-01 | Scheduler fails before the 2028 EOL migration, with no standby and no manual run procedure | ED-049 | Medium | **Critical** | Replacement assessment funded Q1 2027; no interim mitigation | Platform Engineering Lead | Monthly |
| DR-02 | Compliance SaaS unavailable during the batch window; no qualified alternative and 0.2% fallback capacity | ED-044 | Low | **Critical** | Fail-closed validated; alternative provider search restarted | Integration Lead | Quarterly |
| DR-03 | IBM concentration — platform, integration, and scheduling from one vendor | ED-047/048/049 | Low | **Critical** | Monitored; no active mitigation | Head of Platform Architecture | Annual |
| DR-04 | V19 renewal decision missed; contract auto-lapses | ED-003 | **Medium** | High | **Decision required by 2026-10-02** | Head of Supply Chain Systems | **Immediate** |
| DR-05 | Sterling site failover untested | ED-048 | Medium | High | Include in the 7.x upgrade programme | Vendor Integration Lead | Quarterly |
| DR-06 | Fourth-party cloud concentration between compliance SaaS and 3 vendors | ED-044 + 3 vendors | Low | High | Disclosure requested from all Tier 1 dependencies | Service Management Lead | Quarterly |
| DR-07 | 3 vendor SSH keys over 4 years old | ED-001–043 subset | Low | Medium | Rotation scheduled (`TD-09`) | Vendor Integration Lead | Quarterly |

**Risk categories assessed**

| Category | Assessment |
| --- | --- |
| Availability | Assessed for all 14 Tier 1 |
| Viability | Assessed annually; no Tier 1 dependency is financially distressed |
| Lock-in | **High for ED-047.** 30 years of COBOL on z/OS is not portable in any practical sense |
| Data | Exit data retrieval contractual for 12 of 14 Tier 1; 2 vendor contracts are silent |
| Change | 60–90 day notice contractual for 13 of 14 |
| Concentration | **IBM** — see §4 |
| **Fourth party** | **Incomplete** — 10 of 14 Tier 1 gave partial or no disclosure |
| Contract | 7 expiring within 12 months; 1 decision overdue |
| Knowledge | Sterling configuration has a bus factor of 2; compliance SaaS integration, 1 |

---

## 9. Dependencies with no technical footprint

> Found by asking, not by scanning. None of these appear in a firewall rule, a scheduler job,
> or an interface catalog, and all of them stop something if they fail.

| Dependency | What it provides | Frequency | Who performs | Failure impact | Contingency |
| --- | --- | --- | --- | --- | --- |
| NMFTA carrier code list | SCAC codes for carrier mapping | Annual download | Vendor Integration analyst | Stale codes map to `'UNK'`; degraded vendor reporting | Low impact; can lapse a year |
| Industry option-code standards body | Advance notice of option classification changes | Quarterly newsletter | Portfolio analyst | Portfolio changes made without upstream context | Low |
| **Tax advisory firm** | Tax category rules that drive `REF.TAXCAT` | ~4 times a year, by email | Tax team → 2 named individuals | **Tax categories become stale; regulatory exposure** | **None. No contract, no SLA, no backup contact** |
| Compliance watch-list publisher | Denied-party list updates, uploaded manually | Weekly | Compliance analyst | Stale screening; compliance exposure | Their portal has a backup contact |
| External COBOL contractor | `ORDTAX05` maintenance | On call, ~3 times a year | Individual contractor | **Bus factor 1** on a component nobody else understands | **None** |
| Vendor capacity spreadsheets | Monthly capacity commitments, emailed | Monthly | 43 vendors → 1 analyst | Routing uses stale capacity; mis-routing | Manual |
| Dealer franchise regulator guidance | Changes to incentive calculation requirements | Ad hoc | Legal → Sales Ops | Non-compliant calculation | Legal monitors |
| Carrier tracking services | Tracking reference resolution | Continuous | — | ~2% of references unresolvable | Accepted |

> **The tax advisory firm and the COBOL contractor are the two that matter.** Both feed
> components with regulatory or financial consequence, both have a bus factor of 1, and
> neither is under contract or covered by any continuity plan. Both were invisible until
> someone asked "who else do you rely on to do your job?". Raised 2026-08; owner assigned to
> the Service Management Lead.

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 3.1.0 | 2026-08-06 | Service Management Lead | Quarterly review. Added §9 tax advisory firm and COBOL contractor after the continuity interviews; escalated DR-04 (V19 renewal deadline); recorded Q2 performance |
| 3.0.0 | 2026-02-19 | Service Management Lead | Added §4 fourth-party disclosure results; added the compliance SaaS manual fallback capacity measurement |
| 2.0.0 | 2025-09-24 | Service Management Lead | Added §9 non-technical dependencies — 6 found through interviews |
| 1.0.0 | 2024-10-21 | Service Management Lead | Initial register |
