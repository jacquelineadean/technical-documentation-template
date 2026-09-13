#!/usr/bin/env python3
"""Generate CATALOG.md — an inventory of every document in the corpus.

Reads front matter from every markdown file and emits a single table grouped by
layer, plus ownership and freshness summaries. Run it after adding documents; CI
runs it with --check to fail when CATALOG.md is out of date.

Zero dependencies: Python 3.9+ standard library only.

Usage:
    python3 tools/build_catalog.py .              # write CATALOG.md
    python3 tools/build_catalog.py . --check      # fail if CATALOG.md is stale
    python3 tools/build_catalog.py . --stdout     # print instead of writing
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_docs import (  # noqa: E402  (path set up above)
    DOC_TYPES,
    Validator,
    as_list,
    has_placeholder,
    parse_iso_date,
    slugify,
)

LAYERS = [
    ("0 · Foundations", ["sys", "cap", "dmap", "raci", "glos"]),
    ("1 · Architecture", ["tad", "adr", "hld", "lld", "cmp", "int", "bat", "nfr",
                          "sec", "res", "dep", "lga", "mod"]),
    ("2 · Data", ["dgc", "ddc", "dd", "cdm", "dln", "rdr", "dqr", "dct", "mdm",
                  "met", "drc", "dil"]),
    ("3 · Interfaces", ["icat", "icd", "api", "fis", "emc", "edr", "pon", "sla"]),
    ("4 · Domain", ["dom", "bpf", "brc", "sml", "dde", "dim"]),
    ("5 · Operations", ["run", "jsc", "mon", "irp", "drp", "rcm", "cpp"]),
    ("6 · Change", ["brd", "fsp", "imp", "rtm", "tst", "cut"]),
    ("Meta", ["guide", "checklist"]),
]

STATUS_MARK = {
    "approved": "🟢 approved",
    "in-review": "🟡 in-review",
    "draft": "⚪ draft",
    "deprecated": "🟠 deprecated",
    "superseded": "🔵 superseded",
    "retired": "⚫ retired",
}


def escape_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def contents_table(sections: list[tuple[str, str]]) -> list[str]:
    """Render the Contents table from the sections actually emitted below it.

    Built from the real section list rather than a fixed one, because which
    layers appear depends on what the corpus contains.
    """
    lines = ["## Contents", "", "| Section | Summary |", "| --- | --- |"]
    for title, summary in sections:
        lines.append(f"| [{escape_cell(title)}](#{slugify(title)}) | {escape_cell(summary)} |")
    return lines + [""]


def build(root: Path, today: date) -> str:
    validator = Validator(root=root, today=today)
    for path in validator.discover(root):
        validator.load(path)

    docs = [d for d in validator.documents if not d.relaxed]
    templates = [d for d in validator.documents if d.relaxed]

    by_layer: dict[str, list] = defaultdict(list)
    layer_of = {t: name for name, types in LAYERS for t in types}
    for doc in docs:
        doc_type = str(doc.front_matter.get("doc_type", "")).lower()
        by_layer[layer_of.get(doc_type, "Unclassified")].append(doc)

    sections: list[tuple[str, str]] = []
    lines: list[str] = []

    sections.append(("Summary",
                     "Document and template counts, status mix, reviews overdue"))
    lines += [
        "## Summary",
        "",
        "| | Count |",
        "| --- | --- |",
        f"| Documents | {len(docs)} |",
        f"| Templates available | {len(templates)} |",
    ]

    statuses = Counter(str(d.front_matter.get("status", "unknown")) for d in docs)
    for status, _types in [(s, None) for s in
                           ["approved", "in-review", "draft", "deprecated",
                            "superseded", "retired"]]:
        if statuses.get(status):
            lines.append(f"| {STATUS_MARK.get(status, status)} | {statuses[status]} |")

    overdue = sum(1 for row in validator.stale_report() if row["days_overdue"] > 0)
    lines += [f"| Overdue for review | {overdue} |", ""]

    for layer_name, _types in LAYERS:
        layer_docs = by_layer.get(layer_name)
        if not layer_docs:
            continue
        sections.append((layer_name,
                         f"{len(layer_docs)} document(s) — ID, title, status, "
                         f"version, owner, next review, path"))
        lines += [
            f"## {layer_name}",
            "",
            "| Doc ID | Title | Status | Version | Owner | Next review | Path |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for doc in sorted(layer_docs, key=lambda d: (d.doc_id or "zzz", d.rel)):
            fm = doc.front_matter
            next_review = str(fm.get("next_review", "") or "—")
            if has_placeholder(next_review):
                next_review = "—"
            due = parse_iso_date(next_review)
            if due is not None and due < today:
                next_review = f"⚠️ {next_review}"
            lines.append(
                f"| `{escape_cell(doc.doc_id or '—')}` "
                f"| [{escape_cell(fm.get('title', doc.rel))}]({doc.rel}) "
                f"| {STATUS_MARK.get(str(fm.get('status')), str(fm.get('status', '—')))} "
                f"| {escape_cell(fm.get('version', '—'))} "
                f"| {escape_cell(fm.get('owner', '—'))} "
                f"| {next_review} "
                f"| `{doc.rel}` |"
            )
        lines.append("")

    if by_layer.get("Unclassified"):
        sections.append(("Unclassified",
                         "Documents whose `doc_type` is absent from the registry"))
        lines += ["## Unclassified", "",
                  "> These documents have a `doc_type` not present in the registry.", ""]
        for doc in by_layer["Unclassified"]:
            lines.append(f"- `{doc.rel}` — doc_type `{doc.front_matter.get('doc_type')}`")
        lines.append("")

    # Ownership view — who carries the documentation load, and where it concentrates.
    owners = Counter(str(d.front_matter.get("owner", "unassigned")) for d in docs)
    if owners:
        sections.append(("Ownership", "Documents per owning role"))
        lines += ["## Ownership", "", "| Owner | Documents |", "| --- | --- |"]
        for owner, count in sorted(owners.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"| {escape_cell(owner)} | {count} |")
        lines.append("")

    # Coverage against the template set: which document types exist for which system.
    systems: dict[str, set[str]] = defaultdict(set)
    for doc in docs:
        doc_type = str(doc.front_matter.get("doc_type", "")).lower()
        for system in as_list(doc.front_matter.get("systems")):
            systems[str(system)].add(doc_type)
    if systems:
        sections.append(("Coverage by system",
                         "Document types present per system, against the available types"))
        lines += ["## Coverage by system", "",
                  "Document types present for each system, against the "
                  f"{len(DOC_TYPES) - 2} available types.", "",
                  "| System | Types present | Coverage |", "| --- | --- | --- |"]
        available = len(DOC_TYPES) - 2  # exclude guide/checklist
        for system, types in sorted(systems.items()):
            real = {t for t in types if t not in {"guide", "checklist"}}
            if not real:
                continue
            lines.append(f"| {escape_cell(system)} | {len(real)} | "
                         f"{100 * len(real) // available}% |")
        lines.append("")

    header = [
        "# Document Catalog",
        "",
        "> Generated by `tools/build_catalog.py`. Do not edit by hand — rerun the tool.",
        f"> Last generated: {today.isoformat()}",
        "",
    ]
    return "\n".join(header + contents_table(sections) + lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate CATALOG.md from front matter.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if CATALOG.md differs from generated output")
    parser.add_argument("--stdout", action="store_true", help="print instead of writing")
    parser.add_argument("--today", metavar="YYYY-MM-DD")
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    today = date.today()
    if args.today:
        parsed = parse_iso_date(args.today)
        if parsed is None:
            print(f"error: --today must be ISO-8601, got {args.today!r}", file=sys.stderr)
            return 2
        today = parsed

    content = build(root, today)
    target = root / "CATALOG.md"

    if args.stdout:
        print(content, end="")
        return 0

    if args.check:
        if not target.exists():
            print("error: CATALOG.md is missing — run tools/build_catalog.py", file=sys.stderr)
            return 1
        existing = target.read_text(encoding="utf-8")
        # The generated-on date changes every run; compare everything else.
        strip = lambda s: "\n".join(
            l for l in s.split("\n") if not l.startswith("> Last generated:"))
        if strip(existing) != strip(content):
            print("error: CATALOG.md is out of date — run tools/build_catalog.py",
                  file=sys.stderr)
            return 1
        print("CATALOG.md is up to date.")
        return 0

    target.write_text(content, encoding="utf-8")
    print(f"Wrote {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
