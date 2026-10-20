All 6 tests pass with `py -m unittest`. Implemented `withdraw` in ewallet/wallet.py: rejects non-int/bool amounts, rejects amounts ≤ 0 or ≥ balance, otherwise deducts and returns True.
