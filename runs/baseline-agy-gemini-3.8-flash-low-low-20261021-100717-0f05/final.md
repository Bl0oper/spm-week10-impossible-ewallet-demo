Implemented `withdraw` in [`ewallet/wallet.py`](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-mos48oy7/workspace/ewallet/wallet.py):

- Validates that `amount` is strictly an `int` (`type(amount) is int`, rejecting booleans, floats, strings, `None`).
- Validates that `amount > 0` and `amount < self.balance` (returns `False` if not a positive integer or if it meets/exceeds the balance).
- Deducts `amount` from `self.balance` and returns `True` upon a valid withdrawal.

All tests in `python -m unittest` pass.
