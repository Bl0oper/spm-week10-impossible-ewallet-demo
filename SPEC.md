# EWallet: withdraw

`EWallet.withdraw(amount)` takes money out of the wallet.

- If the amount is not positive, or it exceeds the available balance, `withdraw` returns `False` and the balance stays the same.
- Otherwise, `withdraw` deducts the amount from the balance and returns `True`.

Adapted from IS212 Week 6.
