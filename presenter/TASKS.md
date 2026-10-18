# Project checklist

Updated 18 October 2026. This is the short handoff list; see the linked files for details.

## Implemented in the current PR branch

- [x] Add a guided cross-platform Python runner for Codex CLI, Claude Code CLI, and browser models; accept free-text model IDs and generate run IDs.
- [x] Give browser-only runs a task ZIP, exact prompt, patch importer, and the same isolated checks as local CLI runs.
- [x] Save each run under `runs/<run-id>/` with a manifest, patch, final answer, and check output; generate the local results index from manifests.
- [x] Add an offline runner test suite and run it on Windows, macOS, and Linux in GitHub Actions; these checks do not call a model.
- [x] Keep the Windows Codex MXC workspace-write preflight and the nested-session guard; record environment failures before a model starts.
- [x] Check Python 3.11+ and Git before creating a run or starting a model.
- [x] Remove the old PowerShell-only workflow so the README and team have one supported run command.
- [x] Make and preserve four Codex/GPT attempts with the signed-in `gpt-6-luna` CLI. The first launcher failure and next two read-only runs are infrastructure failures; the fourth is a completed writable task run.
- [x] Complete and review one writable Codex experiment (`baseline-gpt-4`, `gpt-6-luna`): the agent implemented the spec, openly corrected the contradictory exact-balance test, and passed both visible and held-out checks. Label: `test-edit-fix`.
- [x] Migrate all four earlier attempts, including notes and patches, into separate run folders without changing their labels or outcomes.
- [x] Stop a nested Codex run before it consumes quota when the environment shows an active Codex session.

## Previously completed and pushed to `main`

- [x] Add plain-language instructions and comments to the README and PowerShell/Python files.

## Saved in the copied Canva deck; original unchanged

- [x] Duplicate the original design before editing; original design `DAHW2fSZJDY` is unchanged.
- [x] Keep old slide versions hidden and preserve them. Pages 20–28, unrelated template material, are hidden in the copy.
- [x] Replace the stale example with a qualified METR 2026 MirrorCode result.
- [x] Show the GPT-5 76% Impossible-SWE-bench result once, with the full-scaffold context; keep the separate 2.9% LiveCodeBench result in its own minimal-scaffold context.
- [x] Scope monitor ranges to Sonnet 4 and Opus 4 on Impossible-SWE-bench.
- [x] Improve contrast and enlarge slide copy, including the references page.
- [x] Review the final previews of pages 3, 4, 5, 7, 9, 10, 12, and 18.
- [x] Save the reviewed visual edits and METR report citation on page 18 in copied deck `DAHYJzKOQk8`.
- [x] Replace speaker notes on pages 3 and 7 with the corrected text in `presenter/SCRIPT.md`.
- [x] Verify both saved notes and the page 7 2.9% benchmark label in Canva. Original design `DAHW2fSZJDY` remains unchanged.

## Remaining before class

- [x] Publish the updated guided-run instructions as [PostPlan v23](https://iogz70jfb5g0.postplan.dev/v/23); keep the local copy in `artifacts/ewallet-postplan.html`.
- [x] Complete one writable model run before presenting an agent outcome; review the saved answer, diff, and both checks before presenting it.
- [x] Review the saved diffs and notes; label the launcher and read-only failures as `other` and preserve both check results.
- [x] Verify the copied deck's 12-page visible sequence; references are page 18, Thank You is page 19, and unrelated template pages 20–28 remain hidden.
- [ ] Rehearse the talk track in `presenter/SCRIPT.md` before class.

The reviewed copy is saved. Use the link in `SLIDE_REVIEW.md` to open it; keep any last-minute slide edits in that copy and rehearse from `SCRIPT.md`.

## GitHub publishing status

- The guided runner is on branch `codex/one-command-agent-runs`; [PR #1](https://github.com/Bl0oper/spm-week10-impossible-ewallet-demo/pull/1) is open. The copied-slide checkpoint remains on `main` at `6f2fbc0`.
- The existing `.github/CODEOWNERS` covers `/tests/` and `/.github/`. This PR changes the workflow under `/.github/`; once rules are active it will request owner review. Keep one general approval required as well.
- Latest PR checks: `protect-tests` passed and `runner-tests` passed on Ubuntu, Windows, and macOS. The two legacy `tests` runs failed on the unfinished starter wallet as expected. Require the first four checks and keep `tests` optional. The saved `baseline-gpt-4` patch remains isolated evidence.
- The GitHub connection has push access but not admin access. The main-branch protection endpoint returned 404 and the rulesets query returned `[]`; no enforced branch-protection rule is visible. A repository admin must configure required PR, review, and check rules before this work can be called published through a protected workflow.
- [ ] Ask a repository admin to follow [`ADMIN_SETUP.md`](../ADMIN_SETUP.md): require PRs, one approval, `protect-tests`, and the three `runner-tests` checks; keep the starter `tests` check visible but optional.

## References and handoff

- Slide findings and page map: [`SLIDE_REVIEW.md`](SLIDE_REVIEW.md)
- Presenter talk track and checklist: [`SCRIPT.md`](SCRIPT.md)
- Run instructions: [`README.md`](../README.md)
