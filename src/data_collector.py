import yfinance as yf
import os

def download_data():
    # Assets: BTC, Gold (GC=F), Silver (SI=F)
    assets = {
        "BTC": "BTC-USD",
        "GOLD": "GC=F",
        "SILVER": "SI=F"
    }
    
    os.makedirs('data', exist_ok=True)
    
    for name, ticker in assets.items():
        print(f"Downloading historical data for {name}...")
        # Fetching 7 days of 5-minute data for a detailed test
        data = yf.download(ticker, period="7d", interval="5m")
        data.to_csv(f"data/{name.lower()}_history.csv")
        print(f"✅ Saved {len(data)} rows for {name}.")

if __name__ == "__main__":
    download_data()