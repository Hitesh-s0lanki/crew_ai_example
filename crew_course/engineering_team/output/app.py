import gradio as gr
from accounts import Account

# Initialize global account with a default demo account
account = Account(account_id="demo_account", initial_deposit=1000.00)

def create_account(account_id: str, initial_deposit: float) -> str:
    global account
    account = Account(account_id, initial_deposit)
    return f"✅ Account '{account_id}' created with balance ${account.balance:.2f}"  

def deposit_funds(amount: float) -> str:
    if amount <= 0:
        return "❌ Deposit amount must be positive."
    account.deposit(amount)
    return f"✅ Deposited ${amount:.2f}. New balance: ${account.balance:.2f}"

def withdraw_funds(amount: float) -> str:
    if amount <= 0:
        return "❌ Withdrawal amount must be positive."
    if account.withdraw(amount):
        return f"✅ Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
    return "❌ Insufficient funds for withdrawal."

def buy_shares(symbol: str, quantity: int) -> str:
    if quantity <= 0:
        return "❌ Quantity must be at least 1."
    if account.buy_shares(symbol, quantity):
        return f"✅ Bought {quantity} share(s) of {symbol}. Remaining balance: ${account.balance:.2f}"  
    return "❌ Insufficient balance to buy shares."

def sell_shares(symbol: str, quantity: int) -> str:
    if quantity <= 0:
        return "❌ Quantity must be at least 1."
    if account.sell_shares(symbol, quantity):
        return f"✅ Sold {quantity} share(s) of {symbol}. Remaining balance: ${account.balance:.2f}"  
    return "❌ Not enough shares to sell."

def get_portfolio_value() -> str:
    value = account.get_portfolio_value()
    return f"📊 Total Portfolio Value: ${value:.2f}"

def get_profit_or_loss() -> str:
    pnl = account.get_profit_or_loss()
    sign = "📈" if pnl >= 0 else "📉"
    return f"{sign} Profit/Loss: ${pnl:.2f}"

def get_holdings_report() -> str:
    return f"🗄️ Holdings: {account.get_holdings_report()}"

def get_transaction_history() -> str:
    return f"📜 Transactions: {account.get_transaction_history()}"

if __name__ == "__main__":
    with gr.Blocks(title="Trading Simulation Platform") as demo:
        gr.Markdown("# Trading Simulation Platform")

        with gr.Tab("Account Setup"):
            with gr.Row():
                account_id_input = gr.Textbox(label="Account ID", placeholder="e.g., demo_account")
                initial_deposit_input = gr.Number(value=1000.00, label="Initial Deposit", precision=2)
                create_btn = gr.Button("Create Account")
            create_output = gr.Textbox(label="Status", interactive=False)
            create_btn.click(create_account, inputs=[account_id_input, initial_deposit_input], outputs=create_output)

        with gr.Tab("Transactions"):
            with gr.Column():
                with gr.Row():
                    dep_amt = gr.Number(label="Deposit Amount", precision=2)
                    dep_btn = gr.Button("Deposit")
                dep_out = gr.Textbox(label="Deposit Status", interactive=False)
                dep_btn.click(deposit_funds, inputs=dep_amt, outputs=dep_out)

                with gr.Row():
                    wd_amt = gr.Number(label="Withdraw Amount", precision=2)
                    wd_btn = gr.Button("Withdraw")
                wd_out = gr.Textbox(label="Withdrawal Status", interactive=False)
                wd_btn.click(withdraw_funds, inputs=wd_amt, outputs=wd_out)

                with gr.Row():
                    symbol_in = gr.Textbox(label="Stock Symbol", placeholder="e.g., AAPL")
                    qty_in = gr.Number(value=1, label="Quantity", precision=0)
                    buy_btn = gr.Button("Buy")
                    sell_btn = gr.Button("Sell")
                buy_out = gr.Textbox(label="Buy Status", interactive=False)
                sell_out = gr.Textbox(label="Sell Status", interactive=False)
                buy_btn.click(buy_shares, inputs=[symbol_in, qty_in], outputs=buy_out)
                sell_btn.click(sell_shares, inputs=[symbol_in, qty_in], outputs=sell_out)

        with gr.Tab("Portfolio"):
            with gr.Row():
                val_btn = gr.Button("Portfolio Value")
                pnl_btn = gr.Button("Profit/Loss")
                hold_btn = gr.Button("Holdings Report")
                hist_btn = gr.Button("Transaction History")
            val_out = gr.Textbox(label="Value", interactive=False)
            pnl_out = gr.Textbox(label="P/L", interactive=False)
            hold_out = gr.Textbox(label="Holdings", interactive=False)
            hist_out = gr.Textbox(label="History", interactive=False)

            val_btn.click(get_portfolio_value, outputs=val_out)
            pnl_btn.click(get_profit_or_loss, outputs=pnl_out)
            hold_btn.click(get_holdings_report, outputs=hold_out)
            hist_btn.click(get_transaction_history, outputs=hist_out)

    demo.launch()
