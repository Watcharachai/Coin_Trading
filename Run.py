import Scaping_Data as Var
from binance.client import Client
import config
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

client = Client(config.api_key, config.api_secret,tld = config.tld)

#ORDER @ MARKET// BUY and SELL
def PlaceBUY(amount, symbol):
    candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=1)
    close = candles[0][4]
    if float(close) * amount < 10:
        return print("NOT ENOUGHT MINIMUM PLACE ORDER")
    else:
        try:
            buy_limit = client.order_market_buy(
            symbol=symbol,
            quantity=str(amount))
            print("BUY COMPLETE")
            return buy_limit
        except BinanceAPIException as e:
            print(e)
        except BinanceOrderException as e:
        # error handling goes here
            print(e)

def PlaceSELL(symbol):
    n = 3
    trades = client.get_my_trades(symbol=symbol)
    while True:
        try:
            qty = float(trades[0]["qty"]) - float(trades[0]["commission"])
            qty = str(qty)[:n]
            client.order_market_sell(
                symbol=symbol,
                quantity=str(qty))
            # > 10USDT
            print("SELL COMPLETE")
            return
        except BinanceAPIException as e:
            n = n - 1
            # error handling goes here
            print(e)
        except BinanceOrderException as e:
            # error handling goes here
            print(e)
            pass

def PlaceCANCEL(buy_order):
    try:
        cancel = client.cancel_order(symbol=buy_order['symbol'], orderId = buy_order['orderId'] )
        return cancel
    except BinanceAPIException as e:
        print(e)
        pass


def Rule1(tickers, money:int):
    #Rule1 = Short<>Long
    Rule1_Buy = (Var.Short_EMA[-2] < Var.Long_EMA[-2]) and (Var.Short_EMA[-1] > Var.Long_EMA[-1])  # Bullish Cross
    Rule1_Sell = (Var.Short_EMA[-2] > Var.Long_EMA[-2]) and (Var.Short_EMA[-1] < Var.Long_EMA[-1])  # Bearish Cross

    # Oversold/Bought
    oversold = Var.rsi[-1] < 30
    overbought = Var.rsi[-1] > 70

    if oversold:
        print("{} OVERSOLD RSI < 30".format(tickers))
    elif overbought:
        print("{} OVERBOUGHT RSI > 70".format(tickers))
    else:
        print("{} MIDDLE 30 < RSI < 70".format(tickers))

    action_price = Var.price[-1]
    amount = round(money/action_price,2)

    if Rule1_Buy: return PlaceBUY(amount=amount,symbol=tickers)
    elif Rule1_Sell: return PlaceSELL(symbol=tickers)
    else: return "NONE"

def Rule2(tickers, money:int):
    pass

if __name__ == '__main__':
    r = Rule1(Var.char,int(input()))
    print(r)