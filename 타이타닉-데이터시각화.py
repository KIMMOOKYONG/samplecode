import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 타이타닉 생존자 데이터셋 불러오기
@st.cache_data
def load_data():
    url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
    data = pd.read_csv(url)
    return data

# 스트림릿 앱 생성
st.title("타이타닉 생존자 데이터 시각화")

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

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    colors = ["skyblue", "salmon"]

    for idx, col in enumerate(gender_survived.columns):
        ax = axes[idx]
        ax.pie(gender_survived[col], labels=gender_survived.index, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title("Survival" if col == 1 else "Death")

    st.pyplot(fig)
elif category == "등급":
    st.header("등급별 생존 비율 그래프")
    class_survived = data.groupby("Pclass")["Survived"].value_counts().unstack()
    st.bar_chart(class_survived)
elif category == "나이 분포":
    st.header("나이 분포 히스토그램")
    fig = sns.histplot(data["Age"], bins=20, kde=True)
    st.pyplot(fig.figure)

# 시각화 개선과 커스터마이징
if category == "등급":
    fig = plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.barplot(x="Pclass", y="Survived", hue="Sex", data=data, ci=None)
    plt.xlabel("Class")
    plt.ylabel("Survival rate")
    plt.title("Survival rates by grade and gender")
    plt.legend(title="Gender")
    st.pyplot(fig)
