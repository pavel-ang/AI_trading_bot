import sqlite3
import pandas as pd

def show_results():
    conn = sqlite3.connect('data/local_simulation.db')
    
    # 1. View Wallet Balance
    wallet = pd.read_sql_query("SELECT * FROM wallet", conn)
    print("\n--- CURRENT WALLET ---")
    print(wallet)
    
    # 2. View Trade History
    trades = pd.read_sql_query("SELECT * FROM trade_history", conn)
    print("\n--- RECENT TRADES ---")
    if trades.empty:
        print("No trades executed yet.")
    else:
        print(trades.tail(10)) # Show last 10 trades
        
        # Calculate simple win rate if profit is logged
        if 'profit' in trades.columns:
            wins = len(trades[trades['profit'] > 0])
            total = len(trades)
            print(f"\nWin Rate: {(wins/total)*100:.2f}%")

    conn.close()

if __name__ == "__main__":
    show_results()