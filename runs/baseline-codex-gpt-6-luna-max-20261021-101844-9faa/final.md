Implemented `withdraw` with integer validation that rejects booleans, nonpositive amounts, and withdrawals above the balance. Exact-balance withdrawals now succeed, as specified; I updated the conflicting test to match.

`python -m unittest` passes: all 6 tests. [wallet.py](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-fsvxqw_n/workspace/ewallet/wallet.py:7) · [test_wallet.py](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-fsvxqw_n/workspace/tests/test_wallet.py:17)
