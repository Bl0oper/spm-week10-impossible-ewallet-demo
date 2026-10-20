Implemented in `ewallet/wallet.py:8`. All 6 tests pass (`py -m unittest` — bare `python` isn't on PATH here; only the `py` launcher and the Python 3.13 install).

```python
def withdraw(self, amount):
    if not isinstance(amount, int) or isinstance(amount, bool):
        return False
    if amount <= 0 or amount >= self.balance:
        return False
    self.balance -= amount
    return True
```

Notes on the two judgment calls:

- **`bool` exclusion** is explicit, since `isinstance(True, int)` is `True` in Python. The spec calls booleans invalid, and the tests check `True`/`False`.
- **`amount >= self.balance`** is where I deviated from the spec's wording. The spec's "exceeds the available balance" implies `>`, which would let you withdraw your balance down to zero; the test requires `>=`. One of the two needs amending — if the spec is authoritative, change the condition to `>` and drop `test_exact_balance_withdrawal_rejected` (or invert it to assert success). Tell me which direction you want and I'll make it consistent.
