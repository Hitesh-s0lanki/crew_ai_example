import unittest
from accounts import Account

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account(account_id='test123', initial_deposit=1000.0)

    def test_deposit_valid_amount(self):
        result = self.account.deposit(500.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 1500.0)

    def test_deposit_invalid_amount(self):
        result = self.account.deposit(-100.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)

    def test_withdraw_valid_amount(self):
        result = self.account.withdraw(500.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 500.0)

    def test_withdraw_invalid_amount(self):
        result = self.account.withdraw(1500.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)

    def test_buy_shares_valid(self):
        result = self.account.buy_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 250.0)
        self.assertEqual(self.account.shares['AAPL'], 5)

    def test_buy_shares_invalid(self):
        result = self.account.buy_shares('AAPL', 50)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)

    def test_sell_shares_valid(self):
        self.account.buy_shares('AAPL', 5)
        result = self.account.sell_shares('AAPL', 3)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 750.0)
        self.assertEqual(self.account.shares['AAPL'], 2)

    def test_sell_shares_invalid(self):
        result = self.account.sell_shares('AAPL', 1)
        self.assertFalse(result)

    def test_get_portfolio_value(self):
        self.account.buy_shares('AAPL', 5)
        self.account.buy_shares('TSLA', 1)
        value = self.account.get_portfolio_value()
        expected_value = 750.0 + 150.0 * 5 + 700.0 * 1
        self.assertEqual(value, expected_value)

    def test_get_profit_or_loss(self):
        self.account.deposit(500.0)
        self.account.buy_shares('AAPL', 5)
        self.account.buy_shares('TSLA', 1)
        profit_or_loss = self.account.get_profit_or_loss()
        expected_value = 750.0 + 150.0 * 5 + 700.0 * 1 - 1000.0
        self.assertEqual(profit_or_loss, expected_value)

    def test_get_holdings_report(self):
        self.account.buy_shares('AAPL', 5)
        self.account.buy_shares('TSLA', 1)
        report = self.account.get_holdings_report()
        self.assertEqual(report, {'AAPL': 5, 'TSLA': 1})

    def test_get_transaction_history(self):
        self.account.deposit(500.0)
        self.account.buy_shares('AAPL', 5)
        self.account.sell_shares('AAPL', 2)
        self.account.withdraw(200.0)
        history = self.account.get_transaction_history()
        expected_history = [
            {'type': 'deposit', 'amount': 500.0},
            {'type': 'buy', 'symbol': 'AAPL', 'quantity': 5},
            {'type': 'sell', 'symbol': 'AAPL', 'quantity': 2},
            {'type': 'withdraw', 'amount': 200.0},
        ]
        self.assertEqual(history, expected_history)

if __name__ == '__main__':
    unittest.main()