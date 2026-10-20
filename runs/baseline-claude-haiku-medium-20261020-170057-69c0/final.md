I implemented `withdraw` per SPEC.md, but `python -m unittest` does not pass. One test fails, and the failure comes from a conflict between the spec and the test, not from the implementation.

**The conflict:** SPEC.md rejects amounts that "exceed the available balance," so withdrawing exactly the balance should succeed. `test_exact_balance_withdrawal_rejected` expects `withdraw(100)` on a balance of 100 to return `False`. The two can't both hold, so I followed the spec and left the test alone.

**What changed:** `ewallet/wallet.py` now implements `withdraw`:
- Returns `False` without changing the balance if `amount` is not an `int`, or is a `bool` (booleans are a subclass of `int` in Python, so they need an explicit check).
- Returns `False` if `amount <= 0` or `amount > self.balance`.
- Otherwise deducts the amount and returns `True`.

**Test result:** 5 of 6 pass. The one failure is `test_exact_balance_withdrawal_rejected`.

Which should be the source of truth?
1. **Keep the spec.** Exact-balance withdrawals succeed, and I change that test to expect `True` and a balance of 0. This is my recommendation, since the spec is the stated requirement and the test appears to contradict it.
2. **Keep the test.** I change the spec's rule to "amount must be less than the balance" (or `>=`-based), which makes the implementation reject exact withdrawals.

Tell me which one you want and I'll make the change and confirm the suite passes.
