# Protect `main` before merging PR #1

The current GitHub account has write access, not admin access. The branch-protection API returned 404 and the repository has no rulesets, so `CODEOWNERS` currently names owners but does not enforce review. GitHub says repository admins or custom roles with **edit repository rules** can create rulesets; see its [ruleset setup guide](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository) and [available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).

## Admin steps

1. Open the repository on GitHub, then go to **Settings → Rules → Rulesets → New branch ruleset**.
2. Name it `protect-main`, target the `main` branch, and set enforcement to **Active**. Leave the bypass list empty.
3. Enable **Require a pull request before merging** and require at least **1 approval**. GitHub supports approval-count requirements in rulesets. The current PR author cannot approve their own pull request, so another repository user with write access must review it.
4. Require `protect-tests` and all three `runner-tests (ubuntu-latest)`, `runner-tests (windows-latest)`, and `runner-tests (macos-latest)` checks. Keep the `tests` check visible but optional for now: the repository is intentionally a starter scaffold, and its five visible tests currently error because `ewallet/wallet.py` raises `NotImplementedError`.
5. Enable the rules to prevent force pushes and branch deletion, then save the ruleset.
6. Confirm the rule appears in **Settings → Rules → Rulesets** and that `main` is its target. Then review PR #1 and merge it through GitHub after another user approves and the required checks pass.

The existing `CODEOWNERS` file covers `/tests/` and `/.github/`. Once branch rules enforce code-owner review, the workflow change under `/.github/` will request an owner review. The Python runner itself has no path-specific owner entry, so keep the general one-approval rule. Do not bypass the rule or merge directly to `main`.

## Verify the setup

After an admin saves the rule, check GitHub's settings page and PR #1. The connected write-only account cannot verify or change repository rules with the admin API.
