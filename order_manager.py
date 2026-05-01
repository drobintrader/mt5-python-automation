import MetaTrader5 as mt5
import logging

class OrderManager:
    """Handles the execution of market orders, including SL/TP management."""

    @staticmethod
    def send_market_order(symbol: str, order_type: int, lot_size: float, slippage: int = 10, magic_number: int = 123456) -> bool:
        """
        Sends a basic market buy or sell order.
        
        :param symbol: e.g., "GBPUSD"
        :param order_type: mt5.ORDER_TYPE_BUY or mt5.ORDER_TYPE_SELL
        :param lot_size: e.g., 0.1
        :return: True if successful, False otherwise
        """
        # Ensure symbol is visible in Market Watch
        if not mt5.symbol_select(symbol, True):
            logging.error(f"Symbol {symbol} not found or not visible.")
            return False

        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logging.error(f"Failed to get info for {symbol}.")
            return False

        # Determine price based on order type
        price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid

        # Construct the MT5 request dictionary
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(lot_size),
            "type": order_type,
            "price": price,
            "slippage": slippage,
            "magic": magic_number,
            "comment": "Python Algo Execution",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC, # Standard for most brokers
        }

        # Send the order
        logging.info(f"Sending {'BUY' if order_type == mt5.ORDER_TYPE_BUY else 'SELL'} order for {symbol} ({lot_size} lots)...")
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Order failed. Retcode: {result.retcode}. Error: {result.comment}")
            return False
            
        logging.info(f"Order filled successfully! Ticket: {result.order}")
        return True