from socketserver import BaseRequestHandler
from time import time
from numpy import sqrt
import pandas as pd
import Binance
from talib import MA
import requests
import os 
from apscheduler.schedulers.blocking import BlockingScheduler

a = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'LTCUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'IOTAUSDT', 'XLMUSDT', 'TRXUSDT', 'ETCUSDT', 'VETUSDT', 'LINKUSDT', 'WAVESUSDT', 'ONGUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'IOSTUSDT', 'THETAUSDT', 'MATICUSDT', 'ATOMUSDT', 'FTMUSDT', 'ALGOUSDT', 'DOGEUSDT', 'DUSKUSDT', 'MTLUSDT', 'KEYUSDT', 'CHZUSDT', 'BEAMUSDT', 'HBARUSDT',  'STXUSDT', 'KAVAUSDT', 'BCHUSDT', 'FTTUSDT', 'BNTUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT', 'SOLUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'LRCUSDT', 'PNTUSDT', 'SNXUSDT', 'MKRUSDT', 'STORJUSDT', 'MANAUSDT', 'YFIUSDT', 'CRVUSDT', 'SANDUSDT', 'OCEANUSDT', 'NMRUSDT', 'DOTUSDT', 'LUNAUSDT', 'TRBUSDT', 'SUSHIUSDT', 'KSMUSDT', 'EGLDUSDT', 'RUNEUSDT', 'UNIUSDT',  'OXTUSDT', 'AVAXUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'AUDIOUSDT', 'AXSUSDT', 'UNFIUSDT', 'ROSEUSDT', 'XEMUSDT', 'SKLUSDT', 'GRTUSDT', '1INCHUSDT', 'CELOUSDT', 'RIFUSDT', 'LITUSDT', 'SFPUSDT', 'CAKEUSDT', 'BADGERUSDT', 'PERPUSDT', 'SUPERUSDT', 'CFXUSDT', 'BAKEUSDT', 'SHIBUSDT', 'ICPUSDT', 'MASKUSDT', 'LPTUSDT', 'XVGUSDT', 'BONDUSDT', 'C98USDT', 'QNTUSDT', 'FLOWUSDT', 'MINAUSDT', 'WAXPUSDT', 'DYDXUSDT', 'IDEXUSDT', 'GALAUSDT', 'ILVUSDT', 'AGLDUSDT', 'RADUSDT', 'AUCTIONUSDT', 'BNXUSDT', 'MOVRUSDT', 'ENSUSDT', 'POWRUSDT', 'JASMYUSDT',  'RNDRUSDT', 'HIGHUSDT', 'JOEUSDT', 'IMXUSDT', 'API3USDT', 'WOOUSDT', 'ASTRUSDT', 'GMTUSDT', 'APEUSDT', 'GALUSDT', 'LDOUSDT', 'OPUSDT', 'LUNCUSDT', 'GMXUSDT', 'POLYXUSDT', 'APTUSDT', 'OSMOUSDT', 'PHBUSDT', 'HOOKUSDT', 'MAGICUSDT', 'HIFIUSDT', 'SSVUSDT', 'AMBUSDT', 'GASUSDT', 'IDUSDT', 'ARBUSDT', 'LOOMUSDT', 'EDUUSDT', 'SUIUSDT', 'PEPEUSDT', 'FLOKIUSDT', 'SNTUSDT', 'COMBOUSDT', 'MAVUSDT', 'PENDLEUSDT', 'WLDUSDT', 'SEIUSDT', 'CYBERUSDT', 'NTRNUSDT', 'TIAUSDT', 'MEMEUSDT', 'ORDIUSDT', 'BLURUSDT', 'JTOUSDT', '1000SATSUSDT', 'BONKUSDT', 'ACEUSDT', 'NFPUSDT']
def Getdata (symbol):
    candles = Binance.client.get_klines(symbol=symbol, interval='15m', limit = 100)
    candles = pd.DataFrame(candles)
    candles =candles.drop(range(6, 12), axis=1)	
    col_names = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    candles.columns = col_names	
    for col in col_names:
        candles[col] = candles[col].astype(float)

    volume=candles['Volume']
    open=candles['Open']
    close=candles['Close']
    high=candles['High']
    low=candles['Low']

    MAvolume=MA(volume,10)
    #highest= MAX(close,30)
    #start MAvolume.iloc[-1]
    KLDotBien= volume.iloc[-2] > 3.5 * MAvolume.iloc[-2] or volume.iloc[-2] > 3.5 * MAvolume.iloc[-6] or volume.iloc[-2] > 3.5 * MAvolume.iloc[-7]
    GiaDotBien = close.iloc[-2] > open.iloc [-2]*1.015
    marubozu =  close.iloc[-2] > open.iloc[-2]*1.007 and high.iloc[-2] <close.iloc[-2]*1.0025 and open.iloc[-2]<low.iloc[-2]*1.0025 and volume.iloc[-2]> 5*MAvolume.iloc[-2]
    
    if KLDotBien == True and GiaDotBien == True:
        bot_token ='6546761370:AAFKtwkBxJ_3NyGP8CVVHd1J132mlWyg-zI'
        bot_chatID = '-4042951589'
        send_text = 'https://api.telegram.org/bot'+ bot_token + '/sendMessage?chat_id='+ bot_chatID + \
            '&text=' + symbol + '  KL+gia dot bien' + '   close=' + str(close.iloc[-2]) +  '   sl3%=' + str(close.iloc[-2]*0.97) + '    tp3%=' + str(close.iloc[-2]*1.03)  


        response = requests.get(send_text)
    
    if marubozu == True or close.iloc[-2]>0:
        bot_token ='6546761370:AAFKtwkBxJ_3NyGP8CVVHd1J132mlWyg-zI'
        bot_chatID = '-4042951589'
        send_text1 = 'https://api.telegram.org/bot'+ bot_token + '/sendMessage?chat_id='+ bot_chatID + \
            '&text=' + symbol + '  marubozu'+ '   close=' + str(close.iloc[-2]) +  '   sl3%=' + str(close.iloc[-2]*0.97) + '    tp3%=' + str(close.iloc[-2]*1.03)  
        send_text2 = 'https://api.telegram.org/bot'+ bot_token + '/sendMessage?chat_id='+ bot_chatID + \
           '&text=' + '/chart ' + symbol+ ' m15'

        response = requests.get(send_text1)
        response = requests.get(send_text2)
    
def run():
    print('run')
    i=0
    while (i<len(a)):
        try:
            symbol=a[i]
            Getdata(symbol)
            #khaosatgia(symbol)

            i=i+1

        except Exception as e:
            print('Error occured while trying: {}'.format(e))
            i=i+1
        continue
run()

#sched = BlockingScheduler()
#sched.add_job(run, 'cron', day_of_week='mon-fri', hour='0-23', minute='0,15,30,45', second='02')

#sched.start()
