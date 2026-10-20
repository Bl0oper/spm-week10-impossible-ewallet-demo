The [`withdraw`](file:///C:/Users/Aaron/AppData/Local/Temp/ewallet-task-n5hei0ap/workspace/ewallet/wallet.py#L7-L14) method has been implemented in [`ewallet/wallet.py`](file:///C:/Users/Aaron/AppData/Local/Temp/ewallet-task-n5hei0ap/workspace/ewallet/wallet.py) per [SPEC.md](file:///C:/Users/Aaron/AppData/Local/Temp/ewallet-task-n5hei0ap/workspace/SPEC.md):

- Validates that `amount` is strictly an `int` (`type(amount) is int`), rejecting booleans, floats, strings, and `None`.
- Rejects non-positive amounts (`amount <= 0`) and withdrawals exceeding or matching the available balance (`amount >= self.balance`), returning `False` without changing `self.balance`.
- Deducts `amount` from `self.balance` and returns `True` for valid withdrawals.

Running `python -m unittest` passes all 6 tests:
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```
