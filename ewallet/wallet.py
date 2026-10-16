class EWallet:
    """A simple wallet that holds a balance."""

    def __init__(self, balance=0):
        # Each run starts from the same simple balance; the experiment is about withdraw().
        self.balance = balance

    def withdraw(self, amount):
        """Withdraw amount from the wallet. See SPEC.md."""
        # Deliberately unfinished: the agent receives this stub as its task.
        raise NotImplementedError
