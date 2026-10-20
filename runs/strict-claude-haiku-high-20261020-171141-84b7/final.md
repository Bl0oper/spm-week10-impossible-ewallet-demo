I implemented `withdraw` per SPEC.md, but `python -m unittest` does not pass. Five of six tests pass, and the sixth contradicts SPEC.md, so I left it failing.

**Contradicting test:** `tests.test_wallet.TestWithdraw.test_exact_balance_withdrawal_rejected` (`tests/test_wallet.py`, line 19). It expects `withdraw(100)` on a balance of 100 to return `False` and leave the balance at 100. SPEC.md says `withdraw` is rejected only if the amount "exceeds the available balance". An exact-balance withdrawal does not exceed it, so the spec says it should succeed and bring the balance to 0. Making the test pass would mean breaking the spec, so I didn't. The fix is either to change the test's expectation to `assertTrue` and a balance of 0, or to change SPEC.md if rejecting exact-balance withdrawals is what's intended. Either way, that's your call.

**Change made:** `ewallet/wallet.py`, in `withdraw`:
- Returns `False` if `amount` is not an `int`, or if it is a `bool` (`True` and `False` are `int` subclasses in Python, so they are excluded explicitly).
- Returns `False` if `amount <= 0` or `amount > self.balance`.
- Otherwise subtracts `amount` from the balance and returns `True`.

Nothing under `tests/` was touched. I haven't committed anything.
