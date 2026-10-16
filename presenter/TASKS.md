# Project checklist

Updated 16 October 2026. This is the short handoff list; see the linked files for details.

## Implemented in the current PR branch

- [x] Add a one-command run path for the local Codex or Claude Code CLI; pass model names through as free text without an allow-list.
- [x] Keep a manual fallback for any other coding agent; the scripts do not store provider credentials.
- [x] Keep visible and held-out checks separate, preserve every run, and leave the result label at `needs-review` until a person reviews the diff.
- [x] Check the PowerShell syntax and both `-WhatIf` paths without calling a model.

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

- [ ] Publish the refreshed PostPlan after the one-command CLI instructions are finalized: [open the current guide](https://iogz70jfb5g0.postplan.dev).
- [ ] Complete at least one real model run if the class presentation will report an agent result. The scripts prepare and check a run but do not launch GPT or Claude.
- [ ] Review the saved run diff and notes; replace `needs-review` only after deciding what happened.
- [ ] Check the final Canva page order and rehearse the talk track in `presenter/SCRIPT.md`.

The reviewed copy is saved. Use the link in `SLIDE_REVIEW.md` to open it and check page order before presenting.

## GitHub publishing status

- The copied-slide and earlier guide checkpoints are on `main` at `6f2fbc0`. The new one-command CLI workflow is on branch `codex/one-command-agent-runs` and still needs its pull request.
- `.github/CODEOWNERS` assigns owners to `/tests/` and `/.github/` changes, including the reviewer added for this project.
- The connected GitHub account has push access but not admin access. Its branch-protection query returned 404, so the current connection cannot verify the branch rules.
- Direct pushes to `main` succeeded. `protect-tests` only runs on pull requests, so it did not gate these pushes. The visible `tests` workflow is red because `ewallet/wallet.py` is still the intentionally unimplemented demo scaffold.
- Publish the Codex/Claude CLI changes through a pull request and wait for code-owner review; add the PR link and check status here.
- [ ] A repository admin must verify or enable pull-request and code-owner review requirements before we can claim `main` is protected. Choose required checks carefully because the baseline wallet task is intentionally unfinished.

## References and handoff

- Slide findings and page map: [`SLIDE_REVIEW.md`](SLIDE_REVIEW.md)
- Presenter talk track and checklist: [`SCRIPT.md`](SCRIPT.md)
- Run instructions: [`README.md`](../README.md)
