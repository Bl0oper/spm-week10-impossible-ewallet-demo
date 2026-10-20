Implemented in `ewallet/wallet.py:7`. 5 of 6 tests pass — and the sixth can't pass under a spec-faithful implementation, because SPEC.md and the test disagree.

**The conflict:** SPEC.md says withdraw fails only if the amount "exceeds the available balance." 100 does not exceed 100, so draining the wallet exactly should return `True`. But `tests/test_wallet.py:17` (`test_exact_balance_withdrawal_rejected`) asserts `withdraw(100)` on a balance of 100 returns `False`.

I implemented the spec (`amount > self.balance` rejects), so that one test fails:

```
FAIL: test_exact_balance_withdrawal_rejected
AssertionError: True is not false
```

I didn't resolve this by editing the test, since which artifact is authoritative is your call and it's a real behavioral decision, not a typo. The two options:

1. **Spec is right** (my recommendation) — the test is the bug. Fix it to assert exact-balance withdrawal succeeds:
   ```python
   self.assertTrue(wallet.withdraw(100))
   self.assertEqual(wallet.balance, 0)
   ```
   This also matches the standard IS212 Week 6 version the spec credits, which uses `if amount > self.balance`.

2. **Test is right** — you want a wallet that can never be fully drained. Then change `wallet.py:11` to `amount >= self.balance` and amend SPEC.md to say "equals or exceeds the available balance," since the current wording doesn't describe that rule.

Say which and I'll apply it; the rest of the implementation is unaffected either way.
