---
doc_id: EDR-<SCOPE>-001
title: <System Name> — External Dependency Register
doc_type: edr
status: draft
version: 0.1.0
owner: <Service Management Lead role>
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: quarterly
classification: internal
systems: [<SYSTEM_CODE>]
domains: [cross-domain]
upstream_docs: [ICAT-<SCOPE>-001]
downstream_docs: []
tags: [dependencies, vendors, risk]
---

# \<System Name\> — External Dependency Register

> **Purpose.** Every third party this system relies on, with criticality, contractual
> position, failure posture, and concentration risk.
>
> **Broader than the interface catalog.** Some dependencies have no technical footprint at
> all — a portal someone logs into monthly, a reference data file emailed by an industry
> body, a consultant who maintains one component. They are dependencies, and they fail.

---

## Contents

| Section | Summary |
| --- | --- |
| [1. Summary](#1-summary) | Counts by tier, contract status, and failover test coverage |
| [2. Register](#2-register) | One row per dependency: type, criticality, interfaces, contract, SLA, alternative |
| [3. Dependency detail](#3-dependency-detail) | Per-dependency detail: what it provides, failure behaviour, contingency |
| [4. Concentration risk](#4-concentration-risk) | Providers carrying several dependencies, where failure is correlated |
| [5. Contract and commercial](#5-contract-and-commercial) | Contract terms, expiry, notice deadlines, and renewals due within 12 months |
| [6. Compliance](#6-compliance) | Data shared, classification, DPAs, processing location, certifications |
| [7. Performance](#7-performance) | SLA attainment over 12 months, breaches, credits, incident history |
| [8. Risks](#8-risks) | Risks by category, with mitigation and owner |
| [9. Manual and non-technical dependencies](#9-manual-and-non-technical-dependencies) | Dependencies with no system integration — found by asking, not scanning |
| [Change log](#change-log) | Version, date, author, change |

---

## 1. Summary

| | Count |
| --- | --- |
| Total external dependencies | |
| Critical (tier 1) | |
| With a contractual SLA | |
| With no alternative supplier | |
| With no tested failover | |
| Contracts expiring within 12 months | |
| Single points of failure | |

---

## 2. Register

| ID | Dependency | Type | Provides | Criticality | Interfaces | Owner | Contract | Expiry | SLA | Alternative | Failover tested |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ED-001 | | Vendor / Partner / SaaS / Data provider / Infrastructure / Regulator / Consultancy | | 1/2/3 | IF-… | | | | | | |

**Criticality**

| Tier | Definition | Requirement |
| --- | --- | --- |
| 1 | Business process stops within hours | Contracted SLA, tested contingency, named relationship owner |
| 2 | Degraded operation; workaround for up to a day | Documented contingency |
| 3 | Tolerable for days | Monitored |

---

## 3. Dependency detail

### ED-\<NNN\>: \<name\>

| | |
| --- | --- |
| Provides | |
| Type | |
| Criticality | |
| Business processes dependent | |
| Interfaces | |
| Relationship owner | |
| Technical owner | |
| Annual cost | |
| Contract reference | |
| Contract expiry / notice | |
| Renewal owner | |

**Service commitments**

| Metric | Commitment | Measured | Remedy for breach | Actual performance |
| --- | --- | --- | --- | --- |
| Availability | | | | |
| Response time | | | | |
| Support hours | | | | |
| Incident response | | | | |
| Change notice | | | | |
| Data delivery timeliness | | | | |

**Failure impact**

| Duration | Impact | Workaround | Workaround capacity |
| --- | --- | --- | --- |
| 1 hour | | | |
| 1 day | | | |
| 1 week | | | |
| Permanent | | | |

**Contingency**

| Aspect | Detail |
| --- | --- |
| Alternative provider | |
| Switching time | |
| Switching cost | |
| Manual fallback | |
| Manual fallback capacity | *(how many transactions/day a human process can absorb — usually far below normal volume; state the number)* |
| Data held by them | |
| Data retrievable on exit | |
| Exit plan | |
| Last tested | |

**Contact**

| Purpose | Contact | Hours | Escalation |
| --- | --- | --- | --- |
| Operational | | | |
| Incident | | | |
| Commercial | | | |
| Technical change | | | |

---

## 4. Concentration risk

> Where one provider carries several dependencies, its failure is correlated rather than
> isolated. This is invisible in a per-dependency view.

| Provider | Dependencies | Combined criticality | Combined spend | Concentration risk |
| --- | --- | --- | --- | --- |
| | | | | |

**Shared underlying dependencies**

| Underlying provider | Our dependencies relying on it | Visible to us? | Risk |
| --- | --- | --- | --- |
| | *(e.g. three vendors all hosted by the same cloud region)* | | |

> Fourth-party risk — the dependencies of your dependencies — is the part that surprises
> people during an outage. Ask each tier-1 provider who *they* depend on, and record the
> answer even where it is incomplete.

---

## 5. Contract and commercial

| ID | Provider | Type | Start | Expiry | Notice | Auto-renew | Annual value | Owner | Review due |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | | |

**Expiring within 12 months**

| ID | Provider | Expiry | Notice deadline | Decision owner | Status |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

---

## 6. Compliance

| ID | Provider | Data shared | Classification | Personal data | DPA | Location | Certifications | Assessment | Next |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | ✅/❌ | ✅/❌ | | | | |

---

## 7. Performance

| ID | Provider | SLA | Actual (12m) | Breaches | Credits claimed | Trend | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

**Incident history**

| Date | Provider | Duration | Our impact | Their root cause | Remedy | Action taken |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

---

## 8. Risks

| ID | Risk | Dependency | Likelihood | Impact | Mitigation | Owner | Review |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

**Risk categories to assess**

| Category | Question |
| --- | --- |
| Availability | What happens when they are down? |
| Viability | Are they financially stable? Have they been acquired? |
| Lock-in | Could we leave? At what cost and over what timeframe? |
| Data | What do they hold and can we get it back in a usable form? |
| Change | Can they change the interface unilaterally? What notice do we get? |
| Concentration | How much do we depend on this one provider? |
| Fourth party | Who do they depend on? |
| Contract | When does it expire and who is watching? |
| Knowledge | Does anyone here understand the integration well enough to replace it? |

---

## 9. Manual and non-technical dependencies

> Dependencies with no system integration. Found by asking, not by scanning.

| Dependency | What it provides | Frequency | Who performs | Failure impact | Contingency |
| --- | --- | --- | --- | --- | --- |
| | *(portal download, emailed file, phone confirmation, individual consultant)* | | | | |

---

## Change log

| Version | Date | Author | Change |
| --- | --- | --- | --- |
| 0.1.0 | | | Initial draft |
