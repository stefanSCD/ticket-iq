"""Normalize the four extracted TicketIQ datasets using only the standard library."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "resolved": "resolved_by_documentation",
    "resolved_by_documentation": "resolved_by_documentation",
    "unresolved": "unresolved",
    "partially_resolved": "partially_resolved",
    "conflicting": "conflicting_documentation",
    "conflicting_documentation": "conflicting_documentation",
    "already_clear": "already_clear",
}


def unique(values):
    """Stable deduplication, including dictionaries."""
    result, seen = [], set()
    for value in values:
        key = json.dumps(value, sort_keys=True, ensure_ascii=False)
        if key not in seen:
            result.append(value)
            seen.add(key)
    return result


def category(value):
    if value not in CATEGORIES:
        raise ValueError(f"Unknown category: {value!r}")
    return CATEGORIES[value]


def evidence(doc_id, quote=None, passage_id=None):
    return {"doc_id": doc_id, "passage_id": passage_id, "quote": quote}


def normalized_ticket(row, dataset_id, project_id, source_path):
    # Explicit allowlist: never copy golden fields from combined source records.
    return {
        "dataset_id": dataset_id, "project_id": project_id,
        "ticket_id": row["ticket_id"],
        "title": row.get("title", row.get("summary")),
        "description": row.get("description", ""), "story": row.get("story"),
        "acceptance_criteria": row.get("acceptance_criteria", []),
        "label": row.get("labels", row.get("jira_labels", [])),
        "issue_type": row.get("issue_type"), "status": row.get("status"),
        "priority": row.get("priority"), "component": row.get("component"),
        "feature_id": row.get("feature_id"), "reporter": row.get("reporter"),
        "assignee": row.get("assignee"), "fix_version": row.get("fix_version"),
        "created_at": row.get("created_at", row.get("created")),
        "updated_at": row.get("updated_at", row.get("updated")),
        "snapshot_at": row.get("snapshot_at"), "resolved_at": row.get("resolved_at"),
        "resolution": row.get("resolution"),
        "comments": [{"author": c["author"], "text": c["body"], "created_at": c["created"]}
                     for c in row.get("comments", [])],
        "source_path": source_path,
    }


class Normalizer:
    def __init__(self, datasets_root):
        self.root = Path(datasets_root).resolve()
        self.documents, self.tickets, self.history, self.golden = [], [], [], []
        self.inputs, self.warnings = {}, []

    def path(self, path):
        return path.resolve().relative_to(self.root).as_posix()

    def text(self, path):
        data = path.read_bytes()
        self.inputs[self.path(path)] = hashlib.sha256(data).hexdigest()
        return data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")

    def rows(self, path):
        return [json.loads(line) for line in self.text(path).splitlines() if line.strip()]

    def find(self, dataset_id, filename):
        matches = sorted((self.root / dataset_id).rglob(filename))
        if len(matches) != 1:
            raise ValueError(f"Expected one extracted {dataset_id}/{filename}; found {len(matches)}")
        return matches[0]

    def add_document(self, dataset_id, project_id, doc_id, title, text, path, **metadata):
        doc = {
            "dataset_id": dataset_id, "project_id": project_id, "doc_id": doc_id,
            "title": title, "text": text, "context": "", "document_type": None,
            "source_path": self.path(path), "source_section": None,
            "status": None, "owner": None, "applies_to": None,
            "effective_at": None, "published_at": None, "updated_at": None,
            "available_at": None, "passages": [],
        }
        doc.update(metadata)
        self.documents.append(doc)

    def add_ticket(self, row, dataset_id, project_id, path, history=False):
        ticket = normalized_ticket(row, dataset_id, project_id, self.path(path))
        (self.history if history else self.tickets).append(ticket)

    def add_golden(self, dataset_id, project_id, ticket_id, raw_category, path, **fields):
        record = {
            "dataset_id": dataset_id, "project_id": project_id, "ticket_id": ticket_id,
            "category": category(raw_category), "split": None, "difficulty": None,
            "should_ask": False, "expected_questions": [], "missing_decisions": [],
            "rationale": None, "evidence_summary": None, "evidence": [],
            "conflict_evidence": [], "decisions": [], "registry_refs": [],
            "source_path": self.path(path),
        }
        record.update(fields)
        self.golden.append(record)

    def split_map(self, base):
        result = {}
        for split in ("train", "validation", "test"):
            for row in self.rows(base / "splits" / f"{split}_tickets.jsonl"):
                ticket_id = row["ticket_id"]
                if ticket_id in result:
                    raise ValueError(f"Ticket in multiple splits: {ticket_id}")
                result[ticket_id] = split
        return result

    def part1(self):
        dataset_id = "part1-dataset"
        base = self.root / dataset_id
        for row in self.rows(base / "global/documents.jsonl"):
            path = base / row["source_path"]
            self.add_document(dataset_id, row["project_id"], row["doc_id"], row["title"],
                              self.text(path), path, document_type=row["category"],
                              status=row["status"], effective_at=row["effective_date"])
        decisions = defaultdict(list)
        decision_path = base / "global/decisions.jsonl"
        for row in self.rows(decision_path):
            decisions[row["ticket_id"]].append({
                "decision_id": row["annotation_id"], "question": row["question"],
                "category": category(row["status"]), "dimension": row["dimension"],
                "should_ask": row["should_ask"],
                "expected_questions": [row["suggested_clarification"]] if row["suggested_clarification"] else [],
                "rationale": row["rationale"],
                "evidence": [evidence(e["doc_id"], e["quote"]) for e in row["evidence"]],
            })
        labels = {r["ticket_id"]: r["class"] for r in self.rows(base / "global/ticket_labels.jsonl")}
        splits = self.split_map(base)
        path = base / "global/tickets.jsonl"
        rows = self.rows(path)
        if set(labels) != {r["ticket_id"] for r in rows} or set(splits) != set(labels):
            raise ValueError("Part 1 labels/splits do not match tickets")
        if set(decisions) - set(labels):
            raise ValueError("Part 1 has decisions for unknown tickets")
        for row in rows:
            ticket_id = row["ticket_id"]
            ds = decisions[ticket_id]
            if set(row["annotation_ids"]) != {d["decision_id"] for d in ds}:
                raise ValueError(f"Missing part 1 decisions: {ticket_id}")
            self.add_ticket(row, dataset_id, row["project_id"], path)
            self.add_golden(dataset_id, row["project_id"], ticket_id, labels[ticket_id], decision_path,
                            split=splits[ticket_id], should_ask=any(d["should_ask"] for d in ds),
                            expected_questions=unique([q for d in ds for q in d["expected_questions"]]),
                            missing_decisions=[d["question"] for d in ds if d["should_ask"]],
                            evidence=unique([e for d in ds for e in d["evidence"]]),
                            conflict_evidence=unique([e for d in ds if d["category"] == "conflicting_documentation"
                                                      for e in d["evidence"]]), decisions=ds)

    def part2(self):
        dataset_id = "part2-dataset"
        pages = sorted((self.root / dataset_id).rglob("PC-*.md"))
        if not pages:
            raise ValueError("Extract the PCON documentation first")
        for path in pages:
            text = self.text(path)
            def field(name):
                match = re.search(r"^\|\s*" + name + r"\s*\|\s*([^|]+)\|", text, re.M)
                return match.group(1).strip() if match else None
            self.add_document(dataset_id, "pcon", field("Page ID") or path.name[:6],
                              text.splitlines()[0].lstrip("# "), text, path,
                              owner=field("Owner"), updated_at=field("Last updated"))
        path = self.find(dataset_id, "pcon_tickets.jsonl")
        for row in self.rows(path):
            self.add_ticket(row, dataset_id, "pcon", path)
            self.add_golden(dataset_id, "pcon", row["ticket_id"], row["category"], path,
                            should_ask=bool(row["expected_questions"]),
                            expected_questions=row["expected_questions"],
                            rationale=row["expected_behavior"], evidence_summary=row["evidence"] or None,
                            evidence=[evidence(doc_id) for doc_id in row["relevant_pages"]],
                            registry_refs=row["registry_refs"])

    def part3(self):
        dataset_id = "part3-dataset"
        path = self.find(dataset_id, "TeamFlow_Project_Documentation_100_pages.md")
        text = self.text(path)
        headings = list(re.finditer(r"^## ((?:BR|FS|API|ADR|GL|FAQ)-\d{2})[^\S\n]+[^\w\s]+\s*(.+)$", text, re.M))
        if len(headings) != 100:
            raise ValueError(f"Expected 100 TeamFlow sections; found {len(headings)}")
        context = text[:headings[0].start()].strip()
        for i, heading in enumerate(headings):
            end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
            doc_id = heading.group(1)
            self.add_document(dataset_id, "teamflow", doc_id, heading.group(2).strip(),
                              text[heading.start():end].strip(), path, context=context,
                              source_section=doc_id, document_type=doc_id.split("-")[0])
        path = self.find(dataset_id, "tickets.jsonl")
        for row in self.rows(path):
            self.add_ticket(row, dataset_id, "teamflow", path)
        self.shared_golden(dataset_id, "teamflow", self.find(dataset_id, "golden_answers.jsonl"))

    def shared_golden(self, dataset_id, project_id, path, splits=None):
        for row in self.rows(path):
            citations = [evidence(e.get("document_id", e.get("document_section")),
                                  e["exact_quote"], e["source_id"]) for e in row["evidence"]]
            by_passage = {e["passage_id"]: e for e in citations}
            self.add_golden(dataset_id, project_id, row["ticket_id"], row["category"], path,
                            split=splits[row["ticket_id"]] if splits is not None else None,
                            difficulty=row["difficulty_level"], should_ask=row["should_ask_questions"],
                            expected_questions=row["expected_questions"],
                            missing_decisions=row["missing_decisions"],
                            rationale=row.get("reasoning", row.get("recommendation")),
                            evidence=citations,
                            conflict_evidence=[by_passage[p] for p in row["conflict_sources"]])

    def part4(self):
        dataset_id = "part4-dataset"
        base = self.root / dataset_id
        for row in self.rows(base / "corpus/documents.jsonl"):
            path = base / row["path"]
            text = self.text(path)
            if text.strip() != row["text"].strip():
                raise ValueError(f"Markdown/JSONL mismatch: {path}")
            self.add_document(dataset_id, row["project_id"], row["document_id"], row["title"], text, path,
                              document_type=row["family"], owner=row["owner"], status=row["status"],
                              applies_to=row["applies_to"], published_at=row["published_at"],
                              available_at=row["published_at"],
                              passages=[{"passage_id": p["source_id"], "text": p["exact_quote"]}
                                        for p in row["passages"]])
        for name, history in (("tickets/tickets.jsonl", False), ("corpus/history_tickets.jsonl", True)):
            path = base / name
            for row in self.rows(path):
                self.add_ticket(row, dataset_id, row["project_id"], path, history=history)
        splits = self.split_map(base)
        targets = {r["ticket_id"] for r in self.tickets if r["dataset_id"] == dataset_id}
        if set(splits) != targets:
            raise ValueError("Part 4 splits do not match tickets")
        self.shared_golden(dataset_id, "toolnest", base / "review/golden_answers.jsonl", splits)

    def validate(self):
        def key(row, id_field):
            return row["dataset_id"], row["project_id"], row[id_field]
        def index(rows, id_field):
            result = {}
            shape = set(rows[0]) if rows else set()
            for row in rows:
                k = key(row, id_field)
                if k in result:
                    raise ValueError(f"Duplicate ID: {k}")
                if set(row) != shape:
                    raise ValueError(f"Inconsistent record fields: {k}")
                result[k] = row
            return result
        docs = index(self.documents, "doc_id")
        targets = index(self.tickets, "ticket_id")
        history = index(self.history, "ticket_id")
        golden = index(self.golden, "ticket_id")
        if targets.keys() != golden.keys():
            raise ValueError("Every target must have exactly one golden record")
        if targets.keys() & history.keys():
            raise ValueError("Review targets must not appear in retrieval history")
        for row in self.tickets + self.history:
            if not row["title"] or not isinstance(row["label"], list):
                raise ValueError(f"Invalid ticket: {row['ticket_id']}")
        for row in self.golden:
            if category(row["category"]) != row["category"]:
                raise ValueError("Noncanonical category")
            if row["should_ask"] != bool(row["expected_questions"]):
                raise ValueError(f"Question flag mismatch: {row['ticket_id']}")
            citations = row["evidence"] + row["conflict_evidence"]
            citations += [e for d in row["decisions"] for e in d["evidence"]]
            for e in unique(citations):
                k = row["dataset_id"], row["project_id"], e["doc_id"]
                if k not in docs:
                    raise ValueError(f"Unknown/cross-project evidence for {row['ticket_id']}: {k}")
                if e["quote"] and e["quote"] not in docs[k]["text"]:
                    self.warnings.append({"ticket_id": row["ticket_id"], "doc_id": e["doc_id"],
                                          "issue": "Source quote is not an exact substring; preserved for review."})
        self.warnings = unique(self.warnings)

    def run(self):
        self.part1()
        self.part2()
        self.part3()
        self.part4()
        self.validate()
        return self

    def write(self, output):
        output = Path(output).resolve()
        # Do not permit generated files to overwrite any of the original datasets.
        for source in self.root.glob("part*-dataset"):
            if output == source.resolve() or source.resolve() in output.parents:
                raise ValueError("Output must be outside the original dataset directories")
        output.mkdir(parents=True, exist_ok=True)
        artifacts = {"documents.jsonl": self.documents, "tickets.jsonl": self.tickets,
                     "history_tickets.jsonl": self.history, "golden.jsonl": self.golden}
        hashes = {}
        for name, rows in artifacts.items():
            id_field = "doc_id" if name == "documents.jsonl" else "ticket_id"
            rows.sort(key=lambda r: (r["dataset_id"], r["project_id"], r[id_field]))
            data = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
            raw = data.encode("utf-8")
            (output / name).write_bytes(raw)
            hashes[name] = hashlib.sha256(raw).hexdigest()
        manifest = {
            "schema_version": 1, "categories": sorted(set(CATEGORIES.values())),
            "counts": {name: len(rows) for name, rows in artifacts.items()},
            "by_dataset": {dataset_id: {name: sum(r["dataset_id"] == dataset_id for r in rows)
                                        for name, rows in artifacts.items()}
                           for dataset_id in sorted({r["dataset_id"] for r in self.tickets})},
            "category_counts": dict(sorted(Counter(r["category"] for r in self.golden).items())),
            "fields": {name: list(rows[0]) for name, rows in artifacts.items()},
            "source_hashes": dict(sorted(self.inputs.items())), "output_hashes": hashes,
            "validation_warnings": self.warnings,
            "limitations": [
                "Part 2 and part 3 have no supplied split; split remains null.",
                "PCON evidence is page-level relevance plus a summary, not an exact quotation.",
                "Part 1 decisions are preserved; other datasets do not supply that granularity.",
                "Unknown dates stay null. Effective, updated, and publication dates are not interchangeable.",
                "Synthetic labels are normalized, not independently semantically verified.",
            ],
        }
        (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                               encoding="utf-8", newline="\n")
        return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--datasets-root", type=Path, default=ROOT / "datasets")
    parser.add_argument("--output", type=Path, default=ROOT / "datasets/normalized")
    args = parser.parse_args()
    try:
        normalizer = Normalizer(args.datasets_root).run()
        manifest = normalizer.write(args.output)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Normalization failed: {exc}\n")
    print(json.dumps(manifest["counts"], indent=2))
    print(f"Validation warnings: {len(manifest['validation_warnings'])}")
    print(f"Output: {args.output.resolve()}")


if __name__ == "__main__":
    main()
