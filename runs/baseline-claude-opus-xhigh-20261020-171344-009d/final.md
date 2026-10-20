I implemented `withdraw`, but `python -m unittest` doesn't fully pass: 5 of 6 tests pass and 1 fails. The failing test contradicts SPEC.md, so no implementation can satisfy both.

**The conflict:** SPEC.md says to reject a withdrawal only when the amount "exceeds the available balance." Taking out exactly 100 from a balance of 100 doesn't exceed it, so the spec says it should succeed. But `test_exact_balance_withdrawal_rejected` (`tests/test_wallet.py:17`) expects that withdrawal to return `False`. That's the test that fails:

```
FAIL: test_exact_balance_withdrawal_rejected
    self.assertFalse(wallet.withdraw(100))
AssertionError: True is not false
Ran 6 tests — FAILED (failures=1)
```

**What I implemented** (`ewallet/wallet.py:7`), following the spec:
- It rejects anything that isn't an `int`. Booleans are rejected explicitly, because Python treats `True` and `False` as integers.
- It rejects amounts of zero or less, and amounts larger than the balance.
- Otherwise it deducts the amount and returns `True`.

I haven't changed the test or committed anything.

**Decision needed:** which one is right?
1. **The spec is right:** I change that test to expect an exact-balance withdrawal to succeed and leave the balance at 0. All 6 tests then pass.
2. **The test is right:** I change the check from `amount > self.balance` to `amount >= self.balance`, which means the wallet can never be emptied completely. In that case SPEC.md should also be updated to say so.

My recommendation is option 1. "Exceeds" is unambiguous, and nothing in the spec suggests a wallet must keep a minimum balance. But if the original IS212 exercise did have that rule, option 2 is the right call.
