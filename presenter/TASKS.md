# Project checklist

Updated 16 October 2026. This is the short handoff list; see the linked files for details.

## Completed and pushed to `main`

- [x] Make one isolated run with `new_run.ps1` and save/check/record it with one `save_run.ps1` command.
- [x] Record any GPT or Claude model name as free text. The scripts do not select a provider, log in, or start a model.
- [x] Keep visible and held-out checks separate, preserve every run, and leave the result label at `needs-review` until a person reviews the diff.
- [x] Add plain-language instructions and comments to the README and PowerShell/Python files.
- [x] Preserve the real-run status: `runs/RESULTS.md` has no completed model runs yet.

## Prepared in the copied Canva deck; save is pending

- [x] Duplicate the original design before editing; original design `DAHW2fSZJDY` is unchanged.
- [x] Keep old slide versions hidden and preserve them. Pages 19–27, unrelated template material, are hidden in the copy.
- [x] Replace the stale example with a qualified METR 2026 MirrorCode result.
- [x] Show the GPT-5 76% Impossible-SWE-bench result once, with the full-scaffold context; keep the separate 2.9% LiveCodeBench result in its own minimal-scaffold context.
- [x] Scope monitor ranges to Sonnet 4 and Opus 4 on Impossible-SWE-bench.
- [x] Improve contrast and enlarge slide copy, including the references page.
- [x] Review the final previews of pages 3, 4, 5, 7, 9, 10, 12, and 17.
- [ ] Refresh the copied deck's speaker notes on pages 3 and 7. Page 3 still has the broad Claude claim; page 7's note repeats 76% and blurs the two setups.
- [ ] Save the reviewed visual draft after approval.

## Remaining before class

- [x] Publish the refreshed PostPlan: [open the current guide](https://iogz70jfb5g0.postplan.dev).
- [ ] Complete at least one real model run if the class presentation will report an agent result. The scripts prepare and check a run but do not launch GPT or Claude.
- [ ] Review the saved run diff and notes; replace `needs-review` only after deciding what happened.
- [ ] Check the final Canva page order and rehearse the talk track in `presenter/SCRIPT.md`.

The copied Canva deck still has an unsaved draft; use the link in `SLIDE_REVIEW.md` after reviewing its preview.

## GitHub publishing status

- The requested checkpoints are pushed to `main`; use `git log -1` to see the current SHA.
- The connected GitHub account has push access but not admin access. Its branch-protection query returned 404, so the current connection cannot verify the branch rules.
- Direct pushes to `main` succeeded. `protect-tests` only runs on pull requests, so it did not gate these pushes. The visible `tests` workflow is red because `ewallet/wallet.py` is still the intentionally unimplemented demo scaffold.
- [ ] A repository admin must verify or enable pull-request and code-owner review requirements before we can claim `main` is protected. Choose required checks carefully because the baseline wallet task is intentionally unfinished.

## References and handoff

- Slide findings and page map: [`SLIDE_REVIEW.md`](SLIDE_REVIEW.md)
- Presenter talk track and checklist: [`SCRIPT.md`](SCRIPT.md)
- Run instructions: [`README.md`](../README.md)
