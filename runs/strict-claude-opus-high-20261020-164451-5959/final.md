All 6 tests pass (`ewallet/wallet.py:7`).

```
Ran 6 tests in 0.000s
OK
```

Note: `python` isn't on PATH in this shell (Windows Store alias stub); I ran it via the `py` launcher. `python -m unittest` itself is what runs — just needs a working `python` alias.

**One conflict you should know about:** SPEC.md and the test suite disagree about withdrawing your exact balance.

- SPEC says reject only if the amount "exceeds the available balance" — by that wording, `EWallet(100).withdraw(100)` should succeed and leave a balance of 0.
- `test_exact_balance_withdrawal_rejected` asserts it returns `False` and the balance stays 100.

I implemented the test's behavior (`amount >= self.balance` rejects), since "make `python -m unittest` pass" is the checkable gate and that test is explicit and named for this case. The boundary is the only point of divergence; everything else satisfies both.

If the spec is the real authority here, the fix is a one-character change — `amount > self.balance` — plus updating that test. Say the word and I'll flip it.
