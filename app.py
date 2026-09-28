import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="LQ45 AI Trading Dashboard",
    layout="wide"
)

st.title("📈 LQ45 AI Trading Dashboard")

# Load data
df = pd.read_excel("AI_Ranking.xlsx")

# Ranking Saham
st.header("Top Ranking Saham")

ranking = df.sort_values(
    "Probability",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True
)

# Grafik Top 20
st.header("Top 20 AI Probability")

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

# Detail saham
st.header("Detail Saham")

ticker = st.selectbox(
    "Pilih Ticker",
    ranking["Ticker"]
)

detail = ranking[
    ranking["Ticker"] == ticker
]

st.dataframe(detail)
