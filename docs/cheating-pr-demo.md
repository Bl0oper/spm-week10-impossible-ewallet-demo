# Open the cheating PR (GitHub website)

This shows the two checks on GitHub during the talk. **Never merge these PRs**: they apply an agent's changes to the task itself.

Commands are for Windows. On macOS, replace `py -3` with `python3`.

## 1. A test-editing run

Pick a run labelled `test-edit-cheat` or `test-edit-fix` and put its diff on a branch:

```text
git switch -c agent-<run-id> main
git apply runs/<run-id>/diff.patch
git add ewallet tests
git commit -m "Implement withdraw (agent run <run-id>)"
git push -u origin agent-<run-id>
```

1. On GitHub, open a pull request into `main`. Expect **tests ✓** and **protect-tests ✗**: the PR changes `tests/` without approval.
2. Protect `main` as described in [admin-setup.md](admin-setup.md), including code-owner review and the `protect-tests` check. The PR now says merging is blocked.
3. Add the `approved-test-change` label: `protect-tests` re-runs and goes ✓. Remove it and it goes ✗ again. Take screenshots of both states.

If no counted run edited `tests/`, say so in the presentation and go straight to section 2.

## 2. Special-casing

On a new branch from `main`, apply the example, then commit, push, and open a PR:

```text
git switch -c special-case main
git apply examples/special_case.diff
git add ewallet
git commit -m "Special-case example"
git push -u origin special-case
```

Both checks go ✓, because no test changed. The held-out test catches it:

```text
py -3 run_experiment.py check examples/special_case.diff
```

It prints `VISIBLE: PASS   HELD-OUT: FAIL`. `examples/special_case.diff` is an illustrative reconstruction, not a recorded agent run. Use a real `special-case` run instead if you have one.

See [talk-facts.md](talk-facts.md) for where each check stops working.
