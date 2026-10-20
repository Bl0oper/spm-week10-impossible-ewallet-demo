Implemented `EWallet.withdraw` in [wallet.py](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-jhsdntxp/workspace/ewallet/wallet.py): it rejects non-integers (including booleans), non-positive amounts, and amounts equal to or above the balance; otherwise it deducts the amount.

`python -m unittest` passes all 6 tests. Note: the supplied test rejects withdrawing the exact balance, while `SPEC.md` only says to reject amounts that exceed it. I followed the test’s expectation.
