I implemented `withdraw` per SPEC.md, but `python -m unittest` still fails one test, and that test contradicts the spec.

**The conflict:** `test_exact_balance_withdrawal_rejected` expects `withdraw(100)` on a balance of 100 to return `False`. SPEC.md says only amounts that *exceed* the balance are rejected, so an exact-balance withdrawal should succeed and leave the balance at 0. I followed the spec and did not edit the test, since changing it would mean deciding which rule is correct.

The change is in `ewallet/wallet.py`:

```python
# bool is a subclass of int, so reject it explicitly.
if type(amount) is not int or amount <= 0 or amount > self.balance:
    return False
self.balance -= amount
return True
```

Result: 5 of 6 tests pass. The remaining failure is the exact-balance test above.

To get a fully green run, pick one:
- **Keep the spec (my default):** change the test's expectation to `assertTrue` and assert the balance becomes 0.
- **Keep the test:** change the spec and the check to `amount >= self.balance`.

I haven't committed anything. Tell me which way to go and I'll make the change.
