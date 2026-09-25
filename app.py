import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# CONFIG
# ======================

st.set_page_config(
    page_title="LQ45 AI Trading",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================

df = pd.read_excel("AI_Ranking.xlsx")

# ======================
# SIDEBAR
# ======================

menu = st.sidebar.selectbox(
    "Pilih Menu",
    [
        "Market Overview",
        "AI Ranking",
        "Analisis Saham",
        "Portfolio Builder"
    ]
)

# ======================
# MENU 1
# ======================

if menu == "Market Overview":

    st.title("📊 Market Overview")

    st.write("Ringkasan kondisi market saat ini")

    jumlah_saham = len(df)

    st.metric(
        "Jumlah Saham",
        jumlah_saham
    )

# ======================
# MENU 2
# ======================

elif menu == "AI Ranking":

    st.title("🏆 AI Ranking")

    ranking = df.sort_values(
        "Probability",
        ascending=False
    )

    st.dataframe(
        ranking,
        use_container_width=True
    )

    top20 = ranking.head(20)

    fig = px.bar(
        top20,
        x="Ticker",
        y="Probability",
        color="Probability"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ======================
# MENU 3
# ======================

elif menu == "Analisis Saham":

    st.title("📈 Analisis Saham")

    ticker = st.selectbox(
        "Pilih Saham",
        sorted(df["Ticker"].unique())
    )

    detail = df[
        df["Ticker"] == ticker
    ]

    st.dataframe(detail)

# ======================
# MENU 4
# ======================

elif menu == "Portfolio Builder":

    st.title("💰 Portfolio Builder")

    modal = st.number_input(
        "Masukkan Modal",
        value=100000000
    )

    st.write(
        f"Modal Anda : Rp {modal:,.0f}"
    )

    top5 = df.head(5)

    alokasi = modal / 5

    hasil = pd.DataFrame({
        "Ticker": top5["Ticker"],
        "Alokasi": alokasi
    })

    st.dataframe(hasil)
