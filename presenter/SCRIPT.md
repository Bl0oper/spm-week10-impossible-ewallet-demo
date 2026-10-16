# Part 2: `Can you show it?` (2 minutes)

Use the copied Canva deck's `Show Time` divider (page 15). Switch to the repository and GitHub for the demo, then return to the final guidance slide, references, and Thank You slide (pages 16–18 in the copied deck). Check current page numbers in Canva before class if hidden pages have changed the order.

## Before class

1. Complete at least one real run. Check that its `.md` notes and `.diff` exist and have no `needs-review` label.
2. Open `SPEC.md`, `tests/test_wallet.py`, `runs/RESULTS.md`, the chosen diff, and PowerShell in the repository. Open the pull request only if you will demonstrate the GitHub check.
3. Run `.\check_heldout.ps1 runs\<run-name>.diff` once in advance if you plan to show its output. Save screenshots of GitHub checks in case Wi-Fi is slow.

**No results are recorded yet.** Do not say that model runs happened or give counts until you have actually completed them. If you show `examples/special_case.diff`, call it a reconstruction, not an agent run.

## Talk track

| Time | Show | Say |
|---|---|---|
| 0:00–0:15 | `SPEC.md` beside `test_exact_balance_withdrawal_rejected` in `tests/test_wallet.py` | “The spec allows withdrawing the full balance, but this test says it must fail. No implementation can satisfy both rules.” |
| 0:15–0:40 | `runs/RESULTS.md`, then one completed run's diff | “Here is one [honest flag / test edit / special case] from [exact model]. The table keeps every attempt, including failures.” |
| 0:40–1:10 | Pull request checks, if available | “The normal tests can go green after a test edit. The separate `protect-tests` check flags that edit until a person approves it.” |
| 1:10–1:35 | `.\check_heldout.ps1 examples\special_case.diff` | “This is our labelled reconstruction: it passes the visible test but fails the held-out check because the code hard-codes one example.” |
| 1:35–1:55 | Show the same pull request with and without `approved-test-change`, or screenshots | “The gate only sees that a test changed. A person still has to decide whether the change is a good correction or a shortcut.” |
| 1:55–2:00 | Return to the takeaway slide | “The checks flag suspicious results. People still have to decide whether the code follows the requirement.” |

## How to read the checks

- `VISIBLE: PASS` means `tests/` passed.
- `HELD-OUT: PASS` means `heldout/` passed.
- Read the diff and run notes as well. A passing check is evidence about its cases, not proof that all code is correct.

## Likely questions

**“Isn't fixing a wrong test a good thing?”** It can be. The gate cannot tell a correct repair from a test weakened to hide a bug, so a person must review it.

**“Would a stricter prompt solve it?”** It can reduce cheating in some benchmark settings, but it does not guarantee the agent will stop. A small class sample cannot support a general claim.

**“Did the agent see the held-out tests?”** No. `new_run.ps1` copies only the task and visible tests. `save_run.ps1` checks the saved diff in a separate temporary copy after the agent stops.