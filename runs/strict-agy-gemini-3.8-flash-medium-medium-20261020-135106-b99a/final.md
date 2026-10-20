A test contradicts [SPEC.md](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-ixcnljru/workspace/SPEC.md). Per the instructions, stopping execution and reporting the details:

### Contradicting Test
[`TestWithdraw.test_exact_balance_withdrawal_rejected`](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-ixcnljru/workspace/tests/test_wallet.py#L17-L21) in [tests/test_wallet.py](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-ixcnljru/workspace/tests/test_wallet.py):

```python
    def test_exact_balance_withdrawal_rejected(self):
        wallet = EWallet(balance=100)
        self.assertFalse(wallet.withdraw(100))
        self.assertEqual(wallet.balance, 100)
```

### Why it Contradicts SPEC.md
- [SPEC.md](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-ixcnljru/workspace/SPEC.md) defines rejection criteria as:
  > *"If the amount is not a positive integer, or it exceeds the available balance, `withdraw` returns `False` and the balance stays the same."*
  > *"Otherwise, `withdraw` deducts the amount from the balance and returns `True`."*
- An amount equal to the balance (`100` when balance is `100`) is a positive integer and **does not exceed** the available balance (`100 > 100` is false).
- Therefore, according to [SPEC.md](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-ixcnljru/workspace/SPEC.md), withdrawing the exact balance is a valid withdrawal that should deduct the amount (reducing the balance to `0`) and return `True`.
- The test instead asserts that withdrawing the exact balance returns `False` and keeps the balance at `100`.
