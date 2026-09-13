# Contributing

## Three kinds of contribution

| Kind | What it is | Review needed |
| --- | --- | --- |
| **Documents** | Adding or updating documentation about a system | Per the approval matrix in [`guides/04-document-lifecycle-and-governance.md`](guides/04-document-lifecycle-and-governance.md#5-approval-matrix) |
| **Templates** | Changing the shape of a document type for everyone | Documentation Architect + one practitioner who has used the template |
| **Tooling** | Validators, CI, catalog generation | Documentation Architect |

---

## Before you open a pull request

```bash
python3 tools/validate_docs.py .          # must pass with zero errors
python3 tools/build_catalog.py .          # if you added or removed documents
```

Both are standard-library Python 3.9+. No install step.

---

## Contributing a document

1. **Copy the template.** Never edit a file in `templates/` to produce a document.
2. **Fill in the front matter first.** `doc_id`, `owner`, `classification`, and the
   `upstream_docs` / `downstream_docs` graph. The graph is what makes mechanical impact
   analysis possible; leaving it empty removes that capability for everyone downstream.
3. **Delete the guidance blocks.** Every template has `>` blockquotes explaining how to
   fill each section. Remove them.
4. **Mark sections you deliberately skipped** as `Not applicable — <reason>`. An empty
   section is ambiguous between "nothing to say" and "not done yet".
5. **Tag every claim about existing behaviour** with `✅ Verified` / `🟡 Inferred` /
   `🔴 Assumed` and its evidence. See
   [documentation standards §3](guides/01-documentation-standards.md#3-confidence-levels).
6. **Complete the relevant checklist** from
   [`guides/08-review-checklists.md`](guides/08-review-checklists.md) in the PR body.

### Where documents live

This repository ships templates, guides, and a worked example. Real documentation for a
real system goes in `systems/<system-name>/`, mirroring the layer structure:

```
systems/meridian/
├── 00-foundations/
├── 01-architecture/
├── 02-data/
├── 03-interfaces/
├── 04-domain/
│   ├── order-processing/
│   └── sales-processing-and-reporting/
├── 05-operations/
└── 06-change/
```

Whether that lives here or in the system's own repository is a local decision. Keeping it
next to the code improves change coupling; keeping it here improves discoverability across
systems. Pick one and be consistent — documentation split across both is found in neither.

---

## Contributing a template change

Templates are shared infrastructure. A change affects every document already produced from
them, so:

1. **State the problem the change solves**, with an example of a document that suffered
   from the current shape.
2. **Prefer adding an optional section** over restructuring. Restructuring orphans the
   documents already written.
3. **Say what existing documents should do.** Most template changes should be
   "applies to new documents; existing ones adopt it at their next review". A change that
   requires retrofitting needs to justify the cost.
4. **Update the registry** in [`guides/03-front-matter-schema.md`](guides/03-front-matter-schema.md)
   if you add a document type — new `doc_type`, ID prefix, approval route, and a validator
   entry in `tools/validate_docs.py`.
5. **Update the README index** and regenerate `CATALOG.md`.

### Adding a new document type

A new type earns its place when an existing one cannot hold the content without becoming
two documents. Before proposing one, check whether the content belongs in a different
layer — that is the more common answer.

Required with the proposal:

- the question the type answers that no existing type does
- its owner role and approval route
- its review cadence
- three examples of documents that would use it

---

## Contributing to the worked example

`examples/meridian/` is a fictional system used to show depth. Contributions must keep it
**internally consistent**: the interface IDs, rule IDs, job names, table names, and figures
cross-reference each other across a dozen documents. A change to the dispatch job's name in
one document must be made everywhere it appears.

Run the validator after any change; it catches broken cross-references but not
inconsistent prose — check that by hand.

---

## Style

Full guidance in [`guides/01-documentation-standards.md`](guides/01-documentation-standards.md).
The points that come up most in review:

- Present tense, active voice, named actors.
- Numbers, not adjectives. Percentiles, not averages.
- Link, do not copy. Duplicated facts diverge.
- `—` for "none"; `🔴 Unknown` for "not known". A blank cell is ambiguous between them.
- Owners are roles, not people.
- Diagrams support prose; they never carry a fact alone.

---

## Review posture

Reviewers check four things, in this order:

1. **Could a competent newcomer act on this** without asking a question the document
   should have answered?
2. **Is every claim about existing behaviour** either obviously checkable or
   confidence-tagged with evidence?
3. **Does any fact here belong in a different layer?**
4. **Is anything here that must never be committed** — credentials, keys, internal
   hostnames in a partner-facing document, real personal data?

Style nits are worth raising once, with a link to the standard. They are not worth a
second round.
