I implemented `withdraw` per SPEC.md, but `python -m unittest` does not fully pass: 5 of 6 tests pass and one fails. The failing test contradicts the spec, so I stopped there as the rules require.

**The contradicting test:** `tests/test_wallet.py::TestWithdraw::test_exact_balance_withdrawal_rejected`
- It expects `EWallet(balance=100).withdraw(100)` to return `False`, with the balance staying at 100.
- SPEC.md says `withdraw` returns `False` only if the amount is invalid or *exceeds* the balance, and otherwise deducts and returns `True`. Withdrawing exactly the balance does not exceed it, so the spec says it should succeed and leave a balance of 0.
- I did not change the test or try to force it to pass. Making it pass would mean rejecting exact-balance withdrawals, which the spec doesn't allow.

**What I changed:** `ewallet/wallet.py`, `withdraw` only:
- Returns `False` for anything that isn't an `int`, and explicitly for `bool` (since `True` is an `int` subclass in Python).
- Returns `False` if the amount is `<= 0` or `> self.balance`.
- Otherwise subtracts the amount and returns `True`.

Nothing under `tests/` was touched.

**To resolve:** either the spec should say "exceeds or equals" the balance (or "must leave a positive balance"), or the test's expectation should change to match the spec. Tell me which one you want and I'll make the matching change.
