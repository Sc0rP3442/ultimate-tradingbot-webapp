
def apply_risk_management(entry_price, current_price, config):
    change = (current_price - entry_price) / entry_price
    if change <= -config["max_loss"]:
        return "stop_loss"
    elif change >= config["take_profit"]:
        return "take_profit"
    return "hold"
