Implemented `EWallet.withdraw` per [SPEC.md](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-2dsu5_e3/workspace/SPEC.md): invalid amounts and withdrawals equal to or above the balance return `False` without changing the balance; valid withdrawals deduct the amount and return `True`.

`python -m unittest` passes: 6 tests.
