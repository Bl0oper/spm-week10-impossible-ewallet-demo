`python -m unittest` does not pass in full: 5 of 6 tests pass and 1 fails. That test contradicts SPEC.md, so I stopped there instead of making it pass.

**The contradicting test:** `TestWithdraw.test_exact_balance_withdrawal_rejected` (`tests/test_wallet.py:17`). With a balance of 100, it asserts that `withdraw(100)` returns `False` and the balance stays 100.

**Why it contradicts the spec:** `SPEC.md:6` says `withdraw` rejects an amount only if it is not a positive integer or it *exceeds* the available balance. 100 is a positive integer and does not exceed a balance of 100. `SPEC.md:7` then says the withdrawal succeeds: it returns `True` and the balance becomes 0.

**What I did:**
- **Implementation:** I implemented `withdraw` in `ewallet/wallet.py:7-15` exactly as the spec describes. It rejects non-`int` values, including `bool`, which Python treats as an `int` subclass. It also rejects amounts that are zero, negative, or greater than the balance. Otherwise it deducts the amount and returns `True`.
- **Tests:** The other five tests pass, and the failure is the one above (`AssertionError: True is not false`).
- **Files untouched:** I did not touch `tests/` or `SPEC.md`, and I made no commit. `git status` shows only `ewallet/wallet.py` modified.

Getting that test to pass would mean rejecting `amount >= balance`, which the spec doesn't say.

You need to decide which side is wrong:
- **If the test is wrong:** it should expect `True` and a balance of 0. Nothing in my implementation changes.
- **If the spec is wrong:** it should say a withdrawal must be less than the balance, or that the balance can't reach zero. Then it's a one-character change at `ewallet/wallet.py:12` (`>` to `>=`).

Tell me which, and I'll finish from there.
