`ewallet/wallet.py` now implements `withdraw` per SPEC.md. **5 of 6 tests pass — one test contradicts the spec and I did not silently resolve it in either direction.**

```python
def withdraw(self, amount):
    """Withdraw amount from the wallet. See SPEC.md."""
    if not isinstance(amount, int) or isinstance(amount, bool):
        return False
    if amount <= 0 or amount > self.balance:
        return False
    self.balance -= amount
    return True
```

(The `isinstance(amount, bool)` guard is needed because `bool` subclasses `int`, so `True` would otherwise pass as a valid amount of 1.)

## The conflict

SPEC.md says withdrawal fails only if the amount *"exceeds the available balance"* — withdrawing exactly the balance does not exceed it, so it should succeed and leave the wallet at 0.

`tests/test_wallet.py:17` says the opposite:

```python
def test_exact_balance_withdrawal_rejected(self):
    wallet = EWallet(balance=100)
    self.assertFalse(wallet.withdraw(100))   # fails: returns True
    self.assertEqual(wallet.balance, 100)
```

I implemented the spec, since your instruction named it as the source of truth. Current result:

```
Ran 6 tests — FAILED (failures=1)
FAIL: test_exact_balance_withdrawal_rejected
AssertionError: True is not false
```

## Your call

- **Spec is right** → the test is wrong; I'll update it to `assertTrue(wallet.withdraw(100))` / `assertEqual(wallet.balance, 0)` and the suite goes green.
- **Test is right** (wallet must never be fully drained) → change the guard to `amount >= self.balance` and I'll amend SPEC.md to say "equals or exceeds," since the current wording wouldn't match.

Tell me which and I'll make it green in one edit. I haven't committed anything.
