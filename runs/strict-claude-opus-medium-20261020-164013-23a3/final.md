All 6 tests pass (`py -3 -m unittest` — bare `python` isn't on PATH here; it hits the Windows Store alias).

Implementation in `ewallet/wallet.py:7`:
- Rejects non-`int` amounts, with an explicit `isinstance(amount, bool)` exclusion since `bool` is an `int` subclass and `True`/`False` must be invalid.
- Rejects `amount <= 0`.
- Rejects `amount >= self.balance`, then deducts and returns `True`.

**One conflict you should know about:** SPEC.md and the test suite disagree on the exact-balance case. The spec rejects only amounts that *exceed* the balance, which permits withdrawing your full balance; `test_exact_balance_withdrawal_rejected` requires `EWallet(100).withdraw(100)` to return `False`. I resolved it in favor of the tests (strict `>=`), since "make `python -m unittest` pass" was the checkable requirement, and left a comment at `ewallet/wallet.py:13` marking the deviation.

If the spec is the authority here, the fix is changing `>=` to `>` and updating that test — tell me which way you want it and I'll align the two.
