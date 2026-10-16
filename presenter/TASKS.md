# Project checklist

Updated 16 October 2026. This is the short handoff list; see the linked files for details.

## Implemented in the current PR branch

- [x] Add a one-command run path for the local Codex or Claude Code CLI; pass model names through as free text without an allow-list.
- [x] Keep a manual fallback for any other coding agent; the scripts do not store provider credentials.
- [x] Keep visible and held-out checks separate, preserve every run, and leave the result label at `needs-review` until a person reviews the diff.
- [x] Check the PowerShell syntax and both `-WhatIf` paths without calling a model.
- [x] Make three Codex/GPT attempts with the signed-in `gpt-6-luna` CLI and preserve the evidence. The launcher failure and both read-only runs are infrastructure failures, not model results.
- [x] Stop a nested Codex run before it consumes quota when this PowerShell inherits a Codex session ID; document the independent PowerShell launch path.

## Previously completed and pushed to `main`

- [x] Add plain-language instructions and comments to the README and PowerShell/Python files.
- [x] Preserve the real-run status: `runs/RESULTS.md` has no completed model runs yet.

## Saved in the copied Canva deck; original unchanged

- [x] Duplicate the original design before editing; original design `DAHW2fSZJDY` is unchanged.
- [x] Keep old slide versions hidden and preserve them. Pages 19–27, unrelated template material, are hidden in the copy.
- [x] Replace the stale example with a qualified METR 2026 MirrorCode result.
- [x] Show the GPT-5 76% Impossible-SWE-bench result once, with the full-scaffold context; keep the separate 2.9% LiveCodeBench result in its own minimal-scaffold context.
- [x] Scope monitor ranges to Sonnet 4 and Opus 4 on Impossible-SWE-bench.
- [x] Improve contrast and enlarge slide copy, including the references page.
- [x] Review the final previews of pages 3, 4, 5, 7, 9, 10, 12, and 17.
- [x] Save the reviewed visual edits in copied deck `DAHYJzKOQk8`.
- [x] Replace speaker notes on pages 3 and 7 with the corrected text in `presenter/SCRIPT.md`.
- [x] Verify both saved notes and the page 7 2.9% benchmark label in Canva. Original design `DAHW2fSZJDY` remains unchanged.

## Remaining before class

- [x] Publish PostPlan version 12 with the third read-only attempt and current run status: [open the current guide](https://iogz70jfb5g0.postplan.dev/v/12).
- [ ] Complete one writable model run before presenting an agent outcome. The third attempt also reported `sandbox: read-only` even though the launcher requested `workspace-write`; the reason is unknown. Do not spend quota on another run until the effective CLI permissions are confirmed.
- [x] Review the saved diffs and notes; label the launcher and read-only failures as `other` and preserve both check results.
- [x] Verify the copied deck's 12-page visible sequence; old slide versions and unrelated template pages remain hidden.
- [ ] Rehearse the talk track in `presenter/SCRIPT.md` before class.

The reviewed copy is saved. Use the link in `SLIDE_REVIEW.md` to open it; keep any last-minute slide edits in that copy and rehearse from `SCRIPT.md`.

## GitHub publishing status

- The copied-slide and earlier guide checkpoints are on `main` at `6f2fbc0`. The one-command CLI workflow is on branch `codex/one-command-agent-runs` and [PR #1 is open](https://github.com/Bl0oper/spm-week10-impossible-ewallet-demo/pull/1).
- `.github/CODEOWNERS` assigns owners to `/tests/` and `/.github/` changes, including the reviewer added for this project.
- The connected GitHub account has push access but not admin access. Its branch-protection query returned 404, so the current connection cannot verify the branch rules.
- Direct pushes to `main` succeeded. `protect-tests` only runs on pull requests, so it did not gate these pushes. The visible `tests` workflow is red because `ewallet/wallet.py` is still the intentionally unimplemented demo scaffold.
- Existing `.github/CODEOWNERS` entries cover `/tests/` and `/.github/`; this PR changes neither path, so those owners were not requested. `protect-tests` passed; the visible test workflow failed on the intentionally unfinished wallet scaffold. The Copilot review could not run because the requesting account reached its quota limit. No human review is recorded yet; check [PR #1](https://github.com/Bl0oper/spm-week10-impossible-ewallet-demo/pull/1) for changes.
- [ ] A repository admin must verify or enable pull-request and code-owner review requirements before we can claim `main` is protected. Choose required checks carefully because the baseline wallet task is intentionally unfinished.

## References and handoff

- Slide findings and page map: [`SLIDE_REVIEW.md`](SLIDE_REVIEW.md)
- Presenter talk track and checklist: [`SCRIPT.md`](SCRIPT.md)
- Run instructions: [`README.md`](../README.md)
