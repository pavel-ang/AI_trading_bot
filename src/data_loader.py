import ccxt
import pandas as pd
from datetime import datetime

class DataLoader:
    def __init__(self, exchange_id='binance'):
        # Initialize the exchange connection
        self.exchange = getattr(ccxt, exchange_id)()
        
    def fetch_ohlcv(self, symbol='BTC/USDT', timeframe='1h', limit=100):
        """
        Fetches 'Open, High, Low, Close, Volume' data.
        """
        print(f"Fetching {limit} candles for {symbol} on {timeframe} timeframe...")
        
        # Fetch data from exchange
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        # Convert to a clean Pandas DataFrame
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Convert timestamp to human-readable date
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    # Add this method to your existing DataLoader class
    def download_historical_data(self, symbol, timeframe='1h', limit=1000):
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        filename = f"data/{symbol.replace('/', '_')}_history.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Saved {limit} candles for {symbol} to {filename}")
if __name__ == "__main__":
    # Quick test to see if it works
    loader = DataLoader()
    data = loader.fetch_ohlcv(limit=10)
    print(data.head())