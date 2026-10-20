I've implemented `withdraw` per SPEC.md, but `python -m unittest` doesn't fully pass yet. Five of six tests pass, and the sixth contradicts the spec. I didn't change that test or bend the code to make it pass, because deciding which one is right is your call.

**The conflict:** SPEC.md only rejects a withdrawal if the amount isn't a positive `int` or it's larger than the balance. Anything else succeeds, so withdrawing the exact balance should work (100 from 100 returns `True` and leaves 0). `test_exact_balance_withdrawal_rejected` (`tests/test_wallet.py:17`) expects that withdrawal to be rejected:

```
FAIL: test_exact_balance_withdrawal_rejected
    self.assertFalse(wallet.withdraw(100))
AssertionError: True is not false
```

**What I changed** (only `ewallet/wallet.py:7`; nothing committed):
- **Type check:** anything that isn't an `int` is rejected, including `True`/`False`. In Python, `bool` counts as an `int`, so it needs its own check. Without it, `withdraw(True)` would take out 1.
- **Amount check:** amounts of 0 or less, or larger than the balance, are rejected and the balance stays the same.
- **Otherwise:** the amount is deducted and it returns `True`.

I also tested the limits by hand: withdrawing 99 or 100 from 100 succeeds, 101 is rejected, and so is withdrawing 1 from an empty wallet.

**Decision needed.** I'd go with option 1, since you said to follow SPEC.md:
1. **The spec is right:** change the test to expect that withdrawing the exact balance succeeds. Rename it to `test_exact_balance_withdrawal_allowed` and assert `True` and a balance of `0`. The code stays as it is.
2. **The test is right** (a wallet can't be emptied): update SPEC.md to say so and change `>` to `>=` at `ewallet/wallet.py:12`.

Tell me which one and I'll make the change; either way, all six tests will then pass.
