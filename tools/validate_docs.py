#!/usr/bin/env python3
"""Validate documentation against the conventions in guides/.

Zero dependencies: Python 3.9+ standard library only, so it runs in CI without an
install step and on a locked-down corporate laptop without a virtualenv.

Checks (see guides/03-front-matter-schema.md §9 for the rule IDs):

  FM-*  front matter presence, required fields, enums, formats, uniqueness
  LN-*  relative links resolve; anchors resolve
  MD-*  mermaid fences balanced and typed; H1 matches title; no bare TODOs

Usage:
    python3 tools/validate_docs.py .                  # validate the whole repo
    python3 tools/validate_docs.py systems/meridian   # validate one subtree
    python3 tools/validate_docs.py . --stale-report    # list documents past review
    python3 tools/validate_docs.py . --impact TAD-OPS-001
    python3 tools/validate_docs.py . --format json

Exit codes: 0 = no errors, 1 = errors found, 2 = bad invocation.

Files under templates/ are validated in RELAXED mode: they carry deliberate
placeholders (`<SCOPE>`, `<YYYY-MM-DD>`) that would fail strict format checks. Their
structure is still checked — front matter must be present and parseable, required
keys must exist, links must resolve, and mermaid must be well-formed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------------------
# Schema — keep in sync with guides/03-front-matter-schema.md
# --------------------------------------------------------------------------------------

REQUIRED_FIELDS = ["doc_id", "title", "doc_type", "status", "version", "owner", "classification"]
APPROVED_EXTRA_FIELDS = ["last_reviewed", "next_review", "review_cycle"]

STATUSES = {"draft", "in-review", "approved", "deprecated", "superseded", "retired"}
CLASSIFICATIONS = {"public", "internal", "confidential", "restricted"}
REVIEW_CYCLES = {"quarterly", "semi-annual", "annual", "on-change"}

# doc_type -> document-ID prefix.
DOC_TYPES = {
    # Layer 0
    "sys": "SYS", "cap": "CAP", "dmap": "DMAP", "raci": "RACI", "glos": "GLOS",
    # Layer 1
    "tad": "TAD", "adr": "ADR", "hld": "HLD", "lld": "LLD", "cmp": "CMP",
    "int": "INT", "bat": "BAT", "nfr": "NFR", "sec": "SEC", "res": "RES",
    "dep": "DEP", "lga": "LGA", "mod": "MOD",
    # Layer 2
    "dgc": "DGC", "ddc": "DDC", "dd": "DD", "cdm": "CDM", "dln": "DLN",
    "rdr": "RDR", "dqr": "DQR", "dct": "DCT", "mdm": "MDM", "met": "MET",
    "drc": "DRC", "dil": "DIL",
    # Layer 3
    "icat": "ICAT", "icd": "ICD", "api": "API", "fis": "FIS", "emc": "EMC",
    "edr": "EDR", "pon": "PON", "sla": "SLA",
    # Layer 4
    "dom": "DOM", "bpf": "BPF", "brc": "BRC", "sml": "SML", "dde": "DDE", "dim": "DIM",
    # Layer 5
    "run": "RUN", "jsc": "JSC", "mon": "MON", "irp": "IRP", "drp": "DRP",
    "rcm": "RCM", "cpp": "CPP",
    # Layer 6
    "brd": "BRD", "fsp": "FSP", "imp": "IMP", "rtm": "RTM", "tst": "TST", "cut": "CUT",
    # Meta
    "guide": "GUIDE", "checklist": "CHK",
}

REVIEW_INTERVAL_DAYS = {"quarterly": 92, "semi-annual": 184, "annual": 366}

DOC_ID_RE = re.compile(r"^[A-Z]{2,5}-[A-Z0-9]{2,6}-\d{3,4}$")
META_DOC_ID_RE = re.compile(r"^(GUIDE|CHK)-\d{3}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PLACEHOLDER_RE = re.compile(r"<[^>]*>")

MERMAID_TYPES = {
    "flowchart", "graph", "sequencediagram", "statediagram", "statediagram-v2",
    "erdiagram", "classdiagram", "gantt", "timeline", "mindmap", "quadrantchart",
    "journey", "pie", "gitgraph", "c4context", "requirementdiagram", "sankey-beta",
    "xychart-beta", "block-beta", "packet-beta",
}

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".github"}

# Front matter keys holding lists of document IDs, for the impact graph.
GRAPH_FIELDS = ("upstream_docs", "downstream_docs")


# --------------------------------------------------------------------------------------
# Minimal YAML front matter parser
# --------------------------------------------------------------------------------------

def _coerce(raw: str) -> Any:
    """Convert a scalar token to str / bool / None, stripping quotes and comments."""
    value = raw.strip()
    if not value:
        return ""
    if value[0] in "\"'" and value[-1] == value[0] and len(value) > 1:
        return value[1:-1]
    # Strip trailing comments only when unquoted and preceded by whitespace.
    hash_pos = value.find(" #")
    if hash_pos != -1:
        value = value[:hash_pos].rstrip()
    lowered = value.lower()
    if lowered in {"true", "yes"}:
        return True
    if lowered in {"false", "no"}:
        return False
    if lowered in {"null", "~"}:
        return None
    return value


def _parse_inline_list(raw: str) -> list:
    inner = raw.strip()[1:-1].strip()
    if not inner:
        return []
    # Front matter lists here never contain nested structures, so a plain split is safe.
    return [_coerce(part) for part in inner.split(",") if part.strip()]


def parse_front_matter(text: str) -> tuple[dict | None, str, str | None]:
    """Return (front_matter, body, error).

    front_matter is None when the document has no ``---`` delimited block.
    """
    if not text.startswith("---"):
        return None, text, None

    lines = text.split("\n")
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() in {"---", "..."}:
            end = index
            break
    if end is None:
        return None, text, "front matter opened with '---' but never closed"

    data: dict[str, Any] = {}
    pending_key: str | None = None
    for lineno, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        # Continuation of a block list: "  - value"
        stripped = line.strip()
        if stripped.startswith("- ") or stripped == "-":
            if pending_key is None:
                return None, text, f"line {lineno}: list item outside of a key"
            item = _coerce(stripped[1:].strip()) if stripped != "-" else ""
            if not isinstance(data.get(pending_key), list):
                data[pending_key] = []
            data[pending_key].append(item)
            continue

        if ":" not in line:
            return None, text, f"line {lineno}: expected 'key: value', got {line.strip()!r}"

        key, _, raw_value = line.partition(":")
        key = key.strip()
        raw_value = raw_value.strip()

        if raw_value.startswith("[") and raw_value.endswith("]"):
            data[key] = _parse_inline_list(raw_value)
            pending_key = None
        elif raw_value == "":
            # Either an empty scalar or the header of a block list; decided by what follows.
            data[key] = ""
            pending_key = key
        else:
            data[key] = _coerce(raw_value)
            pending_key = None

    body = "\n".join(lines[end + 1:])
    return data, body, None


# --------------------------------------------------------------------------------------
# Findings
# --------------------------------------------------------------------------------------

@dataclass
class Finding:
    path: str
    rule: str
    severity: str  # "error" | "warning"
    message: str
    line: int | None = None

    def render(self) -> str:
        where = f"{self.path}:{self.line}" if self.line else self.path
        return f"{where}: {self.severity}: [{self.rule}] {self.message}"

    def to_dict(self) -> dict:
        return {
            "path": self.path, "line": self.line, "rule": self.rule,
            "severity": self.severity, "message": self.message,
        }


@dataclass
class Document:
    path: Path
    rel: str
    front_matter: dict
    body: str
    relaxed: bool
    doc_id: str | None = None
    upstream: list[str] = field(default_factory=list)
    downstream: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------------------

def has_placeholder(value: Any) -> bool:
    return isinstance(value, str) and bool(PLACEHOLDER_RE.search(value))


def as_list(value: Any) -> list:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    return [value]


def parse_iso_date(value: str) -> date | None:
    if not ISO_DATE_RE.match(value):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def slugify(heading: str) -> str:
    """Reproduce GitHub's heading-anchor algorithm.

    Lowercase, drop everything that is not word/space/hyphen, then map each
    whitespace character to one hyphen. Runs of spaces are *not* collapsed —
    "ICD — Interface" becomes "icd--interface" because the em dash is removed
    and both surrounding spaces survive as hyphens.
    """
    slug = re.sub(r"[^\w\s-]", "", heading.lower())
    return re.sub(r"\s", "-", slug).strip("-")


def strip_code_and_quotes(line: str) -> str:
    """Blank out inline code spans and quoted text.

    Used so that a document *discussing* a marker ("never write `TBD`") is not
    reported as containing one.
    """
    line = re.sub(r"`[^`]*`", "", line)
    return re.sub(r"[\"'“”‘’][^\"'“”‘’]*"
                  r"[\"'“”‘’]", "", line)


class Validator:
    def __init__(self, root: Path, today: date):
        self.root = root
        self.today = today
        self.findings: list[Finding] = []
        self.documents: list[Document] = []
        self.by_id: dict[str, Document] = {}

    # -- helpers ------------------------------------------------------------------

    def add(self, path: str, rule: str, severity: str, message: str, line: int | None = None) -> None:
        self.findings.append(Finding(path, rule, severity, message, line))

    # -- discovery ----------------------------------------------------------------

    def discover(self, target: Path) -> list[Path]:
        if target.is_file():
            return [target]
        found: list[Path] = []
        for dirpath, dirnames, filenames in os.walk(target):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
            for name in sorted(filenames):
                if name.endswith(".md"):
                    found.append(Path(dirpath) / name)
        return found

    # -- per-file -----------------------------------------------------------------

    def load(self, path: Path) -> None:
        rel = str(path.relative_to(self.root)) if path.is_relative_to(self.root) else str(path)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            self.add(rel, "FM-01", "error", f"cannot read file: {exc}")
            return

        front_matter, body, error = parse_front_matter(text)
        if error:
            self.add(rel, "FM-01", "error", error)
            return
        if front_matter is None:
            # Repo-level prose (README, CONTRIBUTING) is exempt; anything under a
            # documentation tree is not.
            if self._is_exempt(rel):
                return
            self.add(rel, "FM-01", "error", "missing YAML front matter")
            return

        relaxed = self._is_template(rel)
        doc = Document(path=path, rel=rel, front_matter=front_matter, body=body, relaxed=relaxed)
        doc_id = front_matter.get("doc_id")
        if isinstance(doc_id, str) and doc_id and not has_placeholder(doc_id):
            doc.doc_id = doc_id
        doc.upstream = [str(v) for v in as_list(front_matter.get("upstream_docs")) if v]
        doc.downstream = [str(v) for v in as_list(front_matter.get("downstream_docs")) if v]
        self.documents.append(doc)

    @staticmethod
    def _is_template(rel: str) -> bool:
        return rel.replace("\\", "/").startswith("templates/")

    @staticmethod
    def _is_exempt(rel: str) -> bool:
        normalised = rel.replace("\\", "/")
        if normalised in {"README.md", "CONTRIBUTING.md", "CHANGELOG.md",
                          "LICENSE.md", "CATALOG.md"}:
            return True
        # Directory index pages are navigation, not documents.
        return normalised.endswith("/README.md")

    # -- front matter -------------------------------------------------------------

    def check_front_matter(self, doc: Document) -> None:
        fm, rel, relaxed = doc.front_matter, doc.rel, doc.relaxed

        for key in REQUIRED_FIELDS:
            if key not in fm or fm[key] in (None, ""):
                self.add(rel, "FM-02", "error", f"required field '{key}' is missing or empty")

        doc_id = fm.get("doc_id")
        if isinstance(doc_id, str) and doc_id:
            if has_placeholder(doc_id):
                if not relaxed:
                    self.add(rel, "FM-03", "error",
                             f"doc_id '{doc_id}' still contains a placeholder")
            elif not (DOC_ID_RE.match(doc_id) or META_DOC_ID_RE.match(doc_id)):
                self.add(rel, "FM-03", "error",
                         f"doc_id '{doc_id}' does not match <TYPE>-<SCOPE>-<NNN> or GUIDE/CHK-<NNN>")

        doc_type = fm.get("doc_type")
        if isinstance(doc_type, str) and doc_type:
            expected = DOC_TYPES.get(doc_type.lower())
            if expected is None:
                self.add(rel, "FM-06", "error",
                         f"doc_type '{doc_type}' is not in the registry "
                         f"(guides/03-front-matter-schema.md §3)")
            elif isinstance(doc_id, str) and doc_id:
                prefix = doc_id.split("-", 1)[0]
                if prefix != expected:
                    self.add(rel, "FM-05", "error",
                             f"doc_id prefix '{prefix}' disagrees with doc_type "
                             f"'{doc_type}' (expected '{expected}')")

        status = fm.get("status")
        if isinstance(status, str) and status and status not in STATUSES:
            self.add(rel, "FM-06", "error",
                     f"status '{status}' is not one of {sorted(STATUSES)}")

        classification = fm.get("classification")
        if isinstance(classification, str) and classification and classification not in CLASSIFICATIONS:
            self.add(rel, "FM-06", "error",
                     f"classification '{classification}' is not one of {sorted(CLASSIFICATIONS)}")

        cycle = fm.get("review_cycle")
        if isinstance(cycle, str) and cycle and cycle not in REVIEW_CYCLES:
            self.add(rel, "FM-06", "error",
                     f"review_cycle '{cycle}' is not one of {sorted(REVIEW_CYCLES)}")

        version = fm.get("version")
        if isinstance(version, str) and version and not SEMVER_RE.match(version):
            self.add(rel, "FM-07", "error", f"version '{version}' is not valid semver")

        for key in ("created", "last_reviewed", "next_review"):
            value = fm.get(key)
            if not isinstance(value, str) or not value:
                continue
            if has_placeholder(value):
                if not relaxed:
                    self.add(rel, "FM-08", "error", f"{key} '{value}' contains a placeholder")
                continue
            if parse_iso_date(value) is None:
                self.add(rel, "FM-08", "error", f"{key} '{value}' is not a valid ISO-8601 date")

        # `on-change` documents (ADRs, BRDs, impact assessments) are historical records:
        # they are exempt from calendar review, so review dates are not required.
        # See guides/03-front-matter-schema.md §6.
        if status == "approved" and not relaxed and cycle != "on-change":
            for key in APPROVED_EXTRA_FIELDS:
                if not fm.get(key):
                    self.add(rel, "FM-09", "error",
                             f"status is 'approved' so '{key}' is required")

        if status == "superseded" and not fm.get("superseded_by"):
            self.add(rel, "FM-10", "error",
                     "status is 'superseded' so 'superseded_by' is required")

        owner = fm.get("owner")
        if isinstance(owner, str) and owner and not has_placeholder(owner):
            self._check_owner_is_role(rel, owner)

        # Meta documents (this repository's own guides and checklists) describe no system.
        is_meta = isinstance(doc_type, str) and doc_type.lower() in {"guide", "checklist"}
        if not is_meta and not as_list(fm.get("systems")):
            self.add(rel, "FM-02", "warning", "'systems' should list at least one entry")

    def _check_owner_is_role(self, rel: str, owner: str) -> None:
        """Heuristic for FM-13: owners must be roles, not people.

        Two capitalised words with no role noun is almost always a person's name.
        """
        role_words = {
            "lead", "owner", "architect", "manager", "steward", "head", "director",
            "custodian", "engineer", "analyst", "officer", "team", "council", "board",
            "sponsor", "chair", "vp", "administrator", "specialist",
        }
        words = re.findall(r"[A-Za-z]+", owner)
        if not words:
            return
        if any(word.lower() in role_words for word in words):
            return
        if len(words) <= 3 and all(word[:1].isupper() for word in words):
            self.add(rel, "FM-13", "warning",
                     f"owner '{owner}' looks like a person's name; owners must be roles "
                     f"(guides/05-ownership-and-raci.md §2)")

    # -- staleness ----------------------------------------------------------------

    def check_staleness(self, doc: Document) -> None:
        if doc.relaxed:
            return
        fm = doc.front_matter
        if fm.get("status") != "approved":
            return
        if fm.get("review_cycle") == "on-change":
            return
        next_review = fm.get("next_review")
        if not isinstance(next_review, str):
            return
        due = parse_iso_date(next_review)
        if due is None:
            return
        if due < self.today:
            days = (self.today - due).days
            self.add(doc.rel, "FM-12", "warning",
                     f"stale: next_review was {next_review} ({days} days ago)")

    # -- links --------------------------------------------------------------------

    def check_links(self, doc: Document) -> None:
        text = doc.body
        # Skip fenced code blocks: they contain illustrative paths, not real links.
        scrubbed_lines = []
        in_fence = False
        for line in text.split("\n"):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                scrubbed_lines.append("")
                continue
            scrubbed_lines.append("" if in_fence else line)

        for lineno, line in enumerate(scrubbed_lines, start=1):
            for match in re.finditer(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", line):
                target = match.group(1)
                if target.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                    continue
                path_part, _, anchor = target.partition("#")
                if not path_part:
                    continue
                resolved = (doc.path.parent / path_part).resolve()
                if not resolved.exists():
                    self.add(doc.rel, "LN-01", "error",
                             f"broken relative link: '{target}'", lineno)
                    continue
                if anchor and resolved.is_file() and resolved.suffix == ".md":
                    self._check_anchor(doc, resolved, target, anchor, lineno)

    def _check_anchor(self, doc: Document, target_path: Path, link: str, anchor: str, lineno: int) -> None:
        try:
            content = target_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return
        slugs = {slugify(line.lstrip("#").strip())
                 for line in content.split("\n") if line.startswith("#")}
        slugs.discard("")
        if anchor.lower() not in slugs:
            self.add(doc.rel, "LN-02", "warning",
                     f"anchor '#{anchor}' not found in link target '{link}'", lineno)

    # -- markdown -----------------------------------------------------------------

    def check_markdown(self, doc: Document) -> None:
        lines = doc.body.split("\n")

        # MD-01: fenced blocks balanced; mermaid blocks declare a known diagram type.
        fence_stack: list[tuple[int, str]] = []
        for lineno, line in enumerate(lines, start=1):
            stripped = line.lstrip()
            if not stripped.startswith("```"):
                continue
            info = stripped[3:].strip()
            if fence_stack and not info:
                fence_stack.pop()
            elif fence_stack and info:
                # An info string while open means the previous fence never closed.
                open_line, open_info = fence_stack[-1]
                self.add(doc.rel, "MD-01", "error",
                         f"code fence opened at line {open_line} "
                         f"({open_info or 'no language'}) is not closed", lineno)
                fence_stack.pop()
                fence_stack.append((lineno, info))
            else:
                fence_stack.append((lineno, info))

            if info.lower() == "mermaid":
                self._check_mermaid(doc, lines, lineno)

        for open_line, info in fence_stack:
            self.add(doc.rel, "MD-01", "error",
                     f"code fence opened at line {open_line} "
                     f"({info or 'no language'}) is never closed", open_line)

        # MD-02: H1 agrees with front-matter title.
        if not doc.relaxed:
            title = doc.front_matter.get("title")
            h1 = next((l[2:].strip() for l in lines if l.startswith("# ")), None)
            if isinstance(title, str) and title and h1 is not None:
                normalise = lambda s: re.sub(r"\s+", " ", s.replace("\\", "")).strip()
                candidate = normalise(h1)
                # ADRs conventionally prefix the H1 with the document ID
                # ("ADR-0007: Externalise ..."); accept that form.
                if doc.doc_id and candidate.startswith(f"{doc.doc_id}:"):
                    candidate = candidate[len(doc.doc_id) + 1:].strip()
                if candidate != normalise(title):
                    self.add(doc.rel, "MD-02", "warning",
                             f"H1 '{h1}' does not match front-matter title '{title}'")

        # MD-03: unresolved TODO/TBD in an approved document.
        if doc.front_matter.get("status") == "approved" and not doc.relaxed:
            in_fence = False
            for lineno, line in enumerate(lines, start=1):
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                if re.search(r"\b(TODO|TBD|FIXME)\b", strip_code_and_quotes(line)):
                    self.add(doc.rel, "MD-03", "warning",
                             "approved document contains an unresolved TODO/TBD/FIXME", lineno)

    def _check_mermaid(self, doc: Document, lines: list[str], fence_line: int) -> None:
        typed = False
        for offset, line in enumerate(lines[fence_line:], start=fence_line + 1):
            stripped = line.strip()
            if stripped.startswith("```"):
                if not typed:
                    self.add(doc.rel, "MD-01", "error", "empty mermaid block", fence_line)
                return
            if not stripped or stripped.startswith("%%"):
                continue

            if not typed:
                typed = True
                first_token = re.split(r"[\s;]", stripped, maxsplit=1)[0].lower()
                if first_token not in MERMAID_TYPES:
                    self.add(doc.rel, "MD-01", "error",
                             f"mermaid block starts with '{first_token}', which is not a "
                             f"recognised diagram type", offset)

            self._check_mermaid_labels(doc, stripped, offset)

    def _check_mermaid_labels(self, doc: Document, line: str, lineno: int) -> None:
        """MD-04: label text must escape characters Mermaid treats as syntax.

        Only label *contents* are checked. A bare ``&`` elsewhere on the line is
        legitimate chaining syntax (``A --> B & C``), so flagging it would be wrong.
        """
        labels = re.findall(r'"([^"]*)"', line)
        labels += re.findall(r"\[([^\[\]\"]*)\]", line)
        for label in labels:
            if re.search(r"&(?!amp;|lt;|gt;|quot;|nbsp;|#\d+;|#x[0-9A-Fa-f]+;)", label):
                self.add(doc.rel, "MD-04", "warning",
                         f"unescaped '&' in a Mermaid label: {label.strip()[:60]!r} "
                         f"— use &amp; (guides/02-diagram-conventions.md §11)", lineno)

        # erDiagram attribute types: Mermaid cannot parse a comma inside decimal(11,2).
        if re.search(r"\b(decimal|numeric|char|varchar)\s*\(\s*\d+\s*,", line):
            self.add(doc.rel, "MD-04", "warning",
                     "comma inside a Mermaid type declaration — write decimal(11-2) and "
                     "note the real type in the data dictionary "
                     "(guides/02-diagram-conventions.md §7)", lineno)

    # -- corpus-level -------------------------------------------------------------

    def check_corpus(self) -> None:
        seen: dict[str, list[str]] = defaultdict(list)
        for doc in self.documents:
            if doc.doc_id:
                seen[doc.doc_id].append(doc.rel)
        for doc_id, paths in sorted(seen.items()):
            if len(paths) > 1:
                for path in paths:
                    self.add(path, "FM-04", "error",
                             f"duplicate doc_id '{doc_id}' also used by "
                             f"{', '.join(p for p in paths if p != path)}")
            else:
                self.by_id[doc_id] = next(d for d in self.documents if d.rel == paths[0])

        known = set(self.by_id)
        for doc in self.documents:
            if doc.relaxed:
                continue
            for field_name in GRAPH_FIELDS:
                for ref in as_list(doc.front_matter.get(field_name)):
                    ref = str(ref)
                    if has_placeholder(ref) or not ref:
                        continue
                    if ref not in known:
                        self.add(doc.rel, "FM-11", "warning",
                                 f"{field_name} references unknown doc_id '{ref}'")

    # -- entry point --------------------------------------------------------------

    def run(self, target: Path) -> None:
        for path in self.discover(target):
            self.load(path)
        for doc in self.documents:
            self.check_front_matter(doc)
            self.check_staleness(doc)
            self.check_links(doc)
            self.check_markdown(doc)
        self.check_corpus()

    # -- reports ------------------------------------------------------------------

    def stale_report(self) -> list[dict]:
        rows = []
        for doc in self.documents:
            fm = doc.front_matter
            if doc.relaxed or fm.get("status") != "approved":
                continue
            if fm.get("review_cycle") == "on-change":
                continue
            next_review = fm.get("next_review")
            due = parse_iso_date(next_review) if isinstance(next_review, str) else None
            if due is None:
                continue
            rows.append({
                "doc_id": doc.doc_id or "(none)",
                "path": doc.rel,
                "owner": fm.get("owner", ""),
                "next_review": next_review,
                "days_overdue": (self.today - due).days,
            })
        rows.sort(key=lambda r: -r["days_overdue"])
        return rows

    def impact(self, doc_id: str) -> list[dict]:
        """Breadth-first traversal of the downstream_docs graph."""
        forward: dict[str, set[str]] = defaultdict(set)
        for doc in self.documents:
            if not doc.doc_id:
                continue
            for ref in doc.downstream:
                forward[doc.doc_id].add(ref)
            # An upstream declaration on B implies B is downstream of A.
            for ref in doc.upstream:
                forward[ref].add(doc.doc_id)

        rows: list[dict] = []
        visited = {doc_id}
        queue = deque([(doc_id, 0)])
        while queue:
            current, depth = queue.popleft()
            for nxt in sorted(forward.get(current, ())):
                if nxt in visited:
                    continue
                visited.add(nxt)
                target = self.by_id.get(nxt)
                rows.append({
                    "doc_id": nxt,
                    "depth": depth + 1,
                    "via": current,
                    "path": target.rel if target else "(not found in corpus)",
                    "owner": target.front_matter.get("owner", "") if target else "",
                })
                queue.append((nxt, depth + 1))
        return rows


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate documentation front matter, links, and diagrams.")
    parser.add_argument("path", nargs="?", default=".", help="file or directory to validate")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as errors")
    parser.add_argument("--stale-report", action="store_true",
                        help="list approved documents past their next_review date")
    parser.add_argument("--impact", metavar="DOC_ID",
                        help="list documents downstream of DOC_ID")
    parser.add_argument("--today", metavar="YYYY-MM-DD",
                        help="override today's date (for reproducible CI runs)")
    args = parser.parse_args(argv)

    target = Path(args.path).resolve()
    if not target.exists():
        print(f"error: path does not exist: {target}", file=sys.stderr)
        return 2

    today = date.today()
    if args.today:
        parsed = parse_iso_date(args.today)
        if parsed is None:
            print(f"error: --today must be ISO-8601, got {args.today!r}", file=sys.stderr)
            return 2
        today = parsed

    root = target if target.is_dir() else target.parent
    validator = Validator(root=root, today=today)
    validator.run(target)

    if args.impact:
        rows = validator.impact(args.impact)
        if args.format == "json":
            print(json.dumps({"impact_of": args.impact, "downstream": rows}, indent=2))
        else:
            origin = validator.by_id.get(args.impact)
            print(f"Impact of changing {args.impact}"
                  f"{' (' + origin.rel + ')' if origin else ''}:")
            if not rows:
                print("  no downstream documents declared")
            for row in rows:
                # Name the edge for indirect rows: indentation alone reads as if the
                # row above were the parent, which is misleading in an impact report.
                via = f"  (via {row['via']})" if row["depth"] > 1 else ""
                print(f"  {'  ' * (row['depth'] - 1)}└─ {row['doc_id']:<16} "
                      f"{row['path']}  [owner: {row['owner'] or 'unassigned'}]{via}")
            print(f"\n{len(rows)} downstream document(s). "
                  f"This is the mechanical floor — extend it with judgement "
                  f"(see templates/06-change/impact-assessment.md).")
        return 0

    if args.stale_report:
        rows = validator.stale_report()
        overdue = [r for r in rows if r["days_overdue"] > 0]
        if args.format == "json":
            print(json.dumps({"documents": rows, "overdue": len(overdue)}, indent=2))
        else:
            print(f"Review status as at {today.isoformat()}\n")
            print(f"{'DOC ID':<16} {'DUE':<12} {'OVERDUE':>8}  OWNER / PATH")
            for row in rows:
                flag = "OVERDUE" if row["days_overdue"] > 0 else ""
                days = f"{row['days_overdue']:+d}d" if row["days_overdue"] > 0 else ""
                print(f"{row['doc_id']:<16} {row['next_review']:<12} {days:>8}  "
                      f"{row['owner']} — {row['path']}")
            print(f"\n{len(overdue)} of {len(rows)} approved documents are overdue for review.")
        return 0

    errors = [f for f in validator.findings if f.severity == "error"]
    warnings = [f for f in validator.findings if f.severity == "warning"]

    if args.format == "json":
        print(json.dumps({
            "documents_checked": len(validator.documents),
            "errors": len(errors),
            "warnings": len(warnings),
            "findings": [f.to_dict() for f in validator.findings],
        }, indent=2))
    else:
        for finding in sorted(validator.findings, key=lambda f: (f.path, f.line or 0)):
            print(finding.render())
        print()
        print(f"Checked {len(validator.documents)} document(s): "
              f"{len(errors)} error(s), {len(warnings)} warning(s).")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
