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

# 데이터 기본 정보 출력
st.header("데이터 미리보기")
st.write(data.head())

# 생존 여부 그래프
st.header("생존 여부 그래프")
survived_counts = data["Survived"].value_counts()
st.bar_chart(survived_counts)

# 성별 생존 비율 그래프
st.header("성별 생존 비율 그래프")
gender_survived = data.groupby("Sex")["Survived"].value_counts().unstack()
st.write(gender_survived.plot(kind="pie", subplots=True))

# 등급별 생존 비율 그래프
st.header("등급별 생존 비율 그래프")
class_survived = data.groupby("Pclass")["Survived"].value_counts().unstack()
st.bar_chart(class_survived)

# 나이 분포 히스토그램
st.header("나이 분포 히스토그램")
st.write(sns.histplot(data["Age"], bins=20, kde=True))

# 등급 및 성별 생존 비율 그래프
st.header("등급 및 성별 생존 비율 그래프")
class_gender_survived = data.groupby(["Pclass", "Sex"])["Survived"].value_counts().unstack()
st.write(class_gender_survived.plot(kind="bar", stacked=True))

# 시각화 개선과 커스터마이징
plt.figure(figsize=(10, 6))
sns.set_style("whitegrid")
sns.barplot(x="Pclass", y="Survived", hue="Sex", data=data, ci=None)
plt.xlabel("등급")
plt.ylabel("생존 비율")
plt.title("등급 및 성별 생존 비율")
plt.legend(title="성별")
st.pyplot(plt)
