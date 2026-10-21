Implemented `EWallet.withdraw` with integer validation, positive-amount and balance checks, and balance deduction. Updated the exact-balance test to match the spec: withdrawing the full balance succeeds.

`python -m unittest` passed: **6 tests**. `git diff --check` reported no issues.

Changed [wallet.py](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-2e6fgemi/workspace/ewallet/wallet.py:8) and [test_wallet.py](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-2e6fgemi/workspace/tests/test_wallet.py:17).
