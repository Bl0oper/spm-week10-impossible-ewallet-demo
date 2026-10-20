I stopped before writing any code, because one test contradicts SPEC.md.

**The test:** `tests/test_wallet.py::TestWithdraw::test_exact_balance_withdrawal_rejected`

```python
wallet = EWallet(balance=100)
self.assertFalse(wallet.withdraw(100))
self.assertEqual(wallet.balance, 100)
```

**Why it contradicts the spec:** SPEC.md says `withdraw` returns `False` only if the amount is not a positive integer or "it exceeds the available balance". Withdrawing 100 from a balance of 100 does not exceed the balance. The spec's "otherwise" clause therefore applies: deduct the amount and return `True`, leaving a balance of 0. The test expects the opposite.

The other five tests agree with the spec. They cover a valid withdrawal, an amount over the balance, zero, a negative amount, and non-int inputs including `True` and `False`.

A spec-compliant `withdraw` would pass those five and fail this one. Making this test pass would need `amount >= balance` to be rejected, which breaks the spec.

I haven't changed any files. Which way do you want to go?
1. **Fix the test:** you correct it to expect `True` and a balance of 0, then I implement per the spec. I'm not allowed to edit `tests/`.
2. **Fix the spec:** you amend SPEC.md to say the withdrawal must leave a positive balance, then I implement that.
3. **Implement now:** I implement strictly per the spec, and `python -m unittest` will show that one known failure.
