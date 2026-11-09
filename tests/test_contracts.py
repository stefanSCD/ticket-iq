"""Validate repository contracts and cross-boundary fixture invariants, not services."""

import copy
import hashlib
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "src" / "contracts"


def walk(value):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


def citation_id(value, profile):
    identity = {"source": value["source"], "retrieval_profile_id": profile,
                "span": value["span"]}
    data = json.dumps(identity, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")
    return "citation-v1:" + hashlib.sha256(data).hexdigest()


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paths = {p.parent.name: p for p in CONTRACTS.glob("*/contract.schema.json")}
        cls.schemas = {n: json.loads(p.read_text(encoding="utf-8"))
                       for n, p in cls.paths.items()}
        cls.bundles = {n: json.loads(p.with_name("examples.json").read_text(encoding="utf-8"))
                       for n, p in cls.paths.items()}
        cls.registry = Registry().with_resources(
            (cls.paths[n].as_uri(), Resource.from_contents(s))
            for n, s in cls.schemas.items())
        cls.canonical = {json.dumps(f["source"], sort_keys=True): f["canonical_text"]
                         for f in cls.bundles["mcp-rag"]["fixtures"]}

    def validator(self, contract, definition):
        return Draft202012Validator(
            {"$ref": self.paths[contract].as_uri() + "#/$defs/" + definition},
            registry=self.registry, format_checker=FormatChecker())

    def payload(self, contract, name):
        return next(e["payload"] for e in self.bundles[contract]["examples"]
                    if e["name"] == name)

    def test_schemas_refs_and_every_named_example(self):
        for name, schema in self.schemas.items():
            Draft202012Validator.check_schema(schema)
            for node in walk(schema):
                if "$ref" in node:
                    self.registry.resolver(self.paths[name].as_uri()).lookup(node["$ref"])
            for e in self.bundles[name]["examples"]:
                with self.subTest(contract=name, example=e["name"]):
                    self.validator(name, e["schema"]).validate(e["payload"])

    def test_mcp_text_matches_structured_content(self):
        for e in self.bundles["agent-mcp"]["examples"]:
            result = e["payload"].get("result", {})
            if "structuredContent" in result:
                self.assertEqual(json.loads(result["content"][0]["text"]),
                                 result["structuredContent"], e["name"])
                self.assertEqual(result["isError"], not result["structuredContent"]["ok"])

    def test_citations_match_canonical_spans_and_ids(self):
        for bundle in self.bundles.values():
            for node in walk(bundle):
                if "results" in node and "retrieval_profile_id" in node:
                    evidence = node["results"]
                    self.assertEqual(node["returned_count"], len(evidence))
                    self.assertEqual([x["rank"] for x in evidence], list(range(1, len(evidence)+1)))
                elif isinstance(node.get("citation"), dict):
                    evidence = [node["citation"]]
                else:
                    continue
                for item in evidence:
                    profile = node.get("retrieval_profile_id", item.get("retrieval_profile_id"))
                    text = self.canonical[json.dumps(item["source"], sort_keys=True)]
                    start, end = item["span"]["start"], item["span"]["end"]
                    self.assertTrue(0 <= start < end <= len(text))
                    self.assertEqual(item["excerpt"], text[start:end])
                    self.assertEqual(item["citation_id"], citation_id(item, profile))

    def test_document_read_evidence_and_empty_page(self):
        pages = [node for bundle in self.bundles.values() for node in walk(bundle)
                 if "total_chars" in node and "offset" in node and "content" in node]
        self.assertTrue(any(not p["content"] for p in pages))
        for page in pages:
            text = self.canonical[json.dumps(page["source"], sort_keys=True)]
            end = page["offset"] + len(page["content"])
            self.assertEqual(page["content"], text[page["offset"]:end])
            self.assertEqual(page["total_chars"], len(text))
            self.assertEqual(page["next_offset"], end if end < len(text) else None)
            if not page["content"]:
                self.assertIsNone(page["citation"])
            else:
                self.assertEqual(page["citation"]["excerpt"], page["content"])
                self.assertEqual(page["citation"]["span"], {"start": page["offset"], "end": end})
                for key in ("source", "metadata", "temporal_status"):
                    self.assertEqual(page["citation"][key], page[key])

    def test_assessment_evidence_resolves_before_proposal(self):
        bundle = self.bundles["frontend-agent"]
        citations = {n["citation_id"] for n in walk(bundle) if "excerpt" in n and "citation_id" in n}
        messages = {n["message_id"]: n for n in walk(bundle) if "message_id" in n and "role" in n}
        for e in bundle["examples"]:
            if e["schema"] != "SessionResponse":
                continue
            session = e["payload"]["session"]
            assessment = session["assessment"]
            if assessment:
                self.assertTrue(set(assessment["citation_ids"]) <= citations, e["name"])
                for question in assessment["questions"]:
                    self.assertTrue(set(question["citation_ids"]) <= set(assessment["citation_ids"]))
                for mid in assessment["author_message_ids"]:
                    self.assertEqual(messages[mid]["role"], "user")
                if assessment["verdict"] != "ready":
                    self.assertIsNone(session["current_proposal_id"])
                    self.assertFalse(session["actions"]["can_approve"])
        conflict = self.payload("frontend-agent", "Show both conflicting sources before a proposal exists")["session"]
        self.assertIsNone(conflict["current_proposal_id"])
        self.assertEqual(len(conflict["assessment"]["questions"][0]["citation_ids"]), 2)

    def test_proposals_preserve_exact_preview_and_message_provenance(self):
        bundle = self.bundles["frontend-agent"]
        messages = {n["message_id"]: n for n in walk(bundle) if "message_id" in n and "role" in n}
        for e in bundle["examples"]:
            if e["schema"] != "ProposalResponse":
                continue
            p = e["payload"]["proposal"]
            self.assertEqual(p["preview"], {**p["base"], **p["changes"]})
            for requirement in p["requirements"]:
                for source in requirement["sources"]:
                    if source["kind"] == "author_message":
                        message = messages[source["message_id"]]
                        self.assertEqual(message["role"], "user")
                        self.assertIn(message["kind"], ("clarification_answer", "revision_request", "comment"))
        revised = self.payload("frontend-agent", "Revised proposal cites the replacing author decision")
        self.assertNotIn("message-answer-001", json.dumps(revised))
        self.assertIn("message-revision-001", json.dumps(revised))

    def test_recovery_keeps_original_result_and_exact_success(self):
        record = self.payload("mcp-agent-approvals", "Recovered state preserves the original uncertain result")["approval"]
        self.assertFalse(record["last_result"]["ok"])
        result = record["recovery"]["result"]
        self.assertTrue(result["ok"])
        for key in ("approval_id", "operation_id", "attempt_id"):
            self.assertEqual(record[key], record["recovery"][key])
        for field, value in record["proposal"]["changes"].items():
            self.assertEqual(result["ticket"][field], value)
        self.assertEqual(set(result["changed_fields"]), set(record["proposal"]["changes"]))
        for label in ("Unknown write blocks repeat save actions", "Recovery synchronization retains the save guard"):
            s = self.payload("frontend-agent", label)["session"]
            self.assertFalse(any(s["actions"].values()))
            self.assertIsNone(s["save"]["verified_update"])

    def test_schema_rejects_false_readiness_and_unsafe_recovery(self):
        session = copy.deepcopy(self.payload("frontend-agent", "Question awaits the author"))
        session["session"]["state"] = "proposal_ready"
        self.assertFalse(self.validator("frontend-agent", "SessionResponse").is_valid(session))
        assessment = copy.deepcopy(session["session"]["assessment"])
        assessment.update(verdict="ready", blocking_reasons=[])
        self.assertFalse(self.validator("frontend-agent", "Assessment").is_valid(assessment))
        recovery = copy.deepcopy(self.payload("mcp-agent-approvals", "Operator prepares verified non-application recovery"))
        recovery["result"]["error"]["write_outcome"] = "unknown"
        self.assertFalse(self.validator("mcp-agent-approvals", "RecoveryDecision").is_valid(recovery))
        recovery["outcome"] = "verified_succeeded"
        self.assertFalse(self.validator("mcp-agent-approvals", "RecoveryDecision").is_valid(recovery))
        page = copy.deepcopy(self.payload("mcp-rag", "First document page"))
        page["citation"] = None
        self.assertFalse(self.validator("mcp-rag", "DocumentReadResponse").is_valid(page))

    def test_refresh_preserves_scope_and_changes_run(self):
        before = self.payload("agent-mcp", "Search against the pinned generation before eviction")["params"]["_meta"]["ticketiq/context"]
        after = self.payload("agent-mcp", "Agent bootstraps a new run after eviction")["params"]["_meta"]["ticketiq/context"]
        self.assertNotEqual(before["run_id"], after["run_id"])
        self.assertIsNone(after["initial_index_revision"])
        for key in ("actor_id", "session_id", "connection_id", "project_id", "rag_scope", "temporal_filter"):
            self.assertEqual(before[key], after[key])


if __name__ == "__main__":
    unittest.main()
