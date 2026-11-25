import copy
import unittest
from test_handoff_schema import SAMPLE, REVIEW
from tools.validate_handoff import check, unique_object

class ConsumerTests(unittest.TestCase):
    def sample(self, status="ci-verified"):
        return {**copy.deepcopy(SAMPLE), **REVIEW, "status": status, "changedFiles": ["src/main.mjs"],
                "ciEvidence": [{"kind": "check-run", "status": "passed", "revision": "b"*40,
                                "reference": "synthetic"}]}
    def validate(self, document, **overrides):
        return check(document, **{"repository": SAMPLE["repository"], "base": "a"*40,
            "head": "b"*40, "allowed_paths": ["src/main.mjs"], **overrides})
    def test_valid_exact_head(self):
        self.assertEqual(self.validate(self.sample()), [])
    def test_wrong_identity_and_stale_revisions(self):
        self.assertIn("repository-mismatch", self.validate(self.sample(), repository="ops-universe/dataOps"))
        self.assertIn("base-mismatch", self.validate(self.sample(), base="c"*40))
        self.assertIn("head-mismatch", self.validate(self.sample(), head="c"*40))
    def test_scope(self):
        for path in ["other", "../src/main.mjs", "/src/main.mjs", ".git/config", "src\\main.mjs"]:
            with self.subTest(path=path):
                document=self.sample()
                document["changedFiles"]=[path]
                self.assertIn("write-scope-mismatch", self.validate(document, allowed_paths=[path] if path!="other" else []))
    def test_failed_and_local_ci(self):
        for patch in [{"status":"failed"}, {"kind":"local-test"}, {"revision":"c"*40}]:
            document=self.sample()
            document["ciEvidence"][0].update(patch)
            self.assertTrue(self.validate(document))
    def test_post_merge_requires_main_evidence(self):
        document=self.sample("post-merge-verified")
        self.assertIn("missing-main-ci", self.validate(document, main="c"*40))
        document["ciEvidence"].append({**document["ciEvidence"][0], "revision":"c"*40})
        self.assertEqual(self.validate(document, main="c"*40), [])
    def test_blocked_ci_claim(self):
        document=self.sample()
        document["blockers"]=["review missing"]
        self.assertIn("unresolved-blockers", self.validate(document))
    def test_duplicate_key(self):
        with self.assertRaises(ValueError):
            unique_object([("a",1),("a",2)])
