Implemented `EWallet.withdraw` in `ewallet/wallet.py`:

- Rejects non-`int` amounts, explicitly excluding `bool` (since `bool` is a subclass of `int` in Python).
- Rejects non-positive amounts and amounts that are `>=` the current balance (matching `test_exact_balance_withdrawal_rejected`, which requires exact-balance withdrawals to also be rejected).
- Otherwise deducts the amount and returns `True`.

All 6 tests in `tests/test_wallet.py` pass via `py -m unittest` (the `python` alias itself is unresolvable in this environment — it points to a Windows Store stub — but the `py` launcher runs the identical `unittest` module and shell).
