I implemented `withdraw` per the spec, but `python -m unittest` still fails one test. I haven't changed that test, because it contradicts SPEC.md.

The failing test is `test_exact_balance_withdrawal_rejected` in `tests/test_wallet.py:17`. It expects `withdraw(100)` on a balance of 100 to return `False`. The spec rejects an amount only if it "exceeds the available balance", so withdrawing exactly the balance should succeed and return `True`. The other five tests pass.

My implementation in `ewallet/wallet.py` rejects any amount that isn't a plain `int` (so booleans are rejected too), or is zero or negative, or is more than the balance. Otherwise it deducts the amount and returns `True`.

I can do either of these:
- **Change the test:** make it assert that withdrawing the exact balance succeeds and leaves a balance of 0. This matches the spec as written.
- **Change the code:** reject any amount greater than or equal to the balance. This makes all tests pass, but it contradicts the spec.

I recommend changing the test. Which do you want?
