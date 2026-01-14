from data_loader import DataLoader
from processor import DataProcessor
from strategy import AIStrategy
from risk_manager import RiskManager
from executor import Executor

def run_bot():
    # 1. Setup Modules
    loader = DataLoader()
    processor = DataProcessor()
    brain = AIStrategy()
    risk = RiskManager(stop_loss_pct=0.01, take_profit_pct=0.02)
    trade_bot = Executor() # Will use 'PAPER' mode from .env

    # 2. Get Market Data & Context
    raw_data = loader.fetch_ohlcv(limit=200)
    df = processor.add_indicators(raw_data)
    
    # Get current wallet balance from exchange
    balance = trade_bot.exchange.fetch_balance()
    usdt_balance = balance.get('USDT', {}).get('free', 1000) # Fallback to 1000 for testing

    # 3. AI Brain Decision
    if brain.train(df):
        latest_row = df.tail(1)
        current_price = latest_row['close'].values[0]
        prediction = brain.predict(latest_row, ['RSI', 'EMA_20', 'EMA_50', 'volume'])
        
        # 4. Risk Check
        can_trade, amount_to_spend = risk.validate_trade(prediction, usdt_balance)
        
        if can_trade:
            # 5. LIVE (or Paper) EXECUTION
            trade_bot.place_buy_order('BTC/USDT', amount_to_spend)
            
            stop_loss, take_profit = risk.get_trade_exit_levels(current_price)
            print(f"📍 Strategy exit targets set: SL: {stop_loss} | TP: {take_profit}")
        else:
            print("\n😴 AI says Wait or Risk conditions not met.")

if __name__ == "__main__":
    run_bot()