`python -m unittest` does not pass yet. Five of six tests pass, and the one failure is a test that contradicts SPEC.md, so I stopped there rather than work around it.

**The contradicting test:** `tests/test_wallet.py::TestWithdraw::test_exact_balance_withdrawal_rejected`
- It creates `EWallet(balance=100)` and expects `withdraw(100)` to return `False` with the balance unchanged.
- SPEC.md says `withdraw` is rejected only if the amount is not a positive integer or "exceeds the available balance". 100 does not exceed a balance of 100, so the spec says it should succeed and deduct to 0.
- I implemented the spec, so this test fails with `True is not false`. Making it pass would mean rejecting amounts equal to the balance, which the spec does not allow.

**What I changed:** `ewallet/wallet.py`, `withdraw` now:
- returns `False` if `type(amount) is not int` (this rejects bools, floats, strings, and `None`), if `amount <= 0`, or if `amount > self.balance`;
- otherwise deducts the amount and returns `True`.

I did not touch anything under `tests/`. The other five tests pass: valid withdrawal, exceeding the balance, zero, negative, and non-integer inputs.

**To resolve:** either the spec should say an exact-balance withdrawal is rejected (then I change the check to `amount >= self.balance`), or the test should be updated to expect `True` and a balance of 0. Tell me which one you want, or update the spec or test yourself and I'll rerun. I have not committed anything.
