The implementation follows SPEC.md, but one test contradicts the spec, so `python -m unittest` does not pass yet.

**What I changed:** `ewallet/wallet.py` `withdraw` now returns `False` if `amount <= 0` or `amount > self.balance`. Otherwise it subtracts the amount and returns `True`.

**The conflict:** SPEC.md says a withdrawal is rejected only when the amount *exceeds* the balance. Withdrawing exactly the balance is therefore allowed, and the wallet ends at 0. `test_exact_balance_withdrawal_rejected` asserts the opposite: that `withdraw(100)` on a balance of 100 returns `False`.

**Current result:** 4 of 5 tests pass. The one failure is `test_exact_balance_withdrawal_rejected`.

I did not edit the test or the spec, since either choice changes behavior you've defined. Which one should win?
- **Keep the spec (exact balance allowed):** I change or remove that test. The suite then passes.
- **Keep the test (exact balance rejected):** I change the condition to `amount >= self.balance`. That contradicts SPEC.md, so the spec would need updating too.

I haven't committed anything.
