<!--
Delete the sections that do not apply. The documentation-obligation section is not
optional for changes that touch system behaviour — see
guides/04-document-lifecycle-and-governance.md §3.
-->

## What this changes

<!-- One or two sentences. -->

## Type of change

- [ ] New document(s)
- [ ] Update to existing document(s)
- [ ] Template change (affects everyone using this repository)
- [ ] Tooling / CI
- [ ] Worked example

## Documentation obligations

Which of these triggers apply, and where is the corresponding documentation change?

| Trigger | Applies | Document updated |
| --- | --- | --- |
| Interface payload, endpoint, or semantics changed | ☐ | |
| New external partner or vendor | ☐ | |
| Business rule added, changed, or retired | ☐ | |
| New or changed derived field / metric | ☐ | |
| Batch job added, removed, or re-sequenced | ☐ | |
| Component added or decommissioned | ☐ | |
| Architecture decision taken | ☐ | |
| Reference data code set extended | ☐ | |
| Sev-1/Sev-2 incident | ☐ | |
| Regulatory or audit finding | ☐ | |

> "Docs to follow" is how a documentation corpus dies. The change and its
> documentation land together.

## Impact

<!--
Paste the output of:
    python3 tools/validate_docs.py . --impact <DOC-ID>
and say, for each downstream document, whether it is updated here or unaffected.
-->

## Checklist

- [ ] `python3 tools/validate_docs.py .` passes
- [ ] `python3 tools/build_catalog.py .` run if documents were added or removed
- [ ] Front matter complete; `owner` is a role, not a person
- [ ] Claims about existing behaviour carry a confidence tag with evidence
- [ ] Every `🔴 Assumed` item has a named owner and a target date
- [ ] No credentials, keys, internal hostnames, or real personal data
- [ ] Diagrams have captions; prose carries the facts
- [ ] Relevant checklist from `guides/08-review-checklists.md` completed

## Reviewers

<!-- Per the approval matrix in guides/04-document-lifecycle-and-governance.md §5. -->
