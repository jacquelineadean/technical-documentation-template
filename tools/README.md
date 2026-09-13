# Tools

Two standard-library Python scripts. No dependencies, no install step, Python 3.9+.

| Script | Purpose |
| --- | --- |
| [`validate_docs.py`](validate_docs.py) | Front matter, document IDs, links, diagrams, staleness, impact traversal |
| [`build_catalog.py`](build_catalog.py) | Generates `CATALOG.md` — the corpus inventory |

---

## Contents

| Section | Summary |
| --- | --- |
| [`validate_docs.py`](#validate_docspy) | Invocation, exit codes, scoped runs, rule table, relaxed mode, exempt files, impact graph |
| [`build_catalog.py`](#build_catalogpy) | Catalog generation, `--check` in CI, date-insensitive comparison |
| [Extending the validator](#extending-the-validator) | Adding a document type or a rule, and the three places to keep in agreement |
| [Why no third-party linters?](#why-no-third-party-linters) | Rationale: repo-specific conventions, no `npm install` dependency |

---

## `validate_docs.py`

```bash
python3 tools/validate_docs.py .                        # validate everything
python3 tools/validate_docs.py systems/meridian         # validate one subtree
python3 tools/validate_docs.py . --strict               # warnings fail too
python3 tools/validate_docs.py . --format json          # machine-readable
python3 tools/validate_docs.py . --stale-report         # documents past review
python3 tools/validate_docs.py . --impact TAD-OPS-001   # downstream traversal
python3 tools/validate_docs.py . --today 2026-09-12     # pin the date for CI
```

Exit codes: `0` clean, `1` errors found (or warnings with `--strict`), `2` bad invocation.

### Scoped runs

Findings are reported only for the path you name, but the **whole repository is always
loaded** so that document-ID uniqueness and the `upstream_docs` / `downstream_docs` graph
resolve. Without this, validating a single file would report every document it references as
unknown:

```
$ python3 tools/validate_docs.py examples/meridian/01-architecture/tad-order-processing.md
Checked 1 document(s) (88 more loaded to resolve cross-references): 0 error(s), 0 warning(s).
```

The repository root is found by walking up for a `.git` directory or a `templates/`
directory; outside a repository the tool falls back to the target itself.

### Rules enforced

| Rule | Severity | Check |
| --- | --- | --- |
| FM-01 | error | Front matter present and parseable |
| FM-02 | error/warn | Required fields present; `systems` populated |
| FM-03 | error | `doc_id` matches `<TYPE>-<SCOPE>-<NNN>` or `GUIDE`/`CHK-<NNN>` |
| FM-04 | error | `doc_id` globally unique |
| FM-05 | error | `doc_id` prefix agrees with `doc_type` |
| FM-06 | error | `status`, `classification`, `review_cycle` are valid enum values |
| FM-07 | error | `version` is valid semver |
| FM-08 | error | Dates are real ISO-8601 dates |
| FM-09 | error | `approved` implies `last_reviewed`, `next_review`, `review_cycle` — **except** `review_cycle: on-change` documents, which are historical records exempt from calendar review |
| FM-10 | error | `superseded` implies `superseded_by` |
| FM-11 | warning | `upstream_docs`/`downstream_docs` resolve to known IDs |
| FM-12 | warning | `next_review` is in the future |
| FM-13 | warning | `owner` looks like a role, not a person's name |
| LN-01 | error | Relative links resolve to an existing file |
| LN-02 | warning | Anchor links resolve to a heading in the target |
| MD-01 | error | Code fences balanced; mermaid blocks declare a known diagram type |
| MD-02 | warning | H1 matches front-matter `title`; an ADR's `<DOC-ID>: ` prefix is accepted |
| MD-03 | warning | No unresolved TODO/TBD/FIXME in an `approved` document (mentions inside backticks or quotes are ignored) |
| MD-04 | warning | Mermaid labels escape `&`; no commas inside `erDiagram` type declarations |
| MD-05 | warning | A `## Contents` table is present and links to every `##` section; skipped below 3 sections |

Full definitions: [`guides/03-front-matter-schema.md`](../guides/03-front-matter-schema.md).

### Relaxed mode

Files under `templates/` are validated in **relaxed** mode. They carry deliberate
placeholders (`<SCOPE>`, `<YYYY-MM-DD>`, `<Role>`) that would fail strict format checks.
Structure is still enforced: front matter must parse, required keys must exist, links must
resolve, mermaid must be well-formed.

### Exempt files

`README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE.md`, the generated `CATALOG.md`,
and any `*/README.md` directory index are navigation rather than documents, and are not
required to carry front matter. Everything else under a documentation tree is.

### The impact graph

`--impact` traverses the `upstream_docs` / `downstream_docs` declarations breadth-first.
An `upstream_docs: [A]` entry on document B implies B is downstream of A, so the graph
works even when only one direction is declared — which in practice is what happens.

```
$ python3 tools/validate_docs.py . --impact ICD-VND-001
Impact of changing ICD-VND-001 (examples/meridian/03-interfaces/icd-vendor-dispatch-outbound.md):
  └─ DLN-OPS-001     examples/meridian/02-data/lineage-order-to-cash.md  [owner: Order Data Steward]
```

This is the **mechanical floor** for an impact assessment, not the whole of it. It cannot
find the spreadsheet somebody built on an extract, the partner whose parser is stricter
than the spec, or the batch job that depends on an implicit ordering. Use it as the
starting point for
[`templates/06-change/impact-assessment.md`](../templates/06-change/impact-assessment.md).

---

## `build_catalog.py`

```bash
python3 tools/build_catalog.py .            # write CATALOG.md
python3 tools/build_catalog.py . --check    # fail if CATALOG.md is stale (CI)
python3 tools/build_catalog.py . --stdout   # print instead of writing
```

Produces an inventory grouped by layer, plus an ownership breakdown and per-system type
coverage. `--check` ignores the generated-on date so a rerun on a different day does not
fail CI spuriously.

---

## Extending the validator

To add a document type, edit `DOC_TYPES` in `validate_docs.py` and the layer mapping in
`build_catalog.py`, then update the registry in
[`guides/03-front-matter-schema.md`](../guides/03-front-matter-schema.md). Keeping the three
in agreement is checked only by review, so mention it in the PR.

To add a rule, add a `check_*` method on `Validator`, call it from `run()`, and document it
in the table above and in the front-matter schema guide. Choose `error` only when the
finding is unambiguous — a noisy validator gets disabled, and a disabled validator enforces
nothing.

---

## Why no third-party linters?

`markdownlint`, `vale`, and link checkers are all useful, and nothing here prevents adding
them. They are deliberately not required, because this validator enforces the conventions
that are specific to *this* documentation system — the ID registry, the layer model, the
dependency graph — and it has to run in environments where `npm install` is not available.
Prose and formatting linting is a separate, optional concern.
