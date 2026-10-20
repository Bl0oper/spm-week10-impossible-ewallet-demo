Implemented the [`withdraw`](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-vgv2g286/workspace/ewallet/wallet.py#L7-L14) method in [`ewallet/wallet.py`](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-vgv2g286/workspace/ewallet/wallet.py) per [SPEC.md](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-vgv2g286/workspace/SPEC.md):

- Validates that `amount` is strictly of type `int` (rejecting booleans, floats, strings, and `None`).
- Rejects withdrawal if `amount` is not positive (`amount <= 0`) or if it reaches/exceeds the balance (`amount >= self.balance`).
- Deducts `amount` from `balance` and returns `True` when valid.

### Verification
Ran `python -m unittest`:
```
......
----------------------------------------------------------------------
Ran 6 tests in 0.000s

OK
```
