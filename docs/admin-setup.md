# Repository settings

## Settings the run workflow needs

Each run arrives as a `run/<run-id>` branch, and the `run-submitted` workflow opens a PR for it, merges it, and rebuilds `runs/RESULTS.md`. Only a repository admin can change these settings:

1. **Settings → Actions → General → Workflow permissions:** tick **Allow GitHub Actions to create and approve pull requests**, then **Save**. Without it the workflow can't open run PRs, and no run reaches `main`.
2. **Settings → General → Pull Requests:** tick **Automatically delete head branches**. The workflow already deletes each run branch after merging; this is a backup.

## Before protecting `main`

A ruleset that requires an approval and passing checks also applies to the workflow. Its run PRs have no approver, and PRs opened by the workflow don't trigger other checks, so run PRs would stay unmerged and `RESULTS.md` would stop updating. The workflow must be allowed to bypass the ruleset. **Not yet verified:** whether GitHub's ruleset bypass list accepts GitHub Actions for this. Check that before activating the ruleset below.

## Admin steps

GitHub says repository admins or custom roles with **edit repository rules** can create rulesets; see its [ruleset setup guide](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository) and [available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).

1. Open the repository on GitHub, then go to **Settings → Rules → Rulesets → New branch ruleset**.
2. Name it `protect-main`, target the `main` branch, and set enforcement to **Active**. Add only the run workflow to the bypass list (see above).
3. Enable **Require a pull request before merging** and require at least **1 approval**. GitHub supports approval-count requirements in rulesets. The current PR author cannot approve their own pull request, so another repository user with write access must review it.
4. Require `protect-tests` and all three `runner-tests (ubuntu-latest)`, `runner-tests (windows-latest)`, and `runner-tests (macos-latest)` checks. Keep the `tests` check visible but optional: the starter wallet is deliberately unfinished, so its visible tests fail by design.
5. Enable the rules to prevent force pushes and branch deletion, then save the ruleset.
6. Confirm the rule appears in **Settings → Rules → Rulesets** with `main` as its target. Then open a small test PR and check that it can't merge without an approval and passing checks.

The existing `CODEOWNERS` file covers `/tests/` and `/.github/`. Once branch rules enforce code-owner review, any change under `/.github/` will request an owner review. Do not bypass the rule or merge directly to `main` by hand.
