
import streamlit as st
import pandas as pd

df = pd.read_excel("AI_Ranking.xlsx")

st.title("LQ45 AI Trading Dashboard")

st.dataframe(df)

st.bar_chart(
    df.set_index("Ticker")["Probability"]
)
