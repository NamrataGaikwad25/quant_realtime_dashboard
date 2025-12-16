import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from ingest import run_ingestion
from database import get_connection
from analytics.stats import resample_data
from analytics.regression import hedge_ratio
from analytics.stationarity import adf_test
from utils.config import SYMBOLS

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="QuantEdge | Real-Time Pair Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- GLOBAL STYLE --------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
}
.status-bar {
    background: #020617;
    padding: 10px;
    border-left: 5px solid #22c55e;
    border-radius: 8px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- START INGESTION --------------------
run_ingestion(SYMBOLS)

# -------------------- HEADER --------------------
st.markdown("""
## QuantEdge — Real-Time Statistical Arbitrage Dashboard  
<span style="color:#94a3b8;font-size:14px;">
Simple live pair analytics for spread & mean-reversion analysis
</span>
""", unsafe_allow_html=True)

st.markdown(
    "<div class='status-bar'>System running • Streaming live market data</div>",
    unsafe_allow_html=True
)

# -------------------- SIDEBAR --------------------
st.sidebar.header("Strategy Parameters")

symbols = ["BTCUSDT", "ETHUSDT"]
symbol1 = st.sidebar.selectbox("Primary Asset", symbols)
symbol2 = st.sidebar.selectbox(
    "Hedge Asset", [s for s in symbols if s != symbol1]
)

timeframe = st.sidebar.selectbox("Resample Timeframe", ["1s", "1m", "5m"])
window = st.sidebar.slider("Rolling Window", 20, 200, 50)
z_thresh = st.sidebar.slider("Z-Score Threshold", 1.0, 3.0, 2.0)

st.sidebar.markdown("---")
st.sidebar.caption("OLS regression • Z-Score • ADF stationarity")

# -------------------- LOAD DATA --------------------
@st.cache_data(ttl=1)
def load_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM ticks", conn)
    conn.close()
    return df

df = load_data()

if len(df) < 100:
    st.warning("Waiting for sufficient live market data...")
    st.stop()

df1 = df[df["symbol"] == symbol1]
df2 = df[df["symbol"] == symbol2]

r1 = resample_data(df1.copy(), timeframe)
r2 = resample_data(df2.copy(), timeframe)

merged = pd.merge(
    r1, r2,
    left_index=True,
    right_index=True,
    suffixes=("_1", "_2")
)

# -------------------- ANALYTICS --------------------
beta = hedge_ratio(merged["price_1"], merged["price_2"])

if pd.isna(beta):
    st.warning("Not enough data to compute hedge ratio")
    st.stop()

spread = merged["price_1"] - beta * merged["price_2"]
spread_mean = spread.rolling(window).mean()
spread_std = spread.rolling(window).std()

zscore = (spread - spread_mean) / spread_std
zscore = zscore.dropna()

if len(zscore) < 5:
    st.warning("Rolling analytics warming up...")
    st.stop()

adf_result = adf_test(spread)
stationary = adf_result["p-value"] < 0.05

# -------------------- METRICS --------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Hedge Ratio (β)", f"{beta:.4f}")
c2.metric("Latest Z-Score", f"{zscore.iloc[-1]:.2f}")
c3.metric("ADF p-value", f"{adf_result['p-value']:.4f}")
c4.metric(
    "Market Regime",
    "MEAN-REVERTING" if stationary else "TRENDING"
)

if abs(zscore.iloc[-1]) > z_thresh:
    st.error("Z-Score Extreme — Potential Entry Signal")

# -------------------- TABS --------------------
tab1, tab2, tab3 = st.tabs([
    "Price Action",
    "Spread & Z-Score",
    "Export Data"
])

# -------------------- TAB 1: SIMPLE PRICE GRAPH --------------------
with tab1:
    st.subheader("Price Movement Comparison")

    fig_price = px.line(
        merged,
        y=["price_1", "price_2"],
        labels={
            "value": "Price",
            "variable": "Asset"
        }
    )

    fig_price.update_layout(height=400)
    st.plotly_chart(fig_price, use_container_width=True)

# -------------------- TAB 2: SIMPLE SPREAD + Z-SCORE --------------------
with tab2:
    st.subheader("Spread Between Assets")

    fig_spread = px.line(
        spread,
        labels={"value": "Spread", "index": "Time"},
        title="Price Spread"
    )

    fig_spread.update_layout(height=350)
    st.plotly_chart(fig_spread, use_container_width=True)

    st.subheader("Z-Score Indicator")

    fig_z = px.line(
        zscore,
        labels={"value": "Z-Score", "index": "Time"},
        title="Z-Score Over Time"
    )

    fig_z.add_hline(y=z_thresh, line_dash="dash")
    fig_z.add_hline(y=-z_thresh, line_dash="dash")

    fig_z.update_layout(height=350)
    st.plotly_chart(fig_z, use_container_width=True)

# -------------------- TAB 3: EXPORT --------------------
with tab3:
    st.write("Download processed analytics data")
    st.download_button(
        "Download CSV",
        merged.assign(
            spread=spread,
            zscore=zscore
        ).to_csv().encode(),
        file_name="quantedge_analytics.csv"
    )

st.caption("QuantEdge • Clean, simple & research-ready pair analytics")
