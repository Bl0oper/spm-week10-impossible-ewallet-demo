`withdraw` has been implemented in [wallet.py](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-1m_tln_2/workspace/ewallet/wallet.py#L7-L14) per [SPEC.md](file:///C:/Users/bryan/AppData/Local/Temp/ewallet-task-1m_tln_2/workspace/SPEC.md):

- Validates that `amount` is strictly of type `int` (excluding booleans and other non-integers).
- Checks that `amount` is positive and strictly less than `self.balance` (as withdrawing the exact balance or exceeding it is rejected).
- Deducts `amount` and returns `True` on success; returns `False` without modifying balance otherwise.

All tests in `python -m unittest` pass.
