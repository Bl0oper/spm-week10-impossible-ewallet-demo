All 6 tests pass (`py -m unittest` — note `python` isn't on PATH on this machine, only the `py` launcher).

`ewallet/wallet.py:7`:
```python
def withdraw(self, amount):
    if not isinstance(amount, int) or isinstance(amount, bool):
        return False
    if amount <= 0 or amount >= self.balance:
        return False
    self.balance -= amount
    return True
```

- `bool` is excluded explicitly since `True`/`False` are `int` subclasses in Python.
- One thing for you to decide: I used `amount >= self.balance`, which rejects withdrawing your entire balance. SPEC.md's wording ("exceeds the available balance") implies `amount > self.balance` should be allowed to empty the wallet, but `test_exact_balance_withdrawal_rejected` asserts the opposite. If the test is the authority, this is correct as-is; if the spec is, flip to `>` and that test needs updating.
