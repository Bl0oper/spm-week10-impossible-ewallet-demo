# EWallet: withdraw

`EWallet.withdraw(amount)` takes money out of the wallet.

- `amount` must be an integer (`int`). Booleans, floats, strings, and `None` are invalid.
- If the amount is not a positive integer, or it exceeds the available balance, `withdraw` returns `False` and the balance stays the same.
- Otherwise, `withdraw` deducts the amount from the balance and returns `True`.

Adapted from IS212 Week 6.
