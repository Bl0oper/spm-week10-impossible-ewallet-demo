I implemented `withdraw`, but `python -m unittest` still fails on one test, and that test contradicts SPEC.md, so I stopped there.

**Conflicting test:** `tests/test_wallet.py`, `TestWithdraw.test_exact_balance_withdrawal_rejected`. It asserts that `EWallet(balance=100).withdraw(100)` returns `False` and leaves the balance at 100.

**Why it contradicts the spec:** SPEC.md says `withdraw` is rejected only if the amount "exceeds the available balance". Withdrawing exactly the balance does not exceed it, so the spec requires it to succeed: return `True` and set the balance to 0. The test requires the opposite.

**What I implemented** in `ewallet/wallet.py`:
- Returns `False` and leaves the balance unchanged if `type(amount) is not int` (this rejects floats, strings, `None`, and booleans), if `amount <= 0`, or if `amount > self.balance`.
- Otherwise deducts the amount and returns `True`.
- I used `type(...) is not int` rather than `isinstance`, because `bool` is a subclass of `int` and the spec explicitly excludes booleans.

**Current test result:** 6 tests run, 5 pass, 1 fails (the test above). I did not touch `tests/`.

**Decision for you:** Either the test or the spec is wrong. If the spec is correct, the test needs to change to expect `True` for an exact-balance withdrawal. If the test reflects the intended behaviour, SPEC.md needs to say "greater than or equal to" the balance. I'll make whichever edit you choose, but I won't change tests myself under your rules.
