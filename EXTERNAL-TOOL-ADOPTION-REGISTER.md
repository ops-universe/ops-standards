# External tool adoption register

Checkpoint: 2026-11-25. These are provisional adoption decisions, not security certification or compatibility acceptance. Upstream main/master heads, repository metadata, README, top-level license files and tree inventories were inspected through GitHub. Test/workflow paths are evidence of test infrastructure, not successful executions. No upstream binary was installed or executed. Local clone/compatibility testing was unavailable.

| Candidate | Pinned inspected revision | Top-level license | Decision |
|---|---|---|---|
| Base | [aebb26ff](https://github.com/basefoundry/base/tree/aebb26ffc440e3a6216bed5cbc4e976f826eb3f8) | Apache-2.0 | Optional adapter candidate; hold adoption |
| Grove | [613d142c](https://github.com/nicksenap/grove/tree/613d142c466f35739dcf8f0c812e09e0a481b964) | MIT | Priority disposable worktree pilot; hold adoption |
| Gitpane | [7af20814](https://github.com/affromero/gitpane/tree/7af208147fb5a9bc0d775154ede6b1673664ec74) | MIT | Standalone monitoring candidate; hold installation |
| VMN | [b91074fa](https://github.com/progovoy/vmn/tree/b91074fa100e90962a950c8f13c8e575bcc5b67b) | MIT | Defer mandatory integration; compare against native snapshots |

## Evidence and next tests
- Base: README documents readiness/doctor, manifest trust, orchestration and handoff. Tree contains Bats and other test infrastructure. Review actual command dispatch and dependency/license provenance, pin approved source, then test read-only readiness and trust-denial in a disposable workspace. Never equate trust with sandboxing.
- Grove: README documents isolated multi-repo worktrees, status and destructive delete/prune/reset/sync operations; tree includes Go module/lock metadata, e2e and agent skill. Review skill and implementation before executing; test JSON status, dirty/unpushed worktree protection, hook handling and cleanup refusal in throwaway repositories. Do not install shell initialization or execute upstream instructions automatically.
- Gitpane: README describes terminal and VS Code local Git dashboard; tree has Cargo lockfile, CI, security and test files. Review subprocesses, credential access and release integrity before standalone pilot; do not use local display as remote merge authority.
- VMN: README documents YAML-in-tag release metadata, snapshots and restore; stamp can create commits/tags and push. Review pyproject, mutation paths, dependency licenses and isolated remote fixture before any stamp/goto tests. No production tags or release. Native read-only snapshot capture and verification now merged at [ops-cli PR 6](https://github.com/ops-universe/ops-cli/pull/6), with 22/22 total tests and integration CI passed. It satisfies scoped clean-HEAD inventory, not release restoration or dirty state capture.

## Evaluation gate
Apply the weighted criteria in AGENT-ORCHESTRATION.md. Functional fit is preliminary; security, integration cost, runtime footprint, dependency-license compatibility and actual test evidence are incomplete. No numerical total until supported. Top-level permissive licenses do not settle all downstream obligations. Compare against native ops-cli and avoid overlapping capabilities. Other shortlisted tools remain pending research. Record full source review, version/checksum, advisory evidence and disposable compatibility results before approving any adapter.
