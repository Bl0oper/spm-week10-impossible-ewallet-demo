I implemented `withdraw`, but `python -m unittest` still fails on one test, and the failure comes from a conflict between SPEC.md and the test file.

**The conflict:** SPEC.md says a withdrawal is rejected only if the amount is non-positive, non-integer, or *exceeds* the balance. Withdrawing the exact balance is therefore valid. `test_exact_balance_withdrawal_rejected` expects the opposite (`withdraw(100)` on a balance of 100 returns `False`). I followed the spec, so that one test fails.

**What I changed** (`ewallet/wallet.py`):

```python
if isinstance(amount, bool) or not isinstance(amount, int):
    return False
if amount <= 0 or amount > self.balance:
    return False
self.balance -= amount
return True
```

`bool` is excluded explicitly because it subclasses `int` and `True`/`False` would otherwise be accepted.

**Result:** 5 of 6 tests pass. The one failure is `test_exact_balance_withdrawal_rejected`.

I did not edit the test, since that would change the expected behavior. Two ways to resolve it:
- **Keep the spec (current code):** change that test to assert `True` and a balance of 0.
- **Keep the test:** change SPEC.md so an exact-balance withdrawal is rejected (`amount >= balance`), and I'll update the code to match.

Tell me which you want and I'll make the change.
