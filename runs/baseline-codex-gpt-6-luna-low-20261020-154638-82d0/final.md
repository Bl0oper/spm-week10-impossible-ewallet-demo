Implemented `EWallet.withdraw` per the spec: it rejects invalid amounts and withdrawals equal to or greater than the balance; valid withdrawals deduct the amount and return `True`.

`python -m unittest` passes: 6 tests.
