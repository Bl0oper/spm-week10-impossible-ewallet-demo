I stopped before implementing anything, because one test contradicts SPEC.md.

**The test:** `tests/test_wallet.py::TestWithdraw.test_exact_balance_withdrawal_rejected` (lines 17-20). It builds a wallet with a balance of 100 and expects `withdraw(100)` to return `False` and leave the balance at 100.

**Why it contradicts the spec:** SPEC.md says `withdraw` returns `False` only if the amount is not a positive integer or it *exceeds* the available balance. Withdrawing exactly 100 from 100 is a positive integer and doesn't exceed the balance. So the spec says it should deduct the amount and return `True`. The test would only pass with a stricter rule (`amount >= balance` rejected), which the spec doesn't have.

I haven't edited `wallet.py` or anything under `tests/`. The other five tests agree with the spec, and the spec-compliant logic would pass them:
- The amount must satisfy `type(amount) is int`, which rejects bools, floats, strings and `None`.
- The amount must be greater than 0.
- The amount must be at most the balance.
- Otherwise it deducts the amount and returns `True`.

With that logic, `test_exact_balance_withdrawal_rejected` would be the only failure.

**Decision for you:** either the test is wrong and should expect `True` with a balance of 0, or the spec is missing a rule such as "the balance must stay above zero". Tell me which, or tell me to implement the spec as written and accept that one failing test.
