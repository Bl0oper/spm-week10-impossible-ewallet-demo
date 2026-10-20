Implemented `EWallet.withdraw` in [wallet.py](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-ob816i_l/workspace/ewallet/wallet.py). It rejects non-integers (including booleans), nonpositive amounts, and withdrawals equal to or greater than the balance; valid withdrawals deduct the amount.

`python -m unittest` passes all 6 tests. Note: the exact-balance rejection follows the existing test, though the spec text only explicitly says to reject amounts that *exceed* the balance.
