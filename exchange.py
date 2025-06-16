
import ccxt

class Exchange:
    def __init__(self, config):
        self.exchange = getattr(ccxt, config["exchange"])({
            "apiKey": config["apiKey"],
            "secret": config["apiSecret"],
            "enableRateLimit": True
        })

    def fetch_ohlcv(self, symbol, timeframe="1h", limit=100):
        return self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

    def create_order(self, symbol, side, amount):
        return self.exchange.create_market_order(symbol, side, amount)
