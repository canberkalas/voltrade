import time
from binance.client import Client
from binance.enums import *
import talib

# API anahtarlarınızı girin
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# Bağlantıyı başlatın
client = Client(api_key, api_secret, tld='com')

def get_stochrsi(pair, interval, stoch_length, rsi_length, k, d):
    """Stochastic RSI hesaplaması"""
    klines = client.futures_klines(symbol=pair, interval=interval, limit=stoch_length+rsi_length)

    closes = [float(x[4]) for x in klines]
    rsi = talib.RSI(np.array(closes), timeperiod=rsi_length)
    stochrsi = talib.STOCHRSI(np.array(closes), timeperiod=stoch_length, fastk_period=k, fastd_period=d)

    return rsi, stochrsi

def check_entry_exit(pair, interval, stoch_length, rsi_length, k, d, leverage, position_size, stop_loss, take_profit):
    """Stratejiyi uygula"""

    # Pozisyonu kontrol et
    positions = client.futures_position_information(symbol=pair)
    for p in positions:
        if p['symbol'] == pair:
            if float(p['positionAmt']) > 0:
                # Long pozisyon
                print('Long pozisyonu kontrol ediliyor.')
                if float(p['unRealizedProfit']) / float(p['positionInitialMargin']) > take_profit:
                    # Kar al
                    print('Kar al.')
                    client.futures_create_order(symbol=pair, side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=abs(float(p['positionAmt'])))
                    return
                elif float(p['unRealizedProfit']) / float(p['positionInitialMargin']) < stop_loss:
                    # Zarar durdur
                    print('Zarar durdur.')
                    client.futures_create_order(symbol=pair, side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=abs(float(p['positionAmt'])))
                    return
            elif float(p['positionAmt']) < 0:
                # Short pozisyon
                print('Short pozisyonu kontrol ediliyor.')
                if float(p['unRealizedProfit']) / float(p['positionInitialMargin']) > take_profit:
                    # Kar al
                    print('Kar al.')
                    client.futures_create_order(symbol=pair, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=abs(float(p['positionAmt'])))
                    return
                elif float(p['unRealizedProfit']) / float(p['positionInitialMargin']) < stop_loss:
                    # Zarar durdur
                    print('Zarar durdur.')
                    client.futures_create_order(symbol=pair, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=abs(float(p['positionAmt'])))
                    return

   # Stochastic RSI'ı kontrol et
def check_stoch_rsi(symbol):
    # Kline verilerini al
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR)

    # Son 14 kapanış fiyatını al
    closes = [float(entry[4]) for entry in klines[-14:]]

    # Stochastic RSI hesapla
    rsi = ta.momentum.StochRSIIndicator(np.array(closes)).stochrsi()

    # Son RSI değerini al
    current_rsi = rsi[-1]

    # Kline verilerini al
    klines = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE)

    # Son kapanış fiyatını al
    current_price = float(klines[-1][4])

    # K ve D çizgisini hesapla
    fastk, fastd = ta.momentum.StochasticOscillator(high=np.array([float(entry[2]) for entry in klines]),
                                                    low=np.array([float(entry[3]) for entry in klines]),
                                                    close=np.array([float(entry[4]) for entry in klines])).stoch()
    # Son K ve D değerlerini al
    current_k, current_d = fastk[-1], fastd[-1]

    return current_price, current_rsi, current_k, current_d
