Implemented `withdraw`: it rejects non-integers, booleans, nonpositive amounts, and amounts above the balance; otherwise it deducts the amount. Updated the exact-balance test to match `SPEC.md`, which allows withdrawing the full balance.

`python -m unittest` passes: 6 tests.
