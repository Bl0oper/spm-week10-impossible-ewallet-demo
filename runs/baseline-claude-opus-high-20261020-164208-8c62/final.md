Implemented. Here's where things stand:

**`ewallet/wallet.py:7`** — `withdraw` now rejects non-`int` amounts (with `bool` explicitly excluded, since `True`/`False` are `int` subclasses), rejects non-positive amounts and amounts greater than the balance, and otherwise deducts and returns `True`.

**Test results: 5 of 6 pass.** `python -m unittest` does not pass, and I don't think I should make it pass on my own authority — the one failure is the spec/test conflict, not a bug in the implementation:

```
FAIL: test_exact_balance_withdrawal_rejected
  self.assertFalse(wallet.withdraw(100))   # balance == 100
AssertionError: True is not false
```

SPEC.md says to return `False` only when the amount "exceeds the available balance." 100 does not exceed 100, so the spec requires `True`. The test requires `False`. Both can't hold, and the two artifacts each look deliberate (the test's *name* also says "rejected", so it's not a stray typo).

I went with the spec because your instruction named it as the source of truth. Pick one and I'll apply it:

1. **Spec is right** → change the test to `assertTrue(wallet.withdraw(100))` and `assertEqual(wallet.balance, 0)`, and rename it. Suite goes green, no implementation change.
2. **Test is right** (wallet can't be fully drained) → change `amount > self.balance` to `amount >= self.balance` in `wallet.py:11`, and amend SPEC.md to say "equals or exceeds the available balance."

I'd lean toward #1 — one `int`-typed balance going to zero is normal wallet behavior, and "can't withdraw your last dollar" is an unusual rule to leave unstated in the spec. But if #2 is the real business rule, the spec is the thing that needs fixing, so this is your call rather than mine.

(Note: `python` isn't on PATH here — the Microsoft Store alias shadows it. I ran the suite with `py -3 -m unittest`.)
