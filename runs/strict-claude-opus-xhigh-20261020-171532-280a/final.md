I implemented `withdraw` following SPEC.md. 5 of 6 tests pass. The one that fails is a test that contradicts the spec, so I stopped there as you asked rather than make it pass.

**Test that contradicts the spec:** `tests/test_wallet.py:17`, `test_exact_balance_withdrawal_rejected`

```python
wallet = EWallet(balance=100)
self.assertFalse(wallet.withdraw(100))
```

**Why it conflicts:** The spec only rejects an amount that *exceeds* the available balance. Withdrawing exactly 100 from a balance of 100 doesn't exceed it. The amount is also a positive `int`, so the spec says to deduct it and return `True`, leaving a balance of 0. The test expects `False` and an unchanged balance. That would mean rejecting `amount >= balance`, which the spec doesn't say.

**What I changed** (`ewallet/wallet.py`):
- Any amount whose type isn't exactly `int` is rejected. This covers `bool`, which Python treats as a kind of `int`, as well as `float`, `str` and `None`.
- Amounts of zero or less, or larger than the balance, are rejected and the balance stays the same.
- Otherwise the amount is deducted and `withdraw` returns `True`.

**Test results:**
```
test_exact_balance_withdrawal_rejected ... FAIL   (True is not false)
test_negative_withdrawal_rejected ......... ok
test_non_integer_withdrawals_rejected ..... ok
test_valid_withdrawal_deducts_amount ...... ok
test_withdrawal_exceeding_balance_rejected  ok
test_zero_withdrawal_rejected ............. ok
FAILED (failures=1)
```

I didn't touch anything under `tests/` and haven't committed. To get a full pass, either the test should be fixed to expect success and a balance of 0, or the spec should be changed to require the balance to stay above zero. If you change the spec, the code only needs `amount > self.balance` changed to `amount >= self.balance`.
