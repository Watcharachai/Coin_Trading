from flask import Flask, render_template, request, flash, redirect, jsonify
import config as iKey
from binance.client import Client
from binance.enums import  *
from datetime import date, timedelta

app = Flask(__name__)
app.secret_key = iKey.api_secret
client = Client(iKey.api_key, iKey.api_secret,tld=iKey.tld)

@app.route('/')
def find_Cypto():
    title = 'CoinViewer'
    account = client.get_account()
    balances = account['balances']
    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']
    return render_template('CyptoViewer.html', title=title, my_balances=balances, symbols=symbols)


@app.route('/buy', methods=['POST'])
def buy():
    print(request.form)
    try:
        order = client.create_order(symbol=request.form['symbol'],
                                    side=SIDE_BUY,
                                    type=ORDER_TYPE_MARKET,
                                    quantity=request.form['quantity'])
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/sell')
def sell():
    return 'sell'

@app.route('/settings')
def settings():
    return 'settings'

@app.route('/history')
def history():
    symbol = "BTCUSDT"
    today = date.today()
    start_date = today - timedelta(day=200)
    start_date = start_date.strftime("%d/%B/%Y")
    try:
        candles = client.get_historical_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE,start_str=start_date ,limit = 400)
        '''
        time_list = ['1m', '5m', '15m', '30m', '1h', '1d']
        time = '1m'   
        if time == '1m':
            candles = client.get_historical_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit = 400)
        elif time == '5m':
            candles = client.get_historical_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=400)
        elif time == '15m':
            candles = client.get_historical_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE,limit = 400)
        elif time == '30m':
            candles = client.get_historical_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_30MINUTE,limit=400)
        elif time == '1h':
            candles = client.get_historical_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR,limit=400)
        elif time == '1d':
            candles = client.get_historical_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1DAY,limit=400)
        else:
            print("Invalid Timeframe")
            time = input()
            '''
    except (TypeError,ValueError) as e:
        print(e)

    process_candles = []
    for data in candles:
        candle = {
            "time": data[0]/1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }
        process_candles.append(candle)

    return jsonify(process_candles)

