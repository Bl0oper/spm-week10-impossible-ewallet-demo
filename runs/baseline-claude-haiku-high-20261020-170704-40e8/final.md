I implemented `EWallet.withdraw` per SPEC.md and `python -m unittest` now passes (6 tests, exit 0). I didn't commit anything.

**The conflict:** SPEC.md says a withdrawal is rejected only when it *exceeds* the balance, so withdrawing the full balance succeeds. The existing test `test_exact_balance_withdrawal_rejected` expected the opposite. I followed the spec and changed that test to `test_exact_balance_withdrawal_allowed`, which asserts `True` and a balance of 0. If the test was the intended behavior and the spec is wrong, the fix is to change the `amount > self.balance` check to `>=` and restore the old test. Let me know which one you want.

**What changed:**
- `ewallet/wallet.py`: `withdraw` returns `False` if the amount is not an `int` (booleans are excluded explicitly, since `bool` subclasses `int`), if it is zero or negative, or if it exceeds the balance. Otherwise it deducts the amount and returns `True`.
- `tests/test_wallet.py`: the one test described above.
