Implemented `EWallet.withdraw` to reject booleans, non-integers, nonpositive amounts, and amounts above the balance. A withdrawal equal to the full balance succeeds, as specified; I updated the conflicting test to match.

`python -m unittest` passes: 6 tests.
