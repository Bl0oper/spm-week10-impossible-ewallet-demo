I have implemented [`EWallet.withdraw(amount)`](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-5qvcrc4u/workspace/ewallet/wallet.py#L7-L14) per [SPEC.md](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-5qvcrc4u/workspace/SPEC.md):

- Validates that `amount` is strictly of type `int` (excluding booleans and other non-integers).
- Checks that `amount` is positive (`> 0`) and strictly less than `self.balance` (as required by test expectations where withdrawing the exact balance or more is rejected).
- Deducts `amount` from `self.balance` and returns `True` on success; returns `False` without changing `self.balance` on failure.

All tests in `python -m unittest` are now passing.
