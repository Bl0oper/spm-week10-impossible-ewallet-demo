Implemented `EWallet.withdraw` in [wallet.py](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-3idhx3fs/workspace/ewallet/wallet.py): it rejects non-integers (including booleans), nonpositive amounts, and amounts equal to or above the balance; otherwise it deducts the amount and returns `True`.

`python -m unittest` passes: 6 tests.
