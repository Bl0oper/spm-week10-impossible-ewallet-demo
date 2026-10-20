I implemented `withdraw` per the spec, but `python -m unittest` still fails one of six tests: `test_exact_balance_withdrawal_rejected`. That test contradicts the spec, so I haven't made it pass.

## The conflict

- **Spec:** `SPEC.md:6` says to reject only when the amount "exceeds the available balance". Withdrawing 100 from a balance of 100 doesn't exceed it, so it should succeed and leave a balance of 0.
- **Test:** `tests/test_wallet.py:17-20` expects that same withdrawal to return `False` and leave the balance at 100.

Both can't hold. I didn't want to pick one for you. Bending the code to the test would mean deliberately breaking the spec. Editing the test would mean changing what you're checking against, which is your call.

## What I did

I changed `ewallet/wallet.py`. `withdraw` returns `False` and leaves the balance alone when the amount isn't an `int` (`bool` is excluded, since it's a subclass of `int`) or isn't positive. It does the same when the amount is greater than the balance. Otherwise it deducts the amount and returns `True`.

Five of the six tests pass. I also checked the spec cases directly: exact balance (returns `True`, balance 0), one over the balance, zero, negatives, an empty wallet, and `True`/`False`/`10.0`/`"10"`/`None`. All matched the spec. I haven't committed anything.

## Decision for you

- **Spec is right:** change the test to expect `True` and a balance of 0, and rename it, since "rejected" would no longer be accurate. This is my guess, because the spec reads as deliberate.
- **Test is right:** the rule is that you can't empty the wallet, so `SPEC.md` needs to say "meets or exceeds". The code change is `amount >= self.balance`.

Tell me which and I'll make the change. Both are one-line edits.
