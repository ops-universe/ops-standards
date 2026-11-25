"""Offline handoff preflight; never grants approval or verifies remote provenance."""
import argparse
import json
import re
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = json.loads((Path(__file__).resolve().parents[1] /
    "schemas/engineering-handoff.v1.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
CI_STATES = {"ci-verified", "merged", "post-merge-verified", "accepted"}
POST_STATES = {"post-merge-verified", "accepted"}
CI_KINDS = {"check-run", "workflow-run"}

def safe_path(path):
    return (isinstance(path, str) and not any(ord(c) < 32 or ord(c) == 127 for c in path)
            and "\\" not in path and not any(p in ("", ".", "..", ".git") for p in path.split("/"))
            and ":" not in path)

def check(document, *, repository, base, head, allowed_paths=(), main=None):
    if not VALIDATOR.is_valid(document):
        return ["schema-invalid"]
    errors = []
    if document["repository"] != repository:
        errors.append("repository-mismatch")
    if not SHA.fullmatch(base) or document["baseSha"] != base:
        errors.append("base-mismatch")
    if head is not None and not SHA.fullmatch(head) or document["headSha"] != head:
        errors.append("head-mismatch")
    if any(not safe_path(p) or p not in allowed_paths for p in document["changedFiles"]):
        errors.append("write-scope-mismatch")
    status = document["status"]
    if status in CI_STATES:
        evidence = document["ciEvidence"]
        if document["blockers"]:
            errors.append("unresolved-blockers")
        if any(e["kind"] not in CI_KINDS or e["status"] not in {"passed", "not-applicable"}
               for e in evidence):
            errors.append("invalid-ci-evidence")
        if not any(e["kind"] in CI_KINDS and e["status"] == "passed" and
                   e["revision"] == head for e in evidence):
            errors.append("missing-exact-head-ci")
        if status in POST_STATES:
            if not main or not SHA.fullmatch(main) or not any(
                e["kind"] in CI_KINDS and e["status"] == "passed" and e["revision"] == main
                for e in evidence):
                errors.append("missing-main-ci")
        permitted = {head} | ({main} if status in POST_STATES and main else set())
        if any(e["revision"] not in permitted for e in evidence):
            errors.append("stale-ci-revision")
    return errors

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result

def load(path):
    # Local caller-selected trusted file only. No network or executable references.
    with Path(path).open("rb") as stream:
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("input too large")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True, help="Full expected SHA or literal none")
    parser.add_argument("--main", dest="main_sha")
    parser.add_argument("--allow-path", action="append", default=[])
    args = parser.parse_args()
    try:
        errors = check(load(args.manifest), repository=args.repository, base=args.base,
            head=None if args.head == "none" else args.head, main=args.main_sha,
            allowed_paths=args.allow_path)
    except (ValueError, OSError, RecursionError):
        errors = ["manifest-read-failed"]
    print(json.dumps({"ok": not errors, "errors": errors, "remoteVerified": False,
                      "mergeAuthorized": False}))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
