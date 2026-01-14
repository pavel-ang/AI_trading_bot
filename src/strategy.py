import pandas as pd
from sklearn.ensemble import RandomForestClassifier

class AIStrategy:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        
    def prepare_data(self, df):
        # Predict if next close is higher than current
        df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
        
        # Must match the names in processor.py
        features = ['rsi', 'ema_20', 'ema_50', 'volume']
        X = df[features].iloc[:-1]
        y = df['target'].iloc[:-1]
        
        return X, y, features

    def train(self, df):
        X, y, features = self.prepare_data(df)
        if len(X) < 20: return False
        self.model.fit(X, y)
        return True

    def predict(self, latest_row, features):
        # Reshape ensures the AI can process a single row of data
        X_input = latest_row[features].values.reshape(1, -1)
        return self.model.predict(X_input)[0]