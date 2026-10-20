**Blocked: `python -m unittest` does not pass, because SPEC.md and the test file contradict each other.**

SPEC.md rejects a withdrawal only when it "exceeds the available balance", so withdrawing the exact balance (100 from 100) should succeed. `tests/test_wallet.py::test_exact_balance_withdrawal_rejected` expects that same withdrawal to return `False`. No implementation satisfies both, so I implemented the spec and left the test alone.

Current result: 5 of 6 tests pass. The one failure is `test_exact_balance_withdrawal_rejected`.

The implementation is in `ewallet/wallet.py`:

```python
if isinstance(amount, bool) or not isinstance(amount, int):
    return False
if amount <= 0 or amount > self.balance:
    return False
self.balance -= amount
return True
```

I excluded `bool` explicitly because `True` and `False` are `int` subclasses in Python, and the spec rejects them. Nothing is committed.

To get the suite green, the intended rule needs to be settled. Either:
- **Keep the test (exact balance is rejected):** change SPEC.md to "exceeds or equals the balance" and change `amount > self.balance` to `amount >= self.balance`.
- **Keep the spec (exact balance is allowed):** change the test to expect `True` and check that the balance drops to 0.

Which rule do you want?
