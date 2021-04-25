class Indicators:

    def __init__(self, frame, window_short, window_long, signal_day):
        self.frame = frame
        self.window_short = window_short
        self.window_long = window_long
        self.signal_day = signal_day

    def sma_short(self):
        return self.frame.rolling(window=self.window_short).mean().values.tolist()

    def sma_long(self):
        return self.frame.rolling(window=self.window_long).mean().values.tolist()

    def ema_short(self):
        return self.frame.ewm(span=self.window_short, adjust=True).mean().values.tolist()

    def ema_long(self):
        return self.frame.ewm(span=self.window_long, adjust=True).mean().values.tolist()

    def MACD_Diver(self):
        import talib
        macd, signal_line, hist= talib.MACD(self.frame, fastperiod= self.window_short, slowperiod = self.window_long, signalperiod = self.signal_day)
        return [macd, signal_line, hist]

    def RSI(self, time:int):
        import talib
        rsi = talib.RSI(self.frame, timeperiod = time)
        return rsi.values.tolist()


'''
    def genrate_dataframe(self):
        import pandas as pd
        data = self.frame.values
        date = self.frame.index
        df = pd.DataFrame(data, date)
        return df

    def Signal_line(self):
        import numpy as np
        k = 2 / self.signal_day + 1

        self.frame['Signal'] = np.zeros(len(self.frame.index))
        self.frame['Signal'].iloc[0] = self.MACD()[0]

        for t in range(1, len(self.frame.Signal)):
            self.frame['Signal'].iloc[t] = (self.MACD()[t] * k) + (self.frame.Signal[t - 1] * (1 - k))
        Signal = self.frame['Signal'].values.ravel()
        return Signal
'''


