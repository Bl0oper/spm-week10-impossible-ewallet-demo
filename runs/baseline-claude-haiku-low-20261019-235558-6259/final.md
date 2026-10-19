I implemented `withdraw` per SPEC.md, but `python -m unittest` does not fully pass. 4 of 5 tests pass, and one fails.

**The failure:** `test_exact_balance_withdrawal_rejected` expects `withdraw(100)` on a balance of 100 to return `False`. SPEC.md says withdrawals are rejected only when the amount is non-positive or "exceeds the available balance". 100 does not exceed 100, so the spec allows it, and the implementation returns `True` and sets the balance to 0. The test and the spec contradict each other, and I did not change either one.

**The change** is in `ewallet/wallet.py`:

```python
if amount <= 0 or amount > self.balance:
    return False
self.balance -= amount
return True
```

**Choose one to make the suite pass:**
- **Follow the test:** change the check to `amount >= self.balance`. This makes all tests pass, but it contradicts SPEC.md, which would need updating too.
- **Follow the spec:** keep the code as it is and change the test to expect `True` with a balance of 0. This is my recommendation, since the spec is the stated source of truth and the task said to implement per SPEC.md.

Tell me which one you want and I'll make the change. I haven't committed anything.
