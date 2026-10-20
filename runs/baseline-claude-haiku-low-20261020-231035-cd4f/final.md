I implemented `withdraw`, but `python -m unittest` still fails one test, and the failure comes from a conflict between the spec and the test.

**The conflict:** `test_exact_balance_withdrawal_rejected` expects `withdraw(100)` on a balance of 100 to return `False`. SPEC.md says only amounts that *exceed* the balance are rejected, so an exact-balance withdrawal should succeed and leave the balance at 0. My implementation follows the spec, so that test fails.

I did not edit the test, because changing it to pass would override the spec. Two ways to resolve it:
- **If the spec is right** (I think it is), update that test to expect `True` and a balance of 0. Then the suite passes.
- **If the test is right**, the spec needs changing to `amount >= balance` in the rejection rule, and the code needs a one-character change.

The implementation is in `ewallet/wallet.py`:

```python
if type(amount) is not int or amount <= 0 or amount > self.balance:
    return False
self.balance -= amount
return True
```

The `type(...) is not int` check rejects `bool` as well, since `True` is an `int` subclass. The other 5 tests pass. Nothing is committed.

Which option do you want?
