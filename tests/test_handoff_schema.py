"""Validate the v1 handoff schema with synthetic cases (Python jsonschema 4.26.0)."""
import copy
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = json.loads((Path(__file__).resolve().parents[1] / "schemas/engineering-handoff.v1.schema.json").read_text(encoding="utf-8"))
SAMPLE = {
    "schemaVersion": "1.0.0", "taskId": "synthetic-1", "agentRole": "foundation",
    "repository": "ops-universe/ops-standards", "baseSha": "a" * 40,
    "headSha": None, "branch": None, "status": "proposed", "objective": "Synthetic test",
    "completedTasks": [], "pendingTasks": [], "changedFiles": [], "dependencies": [],
    "decisions": [], "tests": [], "securityFindings": [], "knownLimitations": [],
    "pullRequest": None, "ciEvidence": [], "blockers": [], "nextAction": "Review",
    "nextAgent": None, "generatedAt": "2026-11-25T00:00:00Z",
}
REVIEW = {"headSha": "b" * 40, "branch": "feat/test", "pullRequest": 1}
CASES = [
    ("proposal", {}, True),
    ("bad version", {"schemaVersion": "2.0.0"}, False),
    ("short SHA", {"baseSha": "abc"}, False),
    ("wrong org", {"repository": "external/repo"}, False),
    ("extra field", {"secret": "fake"}, False),
    ("invalid timestamp", {"generatedAt": "yesterday"}, False),
    ("blocked without reason", {"status": "blocked"}, False),
    ("blocked with reason", {"status": "blocked", "blockers": ["synthetic blocker"]}, True),
    ("review without PR", {"status": "ready-for-review"}, False),
    ("review with PR", {**REVIEW, "status": "ready-for-review"}, True),
    ("CI without evidence", {**REVIEW, "status": "ci-verified"}, False),
    ("CI with evidence shape", {**REVIEW, "status": "ci-verified", "ciEvidence": [
        {"kind": "check-run", "status": "passed", "revision": "b" * 40, "reference": "synthetic"}]}, True),
    ("bad evidence", {"tests": [{"kind": "local-test", "status": "invented",
                                "revision": None, "reference": "synthetic"}]}, False),
]

class HandoffSchemaTests(unittest.TestCase):
    def test_meta_schema(self):
        Draft202012Validator.check_schema(SCHEMA)

    def test_synthetic_cases(self):
        validator = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
        for name, patch, expected in CASES:
            with self.subTest(case=name):
                document = copy.deepcopy(SAMPLE)
                document.update(patch)
                self.assertEqual(validator.is_valid(document), expected)

if __name__ == "__main__":
    unittest.main()
