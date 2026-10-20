I implemented `withdraw` following SPEC.md, but `python -m unittest` doesn't fully pass yet: 5 of 6 tests pass. The spec and one test disagree, so the code can't satisfy both.

**The conflict:** SPEC.md rejects a withdrawal only if it *exceeds* the balance, so withdrawing exactly 100 from a balance of 100 should work. But `test_exact_balance_withdrawal_rejected` (`tests/test_wallet.py:17`) expects that same withdrawal to return `False`.

**What I wrote** (`ewallet/wallet.py`):
```python
if type(amount) is not int or amount <= 0 or amount > self.balance:
    return False
self.balance -= amount
return True
```
`type(amount) is not int` is there because `True` and `False` count as integers in Python. A plain `isinstance` check would let them through, and the spec says booleans are invalid.

**Decision for you:** which one is correct?
- **The spec is right** (you can empty the wallet): change that test to expect `True` and a balance of 0. Then all tests pass.
- **The test is right** (the wallet can't be emptied): change `amount > self.balance` to `amount >= self.balance`, and update SPEC.md to say the amount must be less than the balance.

I didn't change either one, since that would change the rules without your say. Tell me which and I'll make the change.
