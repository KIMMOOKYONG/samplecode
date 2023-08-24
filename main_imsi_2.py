# import the necessary Python packages
import pandas_ta as ta
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting import Backtest
import yfinance as yf
import pandas as pd

import streamlit as st
import time

def load_price_data(symbol, period, interval):
    data = yf.download(tickers=symbol, period=period, interval=interval)
    df = pd.DataFrame(data)

    return df

def EMA(df_in, window):
    df = df_in.copy()
    ema_series = ta.ema(df['Close'], length=window)
    return ema_series


class EmaCrossoverStrategy(Strategy):
    ema1_len = 10
    ema2_len = 50
    def init(self):
        super().init()
        # Add indicators
        self.ema1 = self.I(EMA, self.data.df, self.ema1_len)
        self.ema2 = self.I(EMA, self.data.df, self.ema2_len)
    def next(self):
        super().init()
        price = self.data.Close[-1]
        # Long entry
        if (not self.position) and crossover(self.ema1, self.ema2):
            #  Buy
            self.position.close()
            self.buy()
        # Long exit
        elif self.position and crossover(self.ema2, self.ema1):
            # Close any existing long trades, and sell the asset
            self.position.close()
            self.sell()

def run_backtest(df):
    # If exclusive orders (each new order auto-closes previous orders/position),
    # cancel all non-contingent orders and close all open trades beforehand
    bt = Backtest(df, EmaCrossoverStrategy, cash=10000, commission=.00075, trade_on_close=True, exclusive_orders=True, hedging=False)
    stats = bt.run()
    df = pd.DataFrame(stats, columns=["VAL"])
    df = df.transpose()
    df.rename(columns=df.iloc[0], inplace=True) # 행열이 전환된 데이터프레임의 열 이름 제대로 수정
    df = df.drop(df.index[0])
    st.dataframe(df)

    st.bokeh_chart(bt.plot())
    st.write(stats["Sortino Ratio"])


st.set_page_config(layout="wide")

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")

#  Download data
symbol = 'ETH-USD'
#  valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
period = '1mo'
#  valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
interval = '15m'
df = load_price_data(symbol, period, interval)
run_backtest(df)

