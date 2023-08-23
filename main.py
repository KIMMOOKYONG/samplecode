import talib
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import date
import bt 

import platform
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Linux':
    rc('font', family='NanumGothic')

# 스트림릿 앱 생성
st.title("데이터 프로파일링 실습")


#inputs from user
ticker = st.sidebar.text_input("Please enter a ticker symbol","SPY").upper()
days = st.sidebar.number_input("Please enter the number of days of data you would like",30)
strategy = st.sidebar.radio('Select Strategy', ['Single Moving Average','Moving Average Crossover'])

#filter moving average windows by strategy
if strategy == 'Single Moving Average':
    single_ma = st.sidebar.number_input("Please enter your moving average window",5)
    single_ma = [single_ma]
    strategy = 'Single Moving Average'
    window = single_ma
else:
    lma = st.sidebar.number_input("Please enter your long MA window",30)
    sma = st.sidebar.number_input("Please enter your short MA window",5)
    strategy = 'Crossover Moving Average'
    window = [sma,lma]


# 파일 업로드 위젯
uploaded_file = st.file_uploader("데이터 파일 업로드", type=["csv", "xlsx"])

if uploaded_file is not None:
    stock_data = pd.read_csv(uploaded_file)

    EMA_short = talib.EMA(stock_data['Close'], timeperiod=12).to_frame()

    EMA_short = EMA_short.rename(columns={0: 'Close'})
    EMA_long = talib.EMA(stock_data['Close'], timeperiod=50).to_frame()
    EMA_long = EMA_long.rename(columns={0: 'Close'})

    signal = EMA_long.copy()
    signal[EMA_long.isnull()] = 0
    signal[EMA_short > EMA_long] = 1
    signal[EMA_short < EMA_long] = -1

    transition = signal[signal['Close'].diff()!=0]
    buy_signal = transition[transition['Close'] == 1]
    sell_signal = transition[transition['Close'] == -1]

    long_index = buy_signal.index
    buy_position = stock_data[stock_data.index.isin(long_index)]
    short_index = sell_signal.index
    sell_position = stock_data[stock_data.index.isin(short_index)]

    fig = go.Figure()
    fig.add_trace(
            go.Candlestick(x=stock_data.index,
                    open=stock_data['Open'],
                    high=stock_data['High'],
                    low=stock_data['Low'],
                    close=stock_data['Close'],
                    name="Stock Prices"
                          )            
    )

    fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=EMA_long['Close'],
                name="EMA 50"
            )
    )

    fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=EMA_short['Close'],
                name = "EMA 12"
            )
    )

    fig.add_trace(
            go.Scatter(
                x=buy_position.index,
                y=buy_position['Close'], 
                name="Buy Signal",
                marker=dict(color="#511CFB", size=15),
                mode="markers",
                marker_symbol="triangle-up"
            )
    )

    fig.add_trace(
            go.Scatter(
                x=sell_position.index,
                y=sell_position['Close'], 
                name="Sell Signal",
                marker=dict(color="#750086", size=15),
                mode="markers",
                marker_symbol="triangle-down"
            )
    )

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title="Daily Close Prices",
        xaxis_title="Date",
        yaxis_title="Price (USD)"
    )

    st.plotly_chart(fig)
