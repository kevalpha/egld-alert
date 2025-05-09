import yfinance as yf
from prophet import Prophet
import telegram
import os
import time

INTERVAL_VERIFICARE = 3600  # verifică la fiecare oră

TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']
bot = telegram.Bot(token=TOKEN)

cripto_monede = {
    "EGLD": "EGLD-USD",
    "PEPE": "PEPE-USD",
    "FLOKI": "FLOKI-USD",
    "BONK": "BONK-USD"
}

def trimite_alerta(mesaj):
    bot.send_message(chat_id=CHAT_ID, text=mesaj)

def prezice_si_anunță(nume, simbol):
    try:
        df = yf.download(simbol, period="180d")
        df = df.rename(columns={"Date": "ds", "Close": "y"})

        if df.empty or len(df) < 30:
            print(f"Date insuficiente pentru {nume}")
            return

        model = Prophet(daily_seasonality=True)
        model.fit(df)

        viitor = model.make_future_dataframe(periods=1)
        prognoza = model.predict(viitor)

        pret_actual = df["y"].iloc[-1]
        pret_viitor = prognoza["yhat"].iloc[-1]
        variatie = ((pret_viitor - pret_actual) / pret_actual) * 100

        if abs(variatie) >= 30:
            directie = "CRESCUT" if variatie > 0 else "SCĂZUT"
            mesaj = f"[ALERTĂ AI] {nume} ({simbol}) a {directie} cu {variatie:.2f}% în următoarele ore."
            trimite_alerta(mesaj)

    except Exception as e:
        print(f"Eroare la {nume}: {e}")

def main():
    while True:
        for nume,