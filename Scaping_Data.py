import requests  # for making http requests to binance
import json  # for parsing what binance sends back to us
import pandas as pd  # for storing and manipulating the data we get back
import numpy as np  # numerical python, i usually need this somewhere
import matplotlib.pyplot as plt  # for charts and such
import datetime as dt  # for dealing with times

# Pull data
def get_bars(symbol, interval):
    root_url = 'https://api.binance.com/api/v1/klines'
    url = root_url + '?symbol=' + symbol + '&interval=' + interval
    data = json.loads(requests.get(url).text)
    df = pd.DataFrame(data)
    df.columns = ['open_time',
                  'Open', 'High', 'Low', 'Close', 'Volume',
                  'close_time', 'qav', 'num_trades',
                  'taker_base_vol', 'taker_quote_vol', 'ignore']
    df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.close_time]
    df.drop(['open_time', 'close_time'], axis=1, inplace=True)
    for col in df.columns:
        df[col] = df[col].astype(float)
    return df

def choose_coin(symbol:str, interval:str):
    coins = get_bars(symbol, interval)
    return coins
#sym = 'ETHBUSD' #ethbusd = get_bars(sym, '1d')

#Insert Char to make a data
char = input('Insert Coins securities ticker:')
sym = choose_coin(char, '1d')

#Reshape Dataframe, choosing only Close price and apply with an indicator
from Indicator import Indicators
myIndicators = Indicators(sym.Close, 12, 26, 9) #Setting up Indicators

# Reshape Dataframe to Stat_frame for back testing (Setting Indicators)
#mydf = myIndicators.genrate_dataframe()
date = sym.index
col = ['Close','short_EMA','long_EMA']
price = sym.Close.values.tolist() #price data

#Indicators
Short_EMA = myIndicators.ema_short()
Long_EMA = myIndicators.ema_long()
macd = myIndicators.MACD_Diver()[0]
signal_line = myIndicators.MACD_Diver()[1]
hist = myIndicators.MACD_Diver()[2]
rsi = myIndicators.RSI(time=14)

#Plotting
data = [price, Short_EMA, Long_EMA]
d= dict(zip(col,data))
mydf = pd.DataFrame(data =d, index= date)
#Plotting data normally
plt.figure(figsize=(8, 5))
mydf.plot()
plt.title(f"Daily Price of {char} with Indicators", fontsize=16)
plt.ylabel("USD", fontsize=12)
plt.legend()
plt.show()

#Ploting Data with density of EMA
plt.figure(figsize=(8, 5))
ax2 = mydf.Close.plot(label = 'Closed Price')
ax2.fill_between(mydf.index,mydf.short_EMA, mydf.long_EMA ,color = 'k',alpha=0.5)
plt.title(f"Daily Price of {char} with Density", fontsize=16)
plt.ylabel("USD", fontsize=12)
plt.legend()
plt.show()