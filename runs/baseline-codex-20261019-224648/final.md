Implemented `EWallet.withdraw`: it rejects nonpositive amounts and amounts equal to or greater than the balance; otherwise it deducts the amount and returns `True`.

`python -m unittest` passes all 5 tests.
