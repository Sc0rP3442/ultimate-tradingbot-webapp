
def log_trade(symbol, action, amount, price):
    with open("trades.log", "a") as f:
        f.write(f"{symbol},{action},{amount},{price}\n")
