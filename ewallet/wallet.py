class EWallet:
    """A simple wallet that holds a balance."""

    def __init__(self, balance=0):
        self.balance = balance

    def withdraw(self, amount):
        """Withdraw amount from the wallet. See SPEC.md."""
        raise NotImplementedError
