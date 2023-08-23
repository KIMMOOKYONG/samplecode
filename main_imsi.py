import talib
import plotly.graph_objects as go
import matplotlib
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
    data = pd.read_csv(uploaded_file, parse_dates=[0])
    data.set_index("Date", inplace=True)

    bt_strategy = bt.Strategy('EMA_crossover',
                                [   bt.algos.RunWeekly(),
                                    bt.algos.WeighTarget(signal),
                                    bt.algos.Rebalance()
                                ]
                             )

    bt_backtest = bt.Backtest(bt_strategy, stock_data['Close'].to_frame())
    bt_result = bt.run(bt_backtest)
    fig = bt_result.plot(title='Backtest result (Equity Progression)')
    st.pyplot(fig.figure)
