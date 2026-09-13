# Templates

58 document templates, grouped by layer. The full index with a one-line purpose for each is
in the [repository README](../README.md#template-index).

| Layer | Directory | Count |
| --- | --- | --- |
| 0 · Foundations | [`00-foundations/`](00-foundations/) | 5 |
| 1 · Architecture | [`01-architecture/`](01-architecture/) | 14 |
| 2 · Data | [`02-data/`](02-data/) | 12 |
| 3 · Interfaces | [`03-interfaces/`](03-interfaces/) | 8 |
| 4 · Domain | [`04-domain/`](04-domain/) | 6 |
| 5 · Operations | [`05-operations/`](05-operations/) | 7 |
| 6 · Change | [`06-change/`](06-change/) | 6 |

---

## How to use a template

1. **Copy it.** Never edit a file here to produce a document — improvements to a template are
   a separate PR against this directory.
2. **Fill in the front matter first.** `doc_id`, `owner`, `classification`, and the
   `upstream_docs` / `downstream_docs` graph. The graph is what makes
   `tools/validate_docs.py --impact` work; leaving it empty removes that capability for
   everyone downstream of you.
3. **Delete the guidance.** Every template carries `>` blockquotes explaining how to fill
   each section. Remove them as you go.
4. **Mark skipped sections** as `Not applicable — <reason>`. An empty section is ambiguous
   between "nothing to say" and "not finished".
5. **Tag claims about existing behaviour** with `✅ Verified` / `🟡 Inferred` / `🔴 Assumed`
   and the evidence. See
   [documentation standards §3](../guides/01-documentation-standards.md#3-confidence-levels).

```bash
cp templates/01-architecture/technical-architecture-document.md \
   systems/<system>/01-architecture/tad-<subsystem>.md
python3 tools/validate_docs.py systems/<system>
```

---

## Validation in relaxed mode

Files in this directory are validated in **relaxed** mode: they carry deliberate placeholders
(`<SCOPE>`, `<YYYY-MM-DD>`, `<Role>`) that would fail strict format checks. Structure is
still enforced — front matter must parse, required keys must exist, relative links must
resolve, and Mermaid blocks must be well-formed.

This means a broken link or a malformed diagram in a template fails CI, while the
placeholders do not. See [`tools/README.md`](../tools/README.md#relaxed-mode).

---

## Seeing a template filled in

Every major template has a worked instance in [`examples/meridian/`](../examples/meridian/).
Blank templates teach structure; the example teaches depth — how much detail a lineage
document actually needs, or what a business rule looks like when it has survived four
re-platformings.

| Template | Worked example |
| --- | --- |
| [Technical Architecture Document](01-architecture/technical-architecture-document.md) | [TAD-OPS-001](../examples/meridian/01-architecture/tad-order-processing.md) |
| [Architecture Decision Record](01-architecture/architecture-decision-record.md) | [ADR-OPS-0007](../examples/meridian/01-architecture/adr-0007-externalise-hold-evaluation.md) · [ADR-PLR-0012](../examples/meridian/01-architecture/adr-0012-package-decoding-rules-as-data.md) *(retrospective)* |
| [Batch & Scheduling Architecture](01-architecture/batch-and-scheduling-architecture.md) | [BAT-MER-001](../examples/meridian/01-architecture/batch-and-scheduling-architecture.md) |
| [Legacy System Archaeology](01-architecture/legacy-system-archaeology.md) | [LGA-OPS-001](../examples/meridian/01-architecture/legacy-system-archaeology-order-decoder.md) |
| [Data Governance Charter](02-data/data-governance-charter.md) | [DGC-MER-001](../examples/meridian/02-data/data-governance-charter.md) |
| [Data Lineage Document](02-data/data-lineage-document.md) | [DLN-OPS-001](../examples/meridian/02-data/lineage-order-to-cash.md) · [DLN-SPR-001](../examples/meridian/02-data/lineage-sales-incentive-payout.md) |
| [Data Dictionary](02-data/data-dictionary.md) | [DD-OPS-001](../examples/meridian/02-data/data-dictionary-order-line.md) |
| [Reference Data Registry](02-data/reference-data-and-code-set-registry.md) | [RDR-PLR-001](../examples/meridian/02-data/reference-data-option-codes.md) |
| [Data Contract](02-data/data-contract.md) | [DCT-VND-001](../examples/meridian/02-data/data-contract-vendor-shipping-confirmation.md) |
| [Metric & KPI Catalog](02-data/metric-and-kpi-definition-catalog.md) | [MET-SPR-001](../examples/meridian/02-data/metric-catalog-sales-reporting.md) |
| [Interface Catalog](03-interfaces/interface-catalog.md) | [ICAT-MER-001](../examples/meridian/03-interfaces/interface-catalog.md) |
| [Interface Control Document](03-interfaces/interface-control-document.md) | [ICD-VND-001](../examples/meridian/03-interfaces/icd-vendor-dispatch-outbound.md) |
| [External Dependency Register](03-interfaces/external-dependency-register.md) | [EDR-MER-001](../examples/meridian/03-interfaces/external-dependency-register.md) |
| [Domain Overview](04-domain/domain-overview.md) | [DOM-OPS-001](../examples/meridian/04-domains/order-processing.md) · [DOM-PLR-001](../examples/meridian/04-domains/product-launch-readiness.md) · [DOM-SPR-001](../examples/meridian/04-domains/sales-processing-and-reporting.md) |
| [Job Schedule Catalog](05-operations/job-schedule-catalog.md) | [JSC-MER-001](../examples/meridian/05-operations/job-schedule-catalog.md) |
| [Runbook](05-operations/runbook.md) | [RUN-OPS-001](../examples/meridian/05-operations/runbook-nightly-order-cycle.md) |
| [System Profile](00-foundations/system-profile.md) | [SYS-MER-001](../examples/meridian/00-foundations/system-profile.md) |
| [Domain Map](00-foundations/domain-map.md) | [DMAP-MER-001](../examples/meridian/00-foundations/domain-map.md) |

The templates with no worked example — HLD, LLD, component spec, NFRs, security, resilience,
deployment, modernization, and the Layer 6 change set — are the ones whose shape is less
contested. The example concentrates on the architecture and data documents, which is where
depth is hardest to judge from a blank form.
