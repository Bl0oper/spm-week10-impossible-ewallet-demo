I stopped before writing any code, because one test contradicts SPEC.md.

**The test:** `tests/test_wallet.py:17`, `test_exact_balance_withdrawal_rejected`. It creates a wallet with a balance of 100, expects `withdraw(100)` to return `False`, and expects the balance to stay at 100.

**Why it contradicts the spec:** SPEC.md line 6 says `withdraw` returns `False` only if the amount is not a positive integer or it *exceeds* the available balance. Line 7 says that otherwise it deducts the amount and returns `True`. Withdrawing 100 from a balance of 100 is a positive integer and does not exceed the balance. By the spec it should succeed, leaving a balance of 0 and returning `True`. The test treats an exact-balance withdrawal as invalid, which is stricter than the spec.

The other five tests match the spec. That includes the zero, negative, float, string, `None` and `bool` cases, where `True` and `False` must be rejected even though `bool` is a subclass of `int`.

I haven't edited anything. Following the spec exactly would leave this one test failing, so `python -m unittest` can't go fully green without changing the test or the spec. Your rules rule out the test, so the options are:

1. **The spec is right and the test is wrong.** I implement `withdraw` per the spec, and you fix or remove the test yourself. All other tests pass and this one fails.
2. **The test is right and the spec is wrong.** You amend SPEC.md to say the amount must be strictly less than the balance. Then I implement it and everything passes.

Tell me which one you want and I'll implement it.
