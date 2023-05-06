from binance.client import Client
import ta
import numpy as np
import time
import requests
import json
import time
import hmac
import hashlib
import urllib.parse
import pandas as pd
import numpy as np
import ccxt
import ta.momentum
from talib import STOCHRSI

exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': 'your_secret_key',
    'enableRateLimit': True,
})

symbol = 'BTC/USDT'
amount = 50
leverage = 5
order_type = 'market'

exchange.futures_create_order(symbol, order_type, 'buy', amount, {'leverage': leverage})
exchange.futures_create_order(symbol, order_type, 'sell', amount, {'leverage': leverage})

client = Client(api_key, api_secret)

period = 11
smooth_k = 2
smooth_d = 2

def get_last_price():
#Mevcut fiyat bilgisini alırMevcut fiyat bilgisini alır
ticker = exchange.fetch_ticker(symbol)
return ticker['last']

def get_open_positions():
#Mevcut açık pozisyonları alır
positions = exchange.futures_private_get_positionrisk({'symbol': symbol})
return positions

def open_long_position(last_price):
#Uzun pozisyon açar
stop_loss = last_price * 0.98
take_profit = last_price * 1.02
exchange.futures_create_order(symbol, 'market', 'buy', amount, {'stopPrice': stop_loss, 'reduceOnly': False, 'takeProfitPrice': take_profit})

def open_short_position(last_price):
#Kısa pozisyon açar
stop_loss = last_price * 1.02
take_profit = last_price * 0.98
exchange.futures_create_order(symbol, 'market', 'sell', amount, {'stopPrice': stop_loss, 'reduceOnly': False, 'takeProfitPrice': take_profit})

def close_position(position_id):
#Pozisyonu kapatır
exchange.futures_create_order(symbol, 'market', 'buy' if position['positionAmt'] < 0 else 'sell', abs(position['positionAmt']), {'reduceOnly': True})

def check_trade_signals():
#Fiyat bilgisini alıyoruz
klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=period+1)
closes = np.array([float(kline[4]) for kline in klines])

#Stoch RSI indikatörünü hesaplıyoruz
stoch_rsi = ta.momentum.StochRSIIndicator(closes, window=period, smooth_k=smooth_k, smooth_d=smooth_d)
k = stoch_rsi.stochrsi_k()
d = stoch_rsi.stochrsi_d()

#K çizgisini ve D çizgisini hesaplayın
k_line, d_line = stoch_rsi()

#En son fiyatı alın
last_price = get_last_price()

#Mevcut pozisyonları kontrol edin
open_positions = get_open_positions()

#Stoch RSI değeri 80'in üzerinde ve K çizgisi D çizgisinin altına düştüyse kısa pozisyon açın
if k_line[-1] < d_line[-1] and k_line[-2] >= d_line[-2] and k_line[-1] > 80:
    if "short" not in open_positions:
        open_short_position(last_price)

#Stoch RSI değeri 20'nin altında ve K çizgisi D çizgisinin üstüne çıktığında uzun pozisyon açın
elif k_line[-1] > d_line[-1] and k_line[-2] <= d_line[-2] and k_line[-1] < 20:
    if "long" not in open_positions:
        open_long_position(last_price)

#Mevcut pozisyonları kapatın
for position in open_positions:
    position_type = position["position_type"]
    position_price = position["entry_price"]
    position_size = position["size"]
    position_stop_loss = position["stop_loss"]
    position_take_profit = position["take_profit"]
    position_id = position["position_id"]
    
    # Kar al seviyesine ulaşıldıysa pozisyonu kapat
    if last_price >= position_take_profit and position_type == "long":
        close_position(position_id)
    elif last_price <= position_take_profit and position_type == "short":
        close_position(position_id)
        
    # Stop loss seviyesine ulaşıldıysa pozisyonu kapat
    elif last_price <= position_stop_loss and position_type == "long":
        close_position(position_id)
    elif last_price >= position_stop_loss and position_type == "short":
        close_position(position_id)

#Açık pozisyonları kontrol edin
open_positions = exchange.futures_private_get_positionrisk({'symbol': symbol})

for position in open_positions:
    if position['positionAmt'] > 0 and float(position['unRealizedProfit']) > amount * 0.013:
        exchange.futures_create_order(symbol, 'market', 'sell', position['positionAmt'], {'reduceOnly': True})
    
    if position['positionAmt'] > 0 and float(position['unRealizedProfit']) < -amount * 0.0043:
        exchange.futures_create_order(symbol, 'market', 'sell', position['positionAmt'], {'reduceOnly': True})
