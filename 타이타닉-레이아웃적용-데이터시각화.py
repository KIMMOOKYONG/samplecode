import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 타이타닉 생존자 데이터셋 불러오기
@st.cache
def load_data():
    url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
    data = pd.read_csv(url)
    return data

# 스트림릿 앱 생성
st.title("타이타닉 생존자 데이터 시각화")

# 레이아웃 함수 정의
def set_layout():
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")

# 데이터 불러오기
data = load_data()

# 사이드바를 통해 카테고리 선택
category = st.sidebar.selectbox("카테고리 선택", ["생존 여부", "성별", "등급", "나이 분포"])

# 선택한 카테고리에 따라 시각화
if category == "생존 여부":
    st.header("생존 여부 그래프")
    survived_counts = data["Survived"].value_counts()
    st.bar_chart(survived_counts)
elif category == "성별":
    st.header("성별 생존 비율 그래프")
    gender_survived = data.groupby("Sex")["Survived"].value_counts().unstack()

    set_layout()
    for idx, col in enumerate(gender_survived.columns):
        plt.subplot(1, 2, idx + 1)
        plt.pie(gender_survived[col], labels=gender_survived.index, colors=["skyblue", "salmon"], autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title("생존" if col == 1 else "사망")

    st.pyplot()
elif category == "등급":
    st.header("등급별 생존 비율 그래프")
    class_survived = data.groupby("Pclass")["Survived"].value_counts().unstack()

    set_layout()
    sns.barplot(x="Pclass", y="Survived", hue="Sex", data=data, ci=None)
    plt.xlabel("등급")
    plt.ylabel("생존 비율")
    plt.title("등급 및 성별 생존 비율")
    plt.legend(title="성별")
    st.pyplot()
elif category == "나이 분포":
    st.header("나이 분포 히스토그램")
    set_layout()
    sns.histplot(data["Age"], bins=20, kde=True)
    plt.xlabel("나이")
    plt.ylabel("빈도")
    plt.title("나이 분포")
    st.pyplot()
