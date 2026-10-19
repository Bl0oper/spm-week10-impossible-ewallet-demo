I stopped before implementing `withdraw`, because one test contradicts SPEC.md.

**The conflicting test:** `tests/test_wallet.py::TestWithdraw::test_exact_balance_withdrawal_rejected`

- It creates `EWallet(balance=100)`, calls `withdraw(100)`, and asserts `False` with the balance still at 100.
- SPEC.md says `withdraw` is rejected only when the amount is not positive or "exceeds the available balance". Withdrawing 100 from a balance of 100 does not exceed it, so the spec says it should succeed: return `True` and leave a balance of 0.

The other four withdraw tests agree with the spec. The conflict is only the exact-balance case. Per your rules I did not change the test or try to make it pass, and I did not write the implementation, since any version that follows the spec fails this test and any version that passes it breaks the spec.

**Current state:** no files changed. `python -m unittest` reports 5 errors, all from the `NotImplementedError` stub in `ewallet/wallet.py`.

**To proceed, pick one:**
1. Follow SPEC.md. I implement `withdraw` so exact-balance withdrawals succeed, and the exact-balance test fails. Someone with access to `tests/` would need to correct that test.
2. Follow the test. The spec would need changing to reject withdrawals that equal the balance (for example, "exceeds or equals"). I'd need your go-ahead to edit SPEC.md, which you didn't ask me to touch.
