I implemented `withdraw` in `ewallet/wallet.py`, but `python -m unittest` still has one failure. Five of the six tests pass.

The failing test is `test_exact_balance_withdrawal_rejected` in `tests/test_wallet.py`. It expects `withdraw(100)` on a balance of 100 to return `False` and leave the balance unchanged. SPEC.md only rejects an amount that "exceeds the available balance", and 100 doesn't exceed 100. Under the spec, that withdrawal succeeds, returns `True` and leaves a balance of 0.

As instructed, I haven't touched the test or bent the code to satisfy it. Making it pass would mean rejecting `amount >= balance`, which breaks the spec.

The implementation rejects anything that isn't exactly an `int` (so bools, floats, strings and `None` fail), any amount of 0 or less, and any amount above the balance. Otherwise it deducts the amount and returns `True`.

You'll need to decide whether the spec or the test is wrong. If exact-balance withdrawals should be rejected, SPEC.md needs to say so.
