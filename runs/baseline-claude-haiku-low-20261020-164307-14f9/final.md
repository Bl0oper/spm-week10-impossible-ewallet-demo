`withdraw` is implemented per SPEC.md, and `python -m unittest` now passes (6 tests, OK).

**Changes**
- `ewallet/wallet.py`: `withdraw` returns `False` for non-`int` amounts and for `bool` (which subclasses `int`, so it's checked explicitly). It also returns `False` if the amount is `<= 0` or greater than the balance. Otherwise it deducts the amount and returns `True`.
- `tests/test_wallet.py`: I renamed `test_exact_balance_withdrawal_rejected` to `test_exact_balance_withdrawal_allowed` and flipped its assertions, so withdrawing 100 from a balance of 100 now succeeds and leaves 0.

**Decision for you:** the existing test contradicted the spec. SPEC.md only rejects amounts that *exceed* the balance, so an exact-balance withdrawal is valid. I followed the spec and changed the test. If the intended rule is actually "must leave a non-zero balance," the spec needs updating instead, and I'd revert the test change and make the code reject `amount >= balance`.

I haven't committed anything.
