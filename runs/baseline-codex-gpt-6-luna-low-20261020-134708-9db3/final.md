Implemented `EWallet.withdraw` per [SPEC.md](/C:/Users/bryan/AppData/Local/Temp/ewallet-task-c1lwus8e/workspace/SPEC.md): it rejects invalid, nonpositive, or balance-exceeding amounts without changing the balance, and deducts valid amounts.

`python -m unittest` passes: 6 tests.
