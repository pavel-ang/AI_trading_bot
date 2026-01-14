import sqlite3
import os

def init_db():
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/local_simulation.db')
    cursor = conn.cursor()

    # Wallet: Total USDT and amount of each asset held
    cursor.execute('''CREATE TABLE IF NOT EXISTS wallet 
                      (asset TEXT PRIMARY KEY, amount REAL)''')
    
    # Initialize with $1000 USDT
    cursor.execute("INSERT OR IGNORE INTO wallet (asset, amount) VALUES ('USDT', 1000.0)")

    # Trades: Log all simulated activities
    cursor.execute('''CREATE TABLE IF NOT EXISTS trade_history 
                      (id INTEGER PRIMARY KEY, timestamp DATETIME, 
                       symbol TEXT, side TEXT, price REAL, qty REAL, cost REAL)''')
    
    conn.commit()
    conn.close()
    print("✅ Simulated database ready at data/local_simulation.db")

if __name__ == "__main__":
    init_db()