class Account:
    def __init__(self, account_id: str, initial_deposit: float) -> None:
        self.account_id = account_id
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.shares = {}
        self.transactions = []

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            return False
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount})
        return True

    def withdraw(self, amount: float) -> bool:
        if amount > self.balance or amount <= 0:
            return False
        self.balance -= amount
        self.transactions.append({'type': 'withdraw', 'amount': amount})
        return True

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        price_per_share = self.get_share_price(symbol)
        total_cost = price_per_share * quantity
        if total_cost > self.balance or quantity <= 0:
            return False
        self.balance -= total_cost
        if symbol in self.shares:
            self.shares[symbol] += quantity
        else:
            self.shares[symbol] = quantity
        self.transactions.append({'type': 'buy', 'symbol': symbol, 'quantity': quantity})
        return True

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if symbol not in self.shares or self.shares[symbol] < quantity or quantity <= 0:
            return False
        price_per_share = self.get_share_price(symbol)
        total_revenue = price_per_share * quantity
        self.balance += total_revenue
        self.shares[symbol] -= quantity
        if self.shares[symbol] == 0:
            del self.shares[symbol]
        self.transactions.append({'type': 'sell', 'symbol': symbol, 'quantity': quantity})
        return True

    def get_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.shares.items():
            total_value += self.get_share_price(symbol) * quantity
        return total_value

    def get_profit_or_loss(self) -> float:
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings_report(self) -> dict:
        return self.shares.copy()

    def get_transaction_history(self) -> list:
        return self.transactions.copy()

    def get_share_price(self, symbol: str) -> float:
        # Test implementation returning fixed prices
        prices = {'AAPL': 150.00, 'TSLA': 700.00, 'GOOGL': 2800.00}
        return prices.get(symbol, 0.0)

# Example usage
account = Account(account_id="user123", initial_deposit=1000.00)
account.deposit(500.00)
account.buy_shares("AAPL", 5)
account.sell_shares("AAPL", 2)
account.withdraw(200.00)
print(account.get_portfolio_value())
print(account.get_profit_or_loss())
print(account.get_holdings_report())
print(account.get_transaction_history())
