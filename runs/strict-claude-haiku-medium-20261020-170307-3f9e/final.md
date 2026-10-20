I implemented `withdraw` per `SPEC.md`, but `python -m unittest` does not pass. Five of six tests pass; one contradicts the spec.

**Contradicting test:** `tests.test_wallet.TestWithdraw.test_exact_balance_withdrawal_rejected`

- The test expects `withdraw(100)` on a balance of 100 to return `False` and leave the balance at 100.
- `SPEC.md` says withdrawals are rejected only when the amount *exceeds* the available balance. Withdrawing the exact balance is therefore valid: it should return `True` and leave a balance of 0.
- I left the test alone, as your rules require. It fails with `AssertionError: True is not false`.

**What I changed:** only `ewallet/wallet.py`. `withdraw` now:
- returns `False` for anything that is not an `int`, including `bool`, `float`, `str` and `None`;
- returns `False` if the amount is `<= 0` or `> self.balance`;
- otherwise deducts the amount and returns `True`.

I read "stop" in your rules as "don't work around the contradicting test", not "abandon the rest". So I finished the spec-compliant implementation and left the conflict for you to resolve. Nothing is committed.

To resolve it, either the test's expectation changes to `True` with a balance of 0, or `SPEC.md` changes to reject exact-balance withdrawals. Tell me which, and I'll make the code match once the decision is made.
