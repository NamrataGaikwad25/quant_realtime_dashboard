# Real-Time Quant Analytics Dashboard

## Overview
A real-time analytical dashboard that ingests Binance tick data, resamples it,
computes quantitative analytics, and visualizes insights live.

## Features
- Live WebSocket ingestion
- Multi-timeframe resampling
- Hedge ratio (OLS)
- Spread & Z-score
- ADF stationarity test
- Alerts
- CSV export

## Tech Stack
Python, Streamlit, Plotly, SQLite, Pandas

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
