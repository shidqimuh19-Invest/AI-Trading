import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="LQ45 AI Trading Dashboard",
    layout="wide"
)

st.title("📈 LQ45 AI Trading Dashboard")

df = pd.read_excel("AI_Ranking.xlsx")

# Ranking
st.subheader("Top Ranking Saham")

ranking = df.sort_values(
    "Probability",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True
)

# Top 20 Chart
st.subheader("Top AI Probability")

top20 = ranking.head(20)

fig = px.bar(
    top20,
    x="Ticker",
    y="Probability",
    color="Probability",
    title="Top 20 Saham Berdasarkan AI Probability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Filter saham
st.subheader("Detail Saham")

ticker = st.selectbox(
    "Pilih Saham",
    ranking["Ticker"].unique()
)

detail = ranking[
    ranking["Ticker"] == ticker
]

st.dataframe(detail)
