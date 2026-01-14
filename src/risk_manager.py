class RiskManager:
    def __init__(self, stop_loss_pct=0.02, take_profit_pct=0.04, risk_per_trade=0.1):
        """
        :param stop_loss_pct: Sell if price drops 2%
        :param take_profit_pct: Sell if price rises 4%
        :param risk_per_trade: Use 10% of total balance per trade
        """
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.risk_per_trade = risk_per_trade

    def calculate_position_size(self, total_balance):
        # Calculates how much USD/USDT to spend on this one trade
        return total_balance * self.risk_per_trade

    def get_trade_exit_levels(self, entry_price, side='BUY'):
        if side == 'BUY':
            stop_loss = entry_price * (1 - self.stop_loss_pct)
            take_profit = entry_price * (1 + self.take_profit_pct)
        else:
            # For short selling (optional later)
            stop_loss = entry_price * (1 + self.stop_loss_pct)
            take_profit = entry_price * (1 - self.take_profit_pct)
            
        return stop_loss, take_profit

    def validate_trade(self, prediction, current_balance, min_trade_size=10):
        """
        Checks if we have enough money to actually execute the AI's decision.
        """
        position_size = self.calculate_position_size(current_balance)
        
        if prediction == 1 and position_size >= min_trade_size:
            return True, position_size
        return False, 0