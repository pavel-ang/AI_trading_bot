import sqlite3
from datetime import datetime

class LocalExecutor:
    def __init__(self, db_path='data/backtest.db'):
        self.db_path = db_path

    def get_local_balance(self):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT balance_usdt FROM wallet").fetchone()[0]

    def execute_local_buy(self, symbol, amount_usd, current_price):
        balance = self.get_local_balance()
        if balance < amount_usd:
            return False, "Insufficient local funds"

        new_balance = balance - amount_usd
        with sqlite3.connect(self.db_path) as conn:
            # Update balance
            conn.execute("UPDATE wallet SET balance_usdt = ?", (new_balance,))
            # Log trade
            conn.execute("INSERT INTO trades (timestamp, side, price, amount) VALUES (?, ?, ?, ?)",
                         (datetime.now(), 'BUY', current_price, amount_usd))
        
        print(f"💰 LOCAL TRADE: Bought {symbol} at ${current_price}. New Balance: ${new_balance:.2f}")
        return True, "Success"