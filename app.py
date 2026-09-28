import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# 1. PENGATURAN HALAMAN
# =========================================================

st.set_page_config(
    page_title="LQ45 AI Trading Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# 2. MEMBACA DATA EXCEL
# =========================================================

try:
    df = pd.read_excel("AI_Ranking.xlsx")
except FileNotFoundError:
    st.error(
        "File AI_Ranking.xlsx tidak ditemukan. "
        "Pastikan file tersebut sudah berada di repository GitHub."
    )
    st.stop()

# =========================================================
# 3. MERAPIKAN DATA
# =========================================================

# Hilangkan spasi yang mungkin terdapat pada nama kolom
df.columns = df.columns.astype(str).str.strip()

# Pastikan kolom penting tersedia
kolom_wajib = ["Ticker", "Close", "Probability"]

kolom_hilang = [
    kolom for kolom in kolom_wajib
    if kolom not in df.columns
]

if kolom_hilang:
    st.error(
        "Kolom berikut tidak ditemukan di AI_Ranking.xlsx: "
        + ", ".join(kolom_hilang)
    )

    st.write("Kolom yang tersedia dalam file:")
    st.write(df.columns.tolist())

    st.stop()

# Ubah kolom angka menjadi numerik
kolom_angka = [
    "Close",
    "Probability",
    "IHSG",
    "Return_1D",
    "Momentum20",
    "Momentum60",
    "RSI14",
    "MACD",
    "Volume"
]

for kolom in kolom_angka:
    if kolom in df.columns:
        df[kolom] = pd.to_numeric(
            df[kolom],
            errors="coerce"
        )

# Ubah Probability ke skala 0 sampai 1 apabila masih berupa persen
if df["Probability"].dropna().max() > 1:
    df["Probability"] = df["Probability"] / 100

# =========================================================
# 4. MEMBUAT REKOMENDASI ANALISIS
# =========================================================

df["Recommendation"] = "HOLD"

df.loc[
    df["Probability"] >= 0.70,
    "Recommendation"
] = "BUY"

df.loc[
    df["Probability"] <= 0.40,
    "Recommendation"
] = "SELL"

# =========================================================
# 5. SIDEBAR
# =========================================================

st.sidebar.title("LQ45 AI Trading")

menu = st.sidebar.selectbox(
    "Pilih Menu",
    [
        "Market Overview",
        "AI Ranking",
        "Analisis Saham",
        "Portfolio Builder"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Dashboard ini merupakan alat bantu analisis dan bukan "
    "rekomendasi investasi personal."
)

# =========================================================
# 6. MENU 1: MARKET OVERVIEW
# =========================================================

if menu == "Market Overview":

    st.title("📊 Market Overview")

    st.write(
        "Ringkasan kondisi saham berdasarkan data terbaru "
        "dalam file AI_Ranking.xlsx."
    )

    # -----------------------------------------------------
    # A. INFORMASI TANGGAL DATA
    # -----------------------------------------------------

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

        tanggal_terakhir = df["Date"].max()

        if pd.notna(tanggal_terakhir):
            st.info(
                "Tanggal data terakhir: "
                + tanggal_terakhir.strftime("%d %B %Y")
            )

    # -----------------------------------------------------
    # B. METRIK UTAMA
    # -----------------------------------------------------

    jumlah_saham = df["Ticker"].nunique()

    jumlah_buy = (
        df["Recommendation"] == "BUY"
    ).sum()

    jumlah_hold = (
        df["Recommendation"] == "HOLD"
    ).sum()

    jumlah_sell = (
        df["Recommendation"] == "SELL"
    ).sum()

    kolom1, kolom2, kolom3, kolom4 = st.columns(4)

    kolom1.metric(
        label="Jumlah Saham",
        value=int(jumlah_saham)
    )

    kolom2.metric(
        label="Sinyal BUY",
        value=int(jumlah_buy)
    )

    kolom3.metric(
        label="Sinyal HOLD",
        value=int(jumlah_hold)
    )

    kolom4.metric(
        label="Sinyal SELL",
        value=int(jumlah_sell)
    )

    st.divider()
    # =====================================================
    # DIAGNOSTIK DISTRIBUSI PROBABILITY
    # =====================================================

    st.subheader("Diagnostik Probability Model")

    probability_min = df["Probability"].min()
    probability_rata_rata = df["Probability"].mean()
    probability_median = df["Probability"].median()
    probability_max = df["Probability"].max()

    d1, d2, d3, d4 = st.columns(4)

    d1.metric(
        "Probability Minimum",
        f"{probability_min * 100:.2f}%"
    )

    d2.metric(
        "Probability Rata-rata",
        f"{probability_rata_rata * 100:.2f}%"
    )

    d3.metric(
        "Probability Median",
        f"{probability_median * 100:.2f}%"
    )

    d4.metric(
        "Probability Maksimum",
        f"{probability_max * 100:.2f}%"
    )

    grafik_distribusi = px.histogram(
        df,
        x="Probability",
        nbins=10,
        title="Distribusi Probability Seluruh Saham",
        labels={
            "Probability": "Probability"
        }
    )

    grafik_distribusi.update_xaxes(
        tickformat=".0%"
    )

    grafik_distribusi.update_layout(
        yaxis_title="Jumlah Saham"
    )

    st.plotly_chart(
        grafik_distribusi,
        use_container_width=True
    )  
    # -----------------------------------------------------
    # C. NILAI IHSG
    # -----------------------------------------------------

    if "IHSG" in df.columns:

        data_ihsg = df["IHSG"].dropna()

        if not data_ihsg.empty:

            nilai_ihsg = data_ihsg.iloc[-1]

            st.metric(
                label="Nilai IHSG dalam Database",
                value=f"{nilai_ihsg:,.2f}"
            )

        else:
            st.warning(
                "Kolom IHSG tersedia tetapi tidak memiliki nilai."
            )

    else:
        st.info(
            "Nilai IHSG belum ditampilkan karena kolom IHSG "
            "tidak ditemukan di AI_Ranking.xlsx."
        )

    st.divider()

    # -----------------------------------------------------
    # D. GRAFIK KOMPOSISI SINYAL
    # -----------------------------------------------------

    st.subheader("Komposisi Sinyal AI")

    komposisi = pd.DataFrame({
        "Sinyal": ["BUY", "HOLD", "SELL"],
        "Jumlah": [
            int(jumlah_buy),
            int(jumlah_hold),
            int(jumlah_sell)
        ]
    })

    warna_sinyal = {
        "BUY": "#00A86B",
        "HOLD": "#F4B400",
        "SELL": "#D93025"
    }

    grafik_sinyal = px.bar(
        komposisi,
        x="Sinyal",
        y="Jumlah",
        color="Sinyal",
        color_discrete_map=warna_sinyal,
        text="Jumlah",
        title="Jumlah Saham Berdasarkan Sinyal AI"
    )

    grafik_sinyal.update_layout(
        showlegend=False,
        xaxis_title="Sinyal",
        yaxis_title="Jumlah Saham"
    )

    st.plotly_chart(
        grafik_sinyal,
        use_container_width=True
    )

    # -----------------------------------------------------
    # E. TOP 10 PROBABILITY
    # -----------------------------------------------------

    st.subheader("Top 10 Probability")

    top10 = (
        df.sort_values(
            by="Probability",
            ascending=False
        )
        .head(10)
        .copy()
    )

    top10["Probability (%)"] = (
        top10["Probability"] * 100
    ).round(2)

    kolom_tampilan = [
        "Ticker",
        "Close",
        "Probability (%)",
        "Recommendation"
    ]

    tambahan = [
        "RSI14",
        "Momentum20",
        "MACD"
    ]

    for kolom in tambahan:
        if kolom in top10.columns:
            kolom_tampilan.append(kolom)

    st.dataframe(
        top10[kolom_tampilan],
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # F. GRAFIK TOP 10
    # -----------------------------------------------------

    grafik_top10 = px.bar(
        top10,
        x="Ticker",
        y="Probability (%)",
        color="Recommendation",
        color_discrete_map=warna_sinyal,
        text="Probability (%)",
        title="10 Saham dengan Probability Tertinggi"
    )

    grafik_top10.update_layout(
        xaxis_title="Ticker",
        yaxis_title="Probability (%)"
    )

    st.plotly_chart(
        grafik_top10,
        use_container_width=True
    )

    # -----------------------------------------------------
    # G. INTERPRETASI
    # -----------------------------------------------------
    # =====================================================
    # 10 SAHAM DENGAN PROBABILITY TERENDAH
    # =====================================================

    st.divider()

    st.subheader("10 Probability Terendah")

    st.write(
        "Tabel ini membantu melihat saham yang dinilai "
        "paling lemah oleh model AI."
    )

    bottom10 = (
        df.sort_values(
            by="Probability",
            ascending=True
        )
        .head(10)
        .copy()
    )

    bottom10["Probability (%)"] = (
        bottom10["Probability"] * 100
    ).round(2)

    kolom_bottom = [
        "Ticker",
        "Close",
        "Probability (%)",
        "Recommendation"
    ]

    for kolom in [
        "RSI14",
        "Momentum20",
        "MACD"
    ]:
        if kolom in bottom10.columns:
            kolom_bottom.append(kolom)

    st.dataframe(
        bottom10[kolom_bottom],
        use_container_width=True,
        hide_index=True
    )

    grafik_bottom10 = px.bar(
        bottom10,
        x="Ticker",
        y="Probability (%)",
        color="Recommendation",
        color_discrete_map=warna_sinyal,
        text="Probability (%)",
        title="10 Saham dengan Probability Terendah"
    )

    grafik_bottom10.update_layout(
        xaxis_title="Ticker",
        yaxis_title="Probability (%)"
    )

    st.plotly_chart(
        grafik_bottom10,
        use_container_width=True
    )
        # =====================================================
    # SELURUH HASIL AI
    # =====================================================

    st.divider()

    st.subheader("Seluruh Hasil AI")

    semua_hasil = (
        df.sort_values(
            by="Probability",
            ascending=False
        )
        .copy()
    )

    semua_hasil["Probability (%)"] = (
        semua_hasil["Probability"] * 100
    ).round(2)

    kolom_semua = [
        "Ticker",
        "Close",
        "Probability (%)",
        "Recommendation"
    ]

    for kolom in [
        "RSI14",
        "Momentum20",
        "Momentum60",
        "MACD"
    ]:
        if kolom in semua_hasil.columns:
            kolom_semua.append(kolom)

    st.dataframe(
        semua_hasil[kolom_semua],
        use_container_width=True,
        hide_index=True
    )
    st.subheader("Panduan Interpretasi")

    st.write(
        """
        - **BUY**: probability AI minimal 70%.
        - **HOLD**: probability AI di atas 40% dan di bawah 70%.
        - **SELL**: probability AI maksimal 40%.
        - Probability bukan jaminan harga akan naik atau turun.
        - Sinyal perlu diuji melalui backtesting sebelum dipakai
          sebagai dasar transaksi dengan dana nyata.
        """
    )

# =========================================================
# 7. MENU 2: AI RANKING
# =========================================================

elif menu == "AI Ranking":

    st.title("🏆 AI Ranking")

    ranking = df.sort_values(
        by="Probability",
        ascending=False
    ).copy()

    ranking["Probability (%)"] = (
        ranking["Probability"] * 100
    ).round(2)

    kolom_ranking = [
        "Ticker",
        "Close",
        "Probability (%)",
        "Recommendation"
    ]

    for kolom in ["RSI14", "Momentum20", "Momentum60", "MACD"]:
        if kolom in ranking.columns:
            kolom_ranking.append(kolom)

    st.dataframe(
        ranking[kolom_ranking],
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# 8. MENU 3: ANALISIS SAHAM
# =========================================================

elif menu == "Analisis Saham":

    st.title("📈 Analisis Saham")

    ticker_pilihan = st.selectbox(
        "Pilih saham",
        sorted(df["Ticker"].dropna().unique())
    )

    detail = df[
        df["Ticker"] == ticker_pilihan
    ].copy()

    if not detail.empty:

        data_terbaru = detail.iloc[0]

        probability_persen = (
            float(data_terbaru["Probability"]) * 100
        )

        kolom1, kolom2, kolom3 = st.columns(3)

        kolom1.metric(
            "Harga",
            f"Rp {data_terbaru['Close']:,.0f}"
        )

        kolom2.metric(
            "Probability",
            f"{probability_persen:.2f}%"
        )

        kolom3.metric(
            "Sinyal",
            data_terbaru["Recommendation"]
        )

        st.dataframe(
            detail,
            use_container_width=True,
            hide_index=True
        )

# =========================================================
# 9. MENU 4: PORTFOLIO BUILDER
# =========================================================

elif menu == "Portfolio Builder":

    st.title("💰 Portfolio Builder")

    modal = st.number_input(
        "Masukkan modal investasi",
        min_value=1000000,
        value=100000000,
        step=1000000
    )

    jumlah_pilihan = st.slider(
        "Jumlah saham dalam portofolio",
        min_value=3,
        max_value=10,
        value=5
    )

    kandidat = (
        df[df["Recommendation"] == "BUY"]
        .sort_values(
            by="Probability",
            ascending=False
        )
        .head(jumlah_pilihan)
        .copy()
    )

    if kandidat.empty:

        st.warning(
            "Belum terdapat saham dengan sinyal BUY."
        )

    else:

        kandidat["Bobot (%)"] = (
            100 / len(kandidat)
        )

        kandidat["Alokasi (Rp)"] = (
            modal / len(kandidat)
        )

        kandidat["Estimasi Lot"] = (
            kandidat["Alokasi (Rp)"]
            / (kandidat["Close"] * 100)
        ).apply(
            lambda nilai: int(nilai)
        )

        kandidat["Nilai Pembelian (Rp)"] = (
            kandidat["Estimasi Lot"]
            * kandidat["Close"]
            * 100
        )

        kandidat["Probability (%)"] = (
            kandidat["Probability"] * 100
        ).round(2)

        st.dataframe(
            kandidat[
                [
                    "Ticker",
                    "Close",
                    "Probability (%)",
                    "Bobot (%)",
                    "Alokasi (Rp)",
                    "Estimasi Lot",
                    "Nilai Pembelian (Rp)"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Perhitungan menggunakan 1 lot = 100 saham dan "
            "belum memperhitungkan biaya broker."
        )
    # =====================================================
    # KESIMPULAN OTOMATIS
    # =====================================================

    st.subheader("Kesimpulan Sinyal Hari Ini")

    saham_buy = df[
        df["Recommendation"] == "BUY"
    ].copy()

    saham_hold = df[
        df["Recommendation"] == "HOLD"
    ].copy()

    saham_sell = df[
        df["Recommendation"] == "SELL"
    ].copy()

    if not saham_buy.empty:

        daftar_buy = ", ".join(
            saham_buy["Ticker"].astype(str).tolist()
        )

        st.success(
            "Terdapat "
            + str(len(saham_buy))
            + " saham dengan sinyal BUY: "
            + daftar_buy
        )

    else:

        st.warning(
            "Belum terdapat saham yang mencapai batas BUY "
            "sebesar 70%."
        )

    if not saham_sell.empty:

        daftar_sell = ", ".join(
            saham_sell["Ticker"].astype(str).tolist()
        )

        st.error(
            "Terdapat "
            + str(len(saham_sell))
            + " saham dengan sinyal SELL: "
            + daftar_sell
        )

    else:

        st.info(
            "Belum terdapat saham yang mencapai batas SELL "
            "sebesar 40% atau lebih rendah."
        )

    st.write(
        "Jumlah saham HOLD:",
        len(saham_hold)
    )
