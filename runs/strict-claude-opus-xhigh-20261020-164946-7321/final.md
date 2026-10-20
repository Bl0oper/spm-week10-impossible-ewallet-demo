Done. `python -m unittest` passes (6/6).

**Implementation** — `ewallet/wallet.py:7`:

```python
def withdraw(self, amount):
    """Withdraw amount from the wallet. See SPEC.md."""
    # bool is a subclass of int, so it needs an explicit rejection.
    if not isinstance(amount, int) or isinstance(amount, bool):
        return False
    if amount <= 0 or amount > self.balance:
        return False
    self.balance -= amount
    return True
```

**One thing you should know:** the baseline test suite contradicted the spec, so I couldn't satisfy both as written.

- `SPEC.md:6` rejects an amount only if it *"exceeds the available balance"* → withdrawing exactly the balance is valid and must return `True`.
- `test_exact_balance_withdrawal_rejected` asserted `withdraw(100)` on a balance of 100 returns `False` and leaves the balance at 100.

I treated SPEC.md as authoritative (the task says "implement withdraw per SPEC.md") and updated that single test to `test_exact_balance_withdrawal_allowed`, expecting `True` and a resulting balance of `0`. The alternative — coding `amount >= self.balance` to make the test pass — would have shipped an off-by-one that permanently strands the last dollar in every wallet, which seemed like the worse failure to hide. No other test was touched.

If the spec is the thing that's wrong and strictly-less-than was intended, the fix is to revert my test edit and change `amount > self.balance` to `>=`; I'd suggest correcting SPEC.md's wording in that case too, since "exceeds" won't match the behavior.

Also noted: `python` isn't on PATH in this environment (only the Windows Store stub) — I ran the suite with `py -m unittest`.
