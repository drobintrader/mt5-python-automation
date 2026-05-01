import time
import logging
import MetaTrader5 as mt5
from mt5_connect import MT5Connection
from data_harvester import DataHarvester
from order_manager import OrderManager
from indicators import TechnicalIndicators

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_trading_loop():
    """Main execution loop for the trading bot."""
    symbol = "EURUSD"
    timeframe = mt5.TIMEFRAME_H1
    lot_size = 0.1
    
    logging.info(f"Starting execution loop for {symbol}...")

    while True:
        try:
            # 1. Fetch latest data
            df = DataHarvester.get_historical_data(symbol, timeframe, 100)
            
            if not df.empty:
                # 2. Calculate Indicators
                df = TechnicalIndicators.add_rsi(df, period=14)
                latest_rsi = df['RSI'].iloc[-1]
                
                logging.info(f"Current {symbol} RSI: {latest_rsi:.2f}")

                # 3. Simple Strategy Logic (Example)
                if latest_rsi < 30:
                    logging.info("Oversold condition detected. Executing BUY...")
                    OrderManager.send_market_order(symbol, mt5.ORDER_TYPE_BUY, lot_size)
                    time.sleep(3600)  # Sleep for the candle duration
                    
                elif latest_rsi > 70:
                    logging.info("Overbought condition detected. Executing SELL...")
                    OrderManager.send_market_order(symbol, mt5.ORDER_TYPE_SELL, lot_size)
                    time.sleep(3600)

            # Wait before checking again (e.g., check every 1 minute)
            time.sleep(60)

        except KeyboardInterrupt:
            logging.info("Bot stopped by user.")
            break
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
            time.sleep(60) # Sleep before retrying to prevent spamming the broker

if __name__ == "__main__":
    if MT5Connection.initialize():
        run_trading_loop()
        MT5Connection.shutdown()