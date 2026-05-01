import MetaTrader5 as mt5
import logging

# Configure professional logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MT5Connection:
    """Handles the connection and session management for MetaTrader 5."""

    @staticmethod
    def initialize() -> bool:
        """Initializes the MT5 terminal connection."""
        if not mt5.initialize():
            logging.error(f"MT5 Initialization failed. Error code: {mt5.last_error()}")
            return False
        
        logging.info("Successfully connected to MetaTrader 5.")
        return True

    @staticmethod
    def get_account_info() -> dict:
        """Retrieves and returns basic account information."""
        account_info = mt5.account_info()
        if account_info is None:
            logging.warning("Failed to retrieve account info.")
            return {}
        
        info_dict = {
            "login": account_info.login,
            "balance": account_info.balance,
            "equity": account_info.equity,
            "currency": account_info.currency,
            "leverage": account_info.leverage
        }
        logging.info(f"Account loaded. Balance: {info_dict['balance']} {info_dict['currency']}")
        return info_dict

    @staticmethod
    def shutdown():
        """Safely shuts down the MT5 connection."""
        mt5.shutdown()
        logging.info("MT5 connection closed gracefully.")

# Example usage if run directly:
if __name__ == "__main__":
    if MT5Connection.initialize():
        MT5Connection.get_account_info()
        MT5Connection.shutdown()