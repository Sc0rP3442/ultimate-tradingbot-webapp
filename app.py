
import streamlit as st
import hashlib
import json
import os
from strategy import StrategyManager
from exchange import Exchange

USERS_FILE = "users.json"
ADMIN_KEY = "supersecureadminkey123"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def login_form():
    st.title("🔐 Login zum TradingBot")
    tab1, tab2 = st.tabs(["Login", "Registrieren"])

    with tab1:
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")
        if st.button("Einloggen"):
            users = load_users()
            if username in users and users[username] == hash_password(password):
                st.session_state["user"] = username
                st.rerun()
            else:
                st.error("❌ Ungültige Anmeldedaten")

    with tab2:
        new_user = st.text_input("Neuer Benutzername")
        new_pw = st.text_input("Neues Passwort", type="password")
        if st.button("Registrieren"):
            users = load_users()
            if new_user in users:
                st.error("Benutzername bereits vergeben")
            else:
                users[new_user] = hash_password(new_pw)
                save_users(users)
                st.success("✅ Registrierung erfolgreich – bitte einloggen")

def main_ui():
    st.title("📊 TradingBot Dashboard")

    if st.session_state["user"] == ADMIN_KEY:
        st.success("🔑 Admin-Modus aktiv")
        st.write("Gesamte Benutzerliste:")
        st.json(load_users())

    from config import config
    exchange = Exchange(config)
    strategy = StrategyManager(config)
    symbol = st.selectbox("Tradingpaar wählen:", config['symbols'])

    if st.button("Jetzt analysieren"):
        data = exchange.fetch_ohlcv(symbol)
        signal = strategy.evaluate(data, symbol)
        if signal:
            st.success(f"Signal: {signal['action'].upper()} {signal['amount']} {symbol}")
        else:
            st.warning("Kein klares Signal aktuell")

    st.markdown("---")
    if st.button("Logout"):
        del st.session_state["user"]
        st.rerun()

if __name__ == "__main__":
    if "user" not in st.session_state:
        login_form()
    else:
        main_ui()
