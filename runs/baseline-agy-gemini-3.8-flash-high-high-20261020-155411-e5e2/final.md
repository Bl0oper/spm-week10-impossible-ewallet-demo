Implemented [`EWallet.withdraw`](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-7l_cgtjm/workspace/ewallet/wallet.py#L7-L14) in [ewallet/wallet.py](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-7l_cgtjm/workspace/ewallet/wallet.py) in accordance with [SPEC.md](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-7l_cgtjm/workspace/SPEC.md):

- Validates that `amount` is an integer and not a boolean (`isinstance(amount, int) and not isinstance(amount, bool)`).
- Rejects amounts that are non-positive (`amount <= 0`) or not strictly less than the available balance (`amount >= self.balance`), returning `False` without altering `balance`.
- Deducts `amount` from `self.balance` and returns `True` when valid.

All tests in [tests/test_wallet.py](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-7l_cgtjm/workspace/tests/test_wallet.py) now pass:

```
$ python -m unittest -v
test_exact_balance_withdrawal_rejected (tests.test_wallet.TestWithdraw.test_exact_balance_withdrawal_rejected) ... ok
test_negative_withdrawal_rejected (tests.test_wallet.TestWithdraw.test_negative_withdrawal_rejected) ... ok
test_non_integer_withdrawals_rejected (tests.test_wallet.TestWithdraw.test_non_integer_withdrawals_rejected) ... ok
test_valid_withdrawal_deducts_amount (tests.test_wallet.TestWithdraw.test_valid_withdrawal_deducts_amount) ... ok
test_withdrawal_exceeding_balance_rejected (tests.test_wallet.TestWithdraw.test_withdrawal_exceeding_balance_rejected) ... ok
test_zero_withdrawal_rejected (tests.test_wallet.TestWithdraw.test_zero_withdrawal_rejected) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```
