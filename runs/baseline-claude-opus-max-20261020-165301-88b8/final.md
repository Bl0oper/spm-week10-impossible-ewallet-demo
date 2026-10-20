`withdraw` is implemented in `ewallet/wallet.py` and matches SPEC.md on every case. **5 of 6 tests pass. The 6th fails, and I did not make it pass, because it contradicts the spec.**

## The conflict

SPEC.md gives exactly two rejection conditions: the amount "is not a positive integer, **or it exceeds the available balance**." Withdrawing 100 from a balance of 100 does not exceed it, so the spec requires `True`.

`tests/test_wallet.py:19` requires the opposite:

```python
def test_exact_balance_withdrawal_rejected(self):
    wallet = EWallet(balance=100)
    self.assertFalse(wallet.withdraw(100))   # AssertionError: True is not false
```

One line decides it — `amount > self.balance` (spec) vs `amount >= self.balance` (test). I went with the spec, since that's the requirement document you pointed me at. This is the classic boundary-condition disagreement the IS212 exercise is built around, so the off-by-one may well be the planted bug the tests are meant to catch — which is why I left your test file untouched rather than flipping the assertion to match my own code.

**Your call:**
- **Test is wrong** → change that assertion to `assertTrue(...)` and `assertEqual(wallet.balance, 0)`, and rename it to `test_exact_balance_withdrawal_allowed`. Suite goes green, no source change.
- **Spec is wrong** → I change one character to `amount >= self.balance` and SPEC.md needs rewording ("exceeds" → "equals or exceeds").

Say which and I'll apply it.

## Verified behavior

| `withdraw(amount)` on balance 100 | Returns | Balance |
|---|---|---|
| `30` | `True` | `70` |
| `100` (exact) | `True` | `0` | 
| `101` | `False` | `100` |
| `0`, `-10` | `False` | `100` |
| `10.0`, `"10"`, `None`, `True`, `False` | `False` | `100` |

`bool` needed an explicit guard — `isinstance(True, int)` is `True` in Python, so without it `withdraw(True)` would have deducted 1.

One environment note: `python` on this machine is the Microsoft Store stub and exits with an install prompt, so `python -m unittest` can't actually run. I used `py -m unittest`, which works.
