
import pandas as pd
import talib
import numpy as np
import tensorflow as tf

class StrategyManager:
    def __init__(self, config):
        self.config = config
        self.model = tf.keras.models.load_model("ai_model.h5")

    def evaluate(self, data, symbol):
        df = pd.DataFrame(data, columns=["ts", "o", "h", "l", "c", "v"])
        close = df["c"]
        rsi = talib.RSI(close, timeperiod=14)
        macd, _, _ = talib.MACD(close)

        if rsi.iloc[-1] < 30 and macd.iloc[-1] > macd.iloc[-2]:
            X = close[-60:].values.reshape(1, 60, 1)
            pred = self.model.predict(X)[0][0]
            if pred > 0.6:
                return {"action": "buy", "amount": self.config["trade_amount"]}
        elif rsi.iloc[-1] > 70 and macd.iloc[-1] < macd.iloc[-2]:
            return {"action": "sell", "amount": self.config["trade_amount"]}
        return None
