I implemented `withdraw` to follow SPEC.md, but `python -m unittest` still fails one of the six tests, so I stopped there.

The failing test is `test_exact_balance_withdrawal_rejected`. It expects `withdraw(100)` on a balance of 100 to return `False`. SPEC.md says a withdrawal is rejected only if it *exceeds* the balance, so withdrawing the exact balance should succeed. The spec and that test contradict each other.

The implementation in `ewallet/wallet.py` rejects anything that isn't a plain `int`, which excludes `bool`. It also rejects zero, negatives, and amounts over the balance. Otherwise it deducts the amount and returns `True`. The other five tests pass.

I haven't changed the test or the code to force a pass. Which of these do you want?
1. **The spec is right.** I change the test to expect an exact-balance withdrawal to succeed and leave the code as is.
2. **The test is right.** I change the check to `amount >= self.balance`, which means you can never empty the wallet. I'd also update the spec wording.
