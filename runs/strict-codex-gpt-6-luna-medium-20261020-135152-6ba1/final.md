`tests/test_wallet.py::TestWithdraw::test_exact_balance_withdrawal_rejected` contradicts `SPEC.md`: the spec says to reject amounts that *exceed* the balance, so withdrawing the exact balance should succeed and leave a zero balance. The test expects rejection and an unchanged balance.

Per your instruction, I stopped without editing files or running the suite.
