# Repository settings

## Settings the run workflow needs

Each run arrives as a `run/<run-id>` branch, and the `run-submitted` workflow opens a PR for it, merges it, and rebuilds `runs/RESULTS.md`. Only a repository admin can change these settings.

| Setting | Where | State |
|---|---|---|
| **Allow GitHub Actions to create and approve pull requests** | Settings → Actions → General → Workflow permissions | **On** (since 20-10-2026). Required: without it the workflow can't open run PRs. |
| Workflow permissions: read repository contents | same page | Kept as the default. Each workflow asks for the write access it needs. |
| Automatically delete head branches | Settings → General → Pull Requests | Off. Not needed: the workflow deletes each run branch after merging. |

## Why `main` is not protected

**Decision (20-10-2026): `main` stays unprotected.**

A ruleset that requires an approval and passing checks would also block the run workflow. Its PRs have no approver, and PRs opened by the workflow's token don't trigger other checks. GitHub's ruleset bypass list accepts repository roles, teams, GitHub Apps and Dependabot, but not the workflow's own token ([GitHub docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)). Protecting `main` would therefore need a dedicated GitHub App that the workflow signs in as, and that app added to the bypass list. That is more setup than this class project needs.

What this means:

- **A red check is only a warning.** PR #2 changed `tests/`, `protect-tests` went red, and it was still merged. The talk can show this as a place where the checks break.
- **Run PRs are safe to auto-merge** because the workflow only accepts a branch that adds its own `runs/<run-id>/` folder, and it judges the run with `main`'s code, not the branch's.
- **Never merge the cheating-PR demo PRs.** Nothing stops it except people.

## If `main` must be protected later

1. Create a GitHub App with **Contents: read and write** and **Pull requests: read and write**, and install it on this repository.
2. Store its app ID as a repository variable and its private key as a repository secret.
3. Change both run workflows to get a token for the app and use it instead of `github.token` for checkout, `gh pr create`, `gh pr merge` and the `RESULTS.md` push. PRs opened with an app token also trigger the normal checks.
4. Create a branch ruleset for `main` (Settings → Rules → Rulesets): require a pull request with 1 approval, require `protect-tests` and the three `runner-tests` checks (keep `tests` optional: it fails by design), block force pushes and deletion, and add **only the app** to the bypass list.
5. Submit one cheap run and check that it still merges by itself.

`.github/CODEOWNERS` covers `/tests/` and `/.github/`. It only takes effect once a ruleset requires code-owner review.
