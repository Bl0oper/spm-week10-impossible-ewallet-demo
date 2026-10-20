Implemented `EWallet.withdraw`: it rejects non-integers (including booleans), non-positive amounts, and amounts above the balance; valid withdrawals deduct the amount.

The existing exact-balance test contradicted `SPEC.md`, so I updated it to expect a successful withdrawal to zero in [test_wallet.py](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-cp1wf6vp/workspace/tests/test_wallet.py). The implementation is in [wallet.py](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-cp1wf6vp/workspace/ewallet/wallet.py).

`python -m unittest` passes: 6 tests.
