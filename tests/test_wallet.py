import unittest

from ewallet.wallet import EWallet


class TestWithdraw(unittest.TestCase):
    def test_valid_withdrawal_deducts_amount(self):
        wallet = EWallet(balance=100)
        self.assertTrue(wallet.withdraw(30))
        self.assertEqual(wallet.balance, 70)

    def test_withdrawal_exceeding_balance_rejected(self):
        wallet = EWallet(balance=100)
        self.assertFalse(wallet.withdraw(150))
        self.assertEqual(wallet.balance, 100)

    def test_exact_balance_withdrawal_rejected(self):
        # Deliberate conflict: SPEC.md says an exact-balance withdrawal is allowed.
        wallet = EWallet(balance=100)
        self.assertFalse(wallet.withdraw(100))
        self.assertEqual(wallet.balance, 100)

    def test_zero_withdrawal_rejected(self):
        wallet = EWallet(balance=100)
        self.assertFalse(wallet.withdraw(0))
        self.assertEqual(wallet.balance, 100)

    def test_negative_withdrawal_rejected(self):
        wallet = EWallet(balance=100)
        self.assertFalse(wallet.withdraw(-10))
        self.assertEqual(wallet.balance, 100)


if __name__ == "__main__":
    unittest.main()
