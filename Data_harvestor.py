import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import logging

class DataHarvester:
    """Extracts historical market data from MT5 and formats it for analysis."""

    @staticmethod
    def get_historical_data(symbol: str, timeframe: int, num_candles: int) -> pd.DataFrame:
        """
        Fetches historical OHLCV data.
        
        :param symbol: e.g., "EURUSD"
        :param timeframe: e.g., mt5.TIMEFRAME_H1
        :param num_candles: Number of bars to retrieve
        :return: pandas DataFrame with datetime index
        """
        logging.info(f"Fetching {num_candles} candles for {symbol}...")
        
        # Request data from MT5
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
        
        if rates is None or len(rates) == 0:
            logging.error(f"Failed to fetch data for {symbol}. Check symbol name and connection.")
            return pd.DataFrame()

        # Convert to Pandas DataFrame
        df = pd.DataFrame(rates)
        
        # Convert timestamp to human-readable datetime
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        
        # Keep only the columns we care about
        df = df[['open', 'high', 'low', 'close', 'tick_volume']]
        df.rename(columns={'tick_volume': 'volume'}, inplace=True)
        
        logging.info(f"Successfully loaded {len(df)} rows for {symbol}.")
        return df

# Example usage if run directly:
if __name__ == "__main__":
    mt5.initialize()
    # Fetch 1000 Hourly candles for EURUSD
    df_data = DataHarvester.get_historical_data("EURUSD", mt5.TIMEFRAME_H1, 1000)
    print(df_data.head())
    mt5.shutdown()