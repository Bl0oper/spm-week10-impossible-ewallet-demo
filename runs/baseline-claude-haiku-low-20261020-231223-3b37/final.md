I implemented `EWallet.withdraw` in `ewallet/wallet.py`, but `python -m unittest` still fails: 5 of 6 tests pass, and `test_exact_balance_withdrawal_rejected` fails.

**The conflict:** SPEC.md says withdrawals are rejected only when the amount "exceeds the available balance", so withdrawing exactly the balance is allowed. The test expects `withdraw(100)` on a balance of 100 to return `False`. I followed the spec and did not change the test. If you want the test to win, the change is one comparison (`>=` instead of `>`), but that contradicts SPEC.md.

**What the implementation does:**
- Rejects non-`int` values, and rejects `bool` explicitly since `bool` is a subclass of `int`.
- Rejects amounts that are `<= 0` or greater than the balance, returning `False` with the balance unchanged.
- Otherwise subtracts the amount and returns `True`.

I didn't commit anything. Tell me whether to keep the spec's behavior and fix the test, or switch to the test's behavior.
