import pandas as pd
import os
from strategy import AIStrategy
from processor import DataProcessor
from risk_manager import RiskManager
from executor import LocalExecutor

def run_backtest(asset_name):
    brain = AIStrategy()
    processor = DataProcessor()
    risk = RiskManager()
    local_exec = LocalExecutor()
    
    file_path = f"data/{asset_name.lower()}_history.csv"
    if not os.path.exists(file_path):
        print(f"❌ Missing data for {asset_name}")
        return

    # Load and Process
    df = pd.read_csv(file_path)
    df = processor.add_indicators(df)

    # Split: Train on first 70%, Test on last 30%
    split = int(len(df) * 0.7)
    train_df = df.iloc[:split]
    test_df = df.iloc[split:]

    if brain.train(train_df):
        print(f"✅ AI Trained for {asset_name}. Simulating {len(test_df)} steps...")
        features = ['rsi', 'ema_20', 'ema_50', 'volume']
        
        for i in range(len(test_df)):
            latest_row = test_df.iloc[[i]]
            prediction = brain.predict(latest_row, features)
            
            if prediction == 1:
                price = latest_row['close'].values[0]
                balance = local_exec.get_local_balance()
                can_trade, amount = risk.validate_trade(prediction, balance)
                
                if can_trade:
                    local_exec.execute_local_buy(asset_name, amount, price)

if __name__ == "__main__":
    for asset in ["BTC", "GOLD", "SILVER"]:
        run_backtest(asset)