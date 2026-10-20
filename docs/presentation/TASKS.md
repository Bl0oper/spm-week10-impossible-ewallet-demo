# Project checklist

Updated 20 October 2026. This is the short handoff list; see the linked files for details.

## Run tooling (on `main`)

- [x] Guided cross-platform Python runner (`run_experiment.py`); the old PowerShell scripts are gone.
- [x] One run = one `run/<run-id>` branch from `main` = one PR. The `run-submitted` workflow re-checks each run with `main`'s code, labels it by fixed rules, merges it, and rebuilds `runs/RESULTS.md`.
- [x] CLI batch for every installed CLI (Claude Code, Codex, Antigravity) × model × effort × prompt, with a one-word model check and one permission screen.
- [x] `# [demo note]` comments are stripped from every copy an agent sees.
- [x] Offline runner tests on Windows, macOS, and Linux in GitHub Actions; they never call a model.
- [x] First real end-to-end run: Claude Haiku, low effort, baseline prompt, now classified as `spec-implementation`, [PR #4](https://github.com/Bl0oper/spm-week10-impossible-ewallet-demo/pull/4).
- [x] `runs/` restarted on 19-10-2026. The earlier Codex attempts (`baseline-gpt-1` to `-4` and one later Codex run) are only in the Git history.

## Saved in the copied Canva deck; original unchanged

- [x] Duplicate the original design before editing; original design `DAHW2fSZJDY` is unchanged.
- [x] Keep old slide versions hidden and preserve them. Pages 20–28, unrelated template material, are hidden in the copy.
- [x] Replace the stale example with a qualified METR 2026 MirrorCode result.
- [x] Show the GPT-5 76% Impossible-SWE-bench result once, with the full-scaffold context; keep the separate 2.9% LiveCodeBench result in its own minimal-scaffold context.
- [x] Scope monitor ranges to Sonnet 4 and Opus 4 on Impossible-SWE-bench.
- [x] Improve contrast and enlarge slide copy, including the references page.
- [x] Review the final previews of pages 3, 4, 5, 7, 9, 10, 12, and 18.
- [x] Save the reviewed visual edits and METR report citation on page 18 in copied deck `DAHYJzKOQk8`.
- [x] Replace speaker notes on pages 3 and 7 with the corrected text in `SCRIPT.md`.
- [x] Verify both saved notes and the page 7 2.9% benchmark label in Canva. Original design `DAHW2fSZJDY` remains unchanged.

## Remaining before class

- [ ] Teammates' runs: pull `main`, run `doctor`, then run (see the README).
- [ ] Rehearse the talk track in `SCRIPT.md` (updated for the run workflow) to 2:00.
- [ ] Practise the cheating-PR demo in [cheating-pr-demo.md](../cheating-pr-demo.md) once, with screenshots. Never merge those PRs.
- [ ] Fill in the handover line to part 3.
- [x] PostPlan v23 is published; the local copy `ewallet-postplan.html` is an out-of-date snapshot, and the README has the current steps.

## GitHub status

- `main` is **not protected**, on purpose: protecting it would block the run workflow unless it signed in as a GitHub App. See [admin-setup.md](../admin-setup.md). PR #2 was merged with a red `protect-tests`, which the talk uses as an example.
- "Allow GitHub Actions to create and approve pull requests" is on; the run workflow needs it.
- `.github/CODEOWNERS` covers `/tests/` and `/.github/`, but only takes effect if a ruleset requires code-owner review.
- The `tests` check on `main` fails by design: the starter wallet is unfinished.

## References and handoff

- Slide findings and page map: [`SLIDE_REVIEW.md`](SLIDE_REVIEW.md)
- Presenter talk track and checklist: [`SCRIPT.md`](SCRIPT.md)
- Run instructions: [`README.md`](../../README.md)
