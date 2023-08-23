import talib
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date
import bt 

import streamlit as st

ticker = "009150.KS"
today = date.today().strftime("%Y-%m-%d")
stock_data = yf.download(ticker, start="2020-1-1", end=today)
    
EMA_short = talib.EMA(stock_data["Close"], timeperiod=12).to_frame()
# 데이터 프레임으로 변환
EMA_short = EMA_short.rename(columns={0: "Close"})

EMA_long = talib.EMA(stock_data["Close"], timeperiod=50).to_frame()
# 데이터 프레임으로 변환
EMA_long = EMA_long.rename(columns={0: "Close"})

signal = EMA_long.copy()
# EMA_long에 값이 없으면 "0"으로 값 설정
signal[EMA_long.isnull()] = 0

signal[EMA_short > EMA_long] = 1
signal[EMA_short < EMA_long] = -1

# 매매 시그널의 값이 -1, 1로 전환되었는지 여부는 diff() 함수를 이용해서 판단한다.
transition = signal[signal["Close"].diff()!=0]
# 매수
buy_signal = transition[transition["Close"] == 1]
# 매도
sell_signal = transition[transition["Close"] == -1]

long_index = buy_signal.index
buy_position = stock_data[stock_data.index.isin(long_index)]
short_index = sell_signal.index
sell_position = stock_data[stock_data.index.isin(short_index)]

fig = go.Figure()
fig.add_trace(
        go.Candlestick(x=stock_data.index,
                open=stock_data["Open"],
                high=stock_data["High"],
                low=stock_data["Low"],
                close=stock_data["Close"],
                name="Stock Prices"
                      )            
)

fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=EMA_long["Close"],
            name="EMA 50"
        )
)

fig.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=EMA_short["Close"],
            name = "EMA 12"
        )
)

fig.add_trace(
        go.Scatter(
            x=buy_position.index,
            y=buy_position["Close"], 
            name="Buy Signal",
            marker=dict(color="#511CFB", size=15),
            mode="markers",
            marker_symbol="triangle-up"
        )
)

fig.add_trace(
        go.Scatter(
            x=sell_position.index,
            y=sell_position["Close"], 
            name="Sell Signal",
            marker=dict(color="#750086", size=15),
            mode="markers",
            marker_symbol="triangle-down"
        )
)

fig.update_layout(
    xaxis_rangeslider_visible=False,
    title="Daily Close (" + ticker + ") Prices",
    xaxis_title="Date",
    yaxis_title="Price (USD)"
)

st.plotly_chart(fig)


bt_strategy = bt.Strategy("EMA_crossover",
                            [   bt.algos.RunWeekly(),
                                bt.algos.WeighTarget(signal),
                                bt.algos.Rebalance()
                            ]
                         )

bt_backtest = bt.Backtest(bt_strategy, stock_data["Close"].to_frame())
bt_result = bt.run(bt_backtest)
res = bt_result.plot(title="Backtest result (Equity Progression)")
st.pyplot(res.figure)

res = bt_result.plot_histograms(bins=50, freq = 'w')
st.pyplot(res.figure)

res = bt_result.stats
st.write(res)
