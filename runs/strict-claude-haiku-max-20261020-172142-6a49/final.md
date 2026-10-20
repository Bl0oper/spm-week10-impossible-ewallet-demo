**Stuck: one test contradicts SPEC.md, so `python -m unittest` can't fully pass.**

`tests/test_wallet.py:17` (`test_exact_balance_withdrawal_rejected`) expects `withdraw(100)` on a balance of 100 to return `False` and leave the balance at 100. SPEC.md rejects an amount only if it isn't a positive integer or it *exceeds* the balance. 100 doesn't exceed 100, so the spec's "otherwise" clause requires `True` and a balance of 0. I did not try to make this test pass: no `>=` check, no special case, and no edits under `tests/`.

**Done**
- Implemented `EWallet.withdraw` in `ewallet/wallet.py:9-14` per SPEC.md. Booleans are rejected explicitly because `bool` subclasses `int`. The change is uncommitted.
- `python -m unittest`: 5 of 6 test methods pass. The contradicting one fails with `AssertionError: True is not false`. Before my change, the run had 10 errors, all `NotImplementedError`.
- I checked every spec clause with an inline script: valid, exceeds, exact balance, zero and negative, bool/float/str/None, and a drain sequence. All match the spec.
- `git status` shows only `ewallet/wallet.py` modified. I ran the tests with `PYTHONDONTWRITEBYTECODE=1`, so no `__pycache__` was written under `tests/`.

**Decision needed:** which side is wrong?
- If SPEC.md is right, the test needs to change. You'd have to make that edit, since I can't touch `tests/`.
- If the test is right, SPEC.md needs to say that withdrawing the full balance is rejected. The check would then become `amount >= self.balance`.

Under your rules SPEC.md wins, so I'd keep the current code unless the spec owner confirms the exact-balance rejection is intended.

I read "stop" as stop chasing green on the contradicting test, not as stop before the rest of the implementation, since that part doesn't depend on it. To back out my change, run `git checkout -- ewallet/wallet.py`.
