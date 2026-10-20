Implemented `EWallet.withdraw` in [wallet.py](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-q4t0v87t/workspace/ewallet/wallet.py): it rejects non-integers (including booleans), nonpositive amounts, and withdrawals equal to or above the balance; valid withdrawals deduct the amount and return `True`.

`python -m unittest` passes: 6 tests. Note: the existing exact-balance test expects rejection, while `SPEC.md` says only amounts that *exceed* the balance are rejected. I followed the test’s expectation for exact-balance withdrawals.
