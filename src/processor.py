import pandas_ta as ta

class DataProcessor:
    @staticmethod
    def add_indicators(df):
        # FIX: Force all columns to lowercase so 'Close' becomes 'close'
        df.columns = [col.lower() for col in df.columns]
        
        # Now these will work without KeyError
        df['rsi'] = ta.rsi(df['close'], length=14)
        df['ema_20'] = ta.ema(df['close'], length=20)
        df['ema_50'] = ta.ema(df['close'], length=50)
        
        # Drop rows where indicators couldn't calculate (first 50 rows)
        return df.dropna()