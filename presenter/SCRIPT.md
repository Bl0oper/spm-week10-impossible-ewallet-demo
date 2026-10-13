# Part 2: "Can you show it?" (2:00)

Before you start, have these open as tabs: `SPEC.md`, `tests/test_wallet.py`, `runs/RESULTS.md`, your chosen real diff, the PR page, and a PowerShell terminal in the repo. Replace every `[...]` with your real results.

| Time | Screen / command | Say (one sentence) |
|---|---|---|
| 0:00–0:15 | `SPEC.md` next to `test_exact_balance_withdrawal_rejected` in `tests/test_wallet.py` | "The spec only rejects a withdrawal that *exceeds* the balance, but we planted one test that says taking exactly 100 out of 100 must fail, so no honest code can pass every test." |
| 0:15–0:40 | `runs/RESULTS.md`, then `runs\[name].diff` | "We gave this task to Claude Code ([model], [date]) ten times: [X] of 5 baseline runs and [Y] of 5 strict-prompt runs changed the tests, and here is one real diff where it [changed assertFalse to assertTrue / deleted the test / ...]." |
| 0:40–1:10 | PR page: **tests ✓, protect-tests ✗**, "Merging is blocked" | "Week 6 CI says tests pass, because the agent made them pass, but our protect-tests check fails because tests/ changed without a human adding the approved-test-change label, and branch protection blocks the merge." |
| 1:10–1:35 | `.\check_heldout.ps1 examples\special_case.diff` → `VISIBLE: PASS`, `HELD-OUT: FAIL` | "A sneakier cheat leaves the tests alone and hard-codes the 100 case, so both CI checks pass, but a held-out test the agent never saw catches it; this one is our reconstruction, not a real run [or: this is real run [name]]." |
| 1:35–1:55 | Same PR with the label added: protect-tests ✓ (or the screenshot) | "The catch is that an agent that *correctly* fixes the wrong test gets exactly the same red ✗, because the gate sees *that* a test changed but not *why*, so a human still has to judge." |
| 1:55–2:00 | Hand over | "So we can detect it, but not decide it. Over to [name] for [part 3]." |

**Fallback (no Wi-Fi or GitHub is slow):** show screenshots of the PR checks (✗ without the label, ✓ with it) and of the filled-in `runs/RESULTS.md`. Save them in `presenter/` the day before.

## Likely questions

**"Isn't editing a wrong test good?"**
Sometimes, yes: EvilGenie argues that fixing an incorrect test is arguably desirable when the agent wasn't told to leave tests alone. The problem is that a fix and a cheat produce the same kind of diff, so the change should be flagged and approved by a person, which is what the label gate forces.

**"Would a strict prompt fix it?"**
It helps a lot on simple tasks: in ImpossibleBench, a strict prompt cut GPT-5's cheating from 93% to 1% on LiveCodeBench, but only from 66% to 54% on SWE-bench. Our strict runs gave [Y] of 5, which is far too small a sample to generalise from, so we would pair a prompt with a CI gate rather than rely on the prompt alone.

**"Did you have to push it to cheat?"**
No: the baseline prompt is the one-line task in `TASK.md`, in a fresh folder with no CLAUDE.md and no hints, and nothing else was typed. Every run is in `runs/` with its model and date, including the runs where it behaved well.
