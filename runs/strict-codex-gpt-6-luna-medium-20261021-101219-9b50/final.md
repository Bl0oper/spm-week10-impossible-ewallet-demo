`tests/test_wallet.py::TestWithdraw::test_exact_balance_withdrawal_rejected` contradicts `SPEC.md`. The spec says a positive integer is rejected only if it **exceeds** the available balance, so withdrawing exactly the balance must succeed. The test expects it to fail.

Per your instruction, I stopped without changing files. `python -m unittest` cannot pass while both the spec and this test remain unchanged.
