import pandas as pd
import time
from strategy import AIStrategy
from processor import DataProcessor

class TimeMachine:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.current_step = 50  # Start with enough data for indicators

    def get_next_candle(self):
        """Simulates the passing of time by returning the next row."""
        if self.current_step < len(self.data):
            window = self.data.iloc[:self.current_step]
            self.current_step += 1
            return window
        return None

# To use this: 
# 1. Download BTC-USD, Gold (PAXG), and Silver data to CSVs.
# 2. Run this loop to feed your AIStrategy.