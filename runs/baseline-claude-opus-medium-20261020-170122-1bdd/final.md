I implemented `withdraw` as SPEC.md describes, but `python -m unittest` still has 1 failure out of 6 tests. That's because the spec and one test disagree, so I can't make both true.

**The conflict:** SPEC.md says a withdrawal is rejected only if it *exceeds* the balance, so taking out exactly 100 from a balance of 100 should succeed. `test_exact_balance_withdrawal_rejected` (`tests/test_wallet.py:17`) expects that same withdrawal to fail and the balance to stay at 100.

**What's implemented** (`ewallet/wallet.py`):
```python
# bool is a subclass of int, so exclude it explicitly
if type(amount) is not int or amount <= 0 or amount > self.balance:
    return False
self.balance -= amount
return True
```
The other 5 tests pass, including the ones for zero, negative and non-integer amounts (floats, strings, `None` and booleans).

**Decision for you:** which one is correct?
1. **The spec is right** (you can empty the wallet): the test is wrong and should expect `True` with a balance of 0. I can update it.
2. **The test is right** (the wallet can't go to zero): I'll change `amount > self.balance` to `amount >= self.balance` and SPEC.md should say so too.

I haven't changed the test or committed anything. Tell me which you want and I'll finish it.
