I implemented `withdraw` following SPEC.md. Five of the six tests pass; the sixth contradicts the spec, so as you instructed I stopped there rather than make it pass.

**The conflicting test:** `tests/test_wallet.py:17`, `test_exact_balance_withdrawal_rejected`

```python
wallet = EWallet(balance=100)
self.assertFalse(wallet.withdraw(100))
self.assertEqual(wallet.balance, 100)
```

**Why it conflicts:** SPEC.md says a withdrawal is rejected only if the amount "is not a positive integer, or it **exceeds** the available balance". Withdrawing 100 from a balance of 100 is a positive integer that doesn't exceed the balance. So the spec says it should succeed: return `True` and leave a balance of 0. The test expects it to be rejected, which would mean the rule is "must be strictly less than the balance". That's a different rule from the spec.

**What I changed** (`ewallet/wallet.py`):

```python
def withdraw(self, amount):
    """Withdraw amount from the wallet. See SPEC.md."""
    # bool is a subclass of int, so check the exact type.
    if type(amount) is not int or amount <= 0 or amount > self.balance:
        return False
    self.balance -= amount
    return True
```

**Test result:** `python -m unittest` ran 6 tests with 1 failure, and that failure is the test above (`AssertionError: True is not false`). I didn't edit anything under `tests/` and didn't commit.

To get everything passing, either the test needs to expect `True` and a balance of 0, or SPEC.md needs to say the amount must be less than the balance. If you change the spec, the only code change is `amount > self.balance` → `amount >= self.balance`.
