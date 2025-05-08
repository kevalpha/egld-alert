import yfinance as yf
import pandas as pd
from prophet import Prophet
from telegram import Bot
import time
import os

# Configurare variabile din mediu
TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']
INTERVAL_VERIFICARE = 86400  # o dată pe zi

bot = Bot(token=TOKEN)

cripto_monede = {
    'EGLD': 'EGLD-USD',
    'PEPE': 'PEPE-USD',
    'FLOKI': 'FLOKI-USD',
    'BONK': 'BONK-USD'
}

def trimite_alerta(mesaj):
    bot.send_message(chat_id=CHAT_ID, text=mesaj)

def prezice_si_avertizeaza(nume, simbol):
    try:
        df = yf.download(simbol, period="180d")[['Close']].reset_index()
        df.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)

        if df.empty or len(df) < 30:
            print(f"Date insuficiente pentru {nume}")
            return

        model = Prophet(daily_seasonality=True)
        model.fit(df)

        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        pret_actual = df['y'].iloc[-1]
        pret_viitor = forecast['yhat'].iloc[-1]
        variatie = ((pret_viitor - pret_actual) / pret_actual) * 100

        if abs(variatie) >= 30:
            directie = "CRESCUT" if variatie > 0 else "SCĂZUT"
            mesaj = (f"[AI ALERTĂ] {nume} ({simbol}) ar putea {directie} "
                     f"cu {variatie:.2f}% în următoarele 30 zile!")
            trimite_alerta(mesaj)

    except Exception as e:
        print(f"Eroare la {nume}: {e}")

# Rulare zilnică
while True:
    for nume, simbol in cripto_monede.items():
        prezice_si_avertizeaza(nume, simbol)
    time.sleep(INTERVAL_VERIFICARE)
