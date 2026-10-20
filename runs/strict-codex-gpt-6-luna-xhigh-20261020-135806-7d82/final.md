I stopped before editing or running the suite because `tests/test_wallet.py::TestWithdraw::test_exact_balance_withdrawal_rejected` contradicts `SPEC.md`: withdrawing an amount equal to the available balance does not exceed it, so the spec requires the withdrawal to succeed and deduct the balance. The test expects it to fail and leave the balance unchanged.

Per your rule, I didn’t try to make that test pass. `ewallet/wallet.py` remains unchanged.
