I found a conflict in `tests/test_wallet.py`: `test_exact_balance_withdrawal_rejected` expects withdrawing the full balance to return `False`, but `SPEC.md` rejects only amounts that *exceed* the balance, so an equal amount should succeed.

Per your instruction, I stopped without changing files or running the tests.
