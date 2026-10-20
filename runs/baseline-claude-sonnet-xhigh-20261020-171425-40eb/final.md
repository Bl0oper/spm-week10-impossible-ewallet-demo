`withdraw` is implemented per SPEC.md, but `python -m unittest` doesn't fully pass. 5 of 6 tests pass, and `test_exact_balance_withdrawal_rejected` fails because it contradicts the spec.

**Implementation** (`ewallet/wallet.py`): `withdraw` returns `False`, leaving the balance unchanged, if the amount isn't an `int`, isn't positive, or exceeds the balance. Otherwise it deducts the amount and returns `True`. I used `type(amount) is not int` instead of `isinstance`, because `bool` is a subclass of `int` and the spec says booleans are invalid.

**The conflict:**
- **Spec:** it says to reject a withdrawal only if it "exceeds the available balance". Withdrawing exactly 100 from a balance of 100 doesn't exceed it, so it should succeed and return `True`.
- **Test:** `test_exact_balance_withdrawal_rejected` (`tests/test_wallet.py:17`) expects `False` and a balance still at 100.

I can't satisfy both. I followed the spec and left the test alone. The alternative is to reject `amount >= balance`, which would pass the test but contradict the spec. The test name suggests it was written deliberately, so I didn't want to pick for you.

Which one is right?
- **Spec is right:** I'll change that test to expect `True` and a balance of 0, and rename it. That gets everything passing.
- **Test is right:** I'll change the check to `amount >= self.balance`, and you'd want to update SPEC.md to say an exact-balance withdrawal is rejected.
