import pandas as pd
import numpy as np

class TechnicalIndicators:
    """Calculates technical indicators using vectorized pandas operations for speed."""

    @staticmethod
    def add_sma(df: pd.DataFrame, period: int, column: str = 'close') -> pd.DataFrame:
        """
        Calculates the Simple Moving Average (SMA).
        """
        df[f'SMA_{period}'] = df[column].rolling(window=period).mean()
        return df

    @staticmethod
    def add_rsi(df: pd.DataFrame, period: int = 14, column: str = 'close') -> pd.DataFrame:
        """
        Calculates the Relative Strength Index (RSI).
        """
        delta = df[column].diff()
        
        # Separate gains and losses
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        
        # Calculate Exponential Moving Average of gains/losses
        avg_gain = pd.Series(gain).ewm(alpha=1/period, min_periods=period).mean()
        avg_loss = pd.Series(loss).ewm(alpha=1/period, min_periods=period).mean()
        
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Align index
        df['RSI'].index = df.index
        return df