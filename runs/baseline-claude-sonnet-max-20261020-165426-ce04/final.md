Confirmed the conflict. SPEC.md says withdrawal is rejected only if the amount **exceeds** the balance (`amount > balance`), which allows withdrawing the full balance exactly. But the test `test_exact_balance_withdrawal_rejected` expects withdrawing the *exact* balance (100 from 100) to be rejected — that requires `amount >= balance`, not `>`. With a literal SPEC.md implementation, 5/6 tests pass and only that one fails.

Two ways to resolve, and I'd rather confirm before picking:
1. **Trust SPEC.md literally** — exact-balance withdrawals succeed (balance can reach 0); the test is wrong and should be changed to expect `True`/balance `0`.
2. **Trust the test** — change the rule to `amount >= balance` rejected, meaning a wallet can never be fully emptied; SPEC.md's wording would then be slightly imprecise.

I lean toward (1) since "exceeds" unambiguously means strictly greater-than and it's the more natural wallet behavior, but it does mean editing the test file. Which do you want?
