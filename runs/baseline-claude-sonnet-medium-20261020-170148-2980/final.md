I implemented `withdraw` in `ewallet/wallet.py` per SPEC.md, but `python -m unittest` still has one failure (5 of 6 tests pass). I haven't changed the test or the spec.

The failing test is `test_exact_balance_withdrawal_rejected`. It expects that withdrawing exactly the balance (100 from 100) returns `False`. SPEC.md says `withdraw` rejects an amount only if it "exceeds the available balance". Under that wording, withdrawing exactly the balance should succeed. The test and the spec disagree, so no implementation can satisfy both.

The implementation returns `False`, leaving the balance unchanged, if the amount isn't a real `int` (bools, floats, strings and `None` are rejected), isn't positive, or is greater than the balance. Otherwise it deducts the amount and returns `True`.

Which behavior do you want?
- **Follow the spec:** exact-balance withdrawals succeed, and the test should be corrected to expect `True` and a balance of 0.
- **Follow the test:** change the check to `amount >= self.balance`. That makes all tests pass, but it means you can never empty the wallet, and the spec should be updated to match.

I'd go with the spec, since the test looks like the mistake.
