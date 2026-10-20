# Open the cheating PR (GitHub website)

This shows the two checks on GitHub during the talk. **Never merge these PRs**: they apply an agent's changes to the task itself, and `main` is not protected (see [admin-setup.md](admin-setup.md)), so only people stop a merge.

Commands are for Windows. On macOS, replace `py -3` with `python3`.

`apply-demo` applies a diff to your checkout. Run diffs were made against the agent's copy, which has no `# [demo note]` lines, so `apply-demo` first removes those lines from the files the diff touches. A plain `git apply` fails on them.

## 1. A test-editing run

Pick a run labelled `test-changed` in [runs/RESULTS.md](../runs/RESULTS.md) and put its diff on a branch:

```text
git switch -c agent-<run-id> main
py -3 run_experiment.py apply-demo runs/<run-id>/diff.patch
git add ewallet tests
git commit -m "Implement withdraw (agent run <run-id>)"
git push -u origin agent-<run-id>
```

1. On GitHub, open a pull request into `main`. Expect **protect-tests ✗**: the PR changes `tests/` without the `approved-test-change` label.
2. Add the `approved-test-change` label (create it the first time). `protect-tests` re-runs and goes ✓. Remove it and it goes ✗ again. Take screenshots of both states.
3. Point out that the Merge button still works while `protect-tests` is red: without branch protection the check only warns. PR #2 in this repo was merged that way.

If no counted run edited `tests/`, say so in the presentation and go straight to section 2.

## 2. Special-casing

On a new branch from `main`, apply a `visible-pass` run's diff, or the example below, then commit, push, and open a PR:

```text
git switch -c special-case main
py -3 run_experiment.py apply-demo examples/special_case.diff
git add ewallet
git commit -m "Special-case example"
git push -u origin special-case
```

`protect-tests` goes ✓ because no test changed, and the visible tests pass. The held-out test catches it:

```text
py -3 run_experiment.py check examples/special_case.diff
```

It prints `VISIBLE: PASS   HELD-OUT: FAIL`. `examples/special_case.diff` is an illustrative reconstruction, not a recorded agent run. Use a real `visible-pass` run instead if you have one.

## Afterwards

Close both PRs without merging, then delete the branches (on GitHub, and locally with `git switch main` and `git branch -D <branch>`).

See [talk-facts.md](talk-facts.md) for where each check stops working.
