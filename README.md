
# QuantEdge — Real-Time Pairs Trading Analytics Dashboard

QuantEdge is a real-time quantitative analytics application designed to demonstrate end-to-end system design for statistical arbitrage research. The application ingests live tick data from Binance WebSocket streams, stores and resamples it, computes key quantitative analytics, and presents results through an interactive dashboard.

This project was built as part of a **Quant Developer Evaluation Assignment**, with emphasis on modularity, extensibility, and clarity of design rather than production-scale optimization.

---

## 🎯 Objective

Design and implement a complete analytical pipeline that covers:

* Real-time market data ingestion
* Storage and resampling
* Quantitative analytics for pair trading
* Interactive visualization and alerting

The system is designed to resemble a prototype analytics stack used by quantitative research and trading teams.

---

## 🚀 Key Features

### 🔹 Real-Time Data Ingestion

* Live tick data ingestion from **Binance WebSocket**
* Captures timestamp, symbol, price, and quantity
* Designed to support alternate feeds (REST, CSV, futures) with minimal changes

### 🔹 Data Storage & Sampling

* Local **SQLite** database for persistence
* Resampling into configurable timeframes:

  * `1s`, `1m`, `5m`
* Rolling window-based analytics

### 🔹 Quantitative Analytics

* Hedge ratio estimation using **OLS regression**
* Spread computation between asset pairs
* Rolling **Z-score**
* **Augmented Dickey-Fuller (ADF)** stationarity test
* Rolling correlation (extensible)
* Alerting on Z-score thresholds (e.g., |z| > 2)

### 🔹 Interactive Dashboard

* Built using **Streamlit** and **Plotly**
* Live price charts with zoom, pan, hover
* Spread & Z-score visualization
* Summary statistics and alerts
* CSV export of processed analytics

---

## 🧠 System Architecture

The application follows a modular architecture where each component is loosely coupled and independently extendable.

![Architecture Diagram](quant%20architecture.png)

---

## 🏗 Architecture Design Rationale

* **Loose coupling** between ingestion, storage, analytics, and UI layers
* Analytics modules are isolated for easy extension
* Storage layer can be swapped (SQLite → Redis / PostgreSQL)
* Frontend updates analytics selectively based on data availability

This architecture allows:

* Plugging in new data sources
* Adding new analytics without breaking existing logic
* Scaling individual components independently

---

## 📂 Project Structure

```text
quant_realtime_dashboard/
│
├── analytics/
│   ├── stats.py            # Resampling, rolling statistics
│   ├── regression.py       # Hedge ratio via OLS
│   ├── stationarity.py     # ADF test
│
├── data/
│   └── ticks.db            # SQLite database storing tick data
│
├── utils/
│   └── config.py           # Global configuration (symbols, params)
│
├── ingest.py               # WebSocket ingestion pipeline
├── database.py             # Database connection & persistence
├── app.py                  # Streamlit dashboard
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ▶️ How to Run the Application

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/NamrataGaikwad25/quant_realtime_dashboard.git
cd quant_realtime_dashboard
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the App

```bash
streamlit run app.py
```

The dashboard will start locally and begin ingesting live market data automatically.

---

## 🔔 Alerts & Live Analytics

* Z-score alerts trigger when user-defined thresholds are breached
* Analytics are enabled dynamically once sufficient data points are available
* Resampled plots update according to their respective timeframes

---

## 📥 Data Export

* Users can download processed analytics (prices, spread, z-score) as CSV
* Enables offline analysis and research workflows

---

## 🤖 ChatGPT Usage Disclosure

ChatGPT was used for:

* Debugging Streamlit behavior
* Structuring modular analytics components
* Improving architecture clarity
* Drafting documentation and README structure

All implementation decisions, integrations, and validations were performed by the author.

---

## ⚠️ Notes & Limitations

* This is a **research-grade prototype**, not production infrastructure
* No analytics requiring more than intraday data are used
* Focus is on clarity, extensibility, and correctness over optimization

---

## 👩‍💻 Author

**Namrata Gaikwad**
Computer Engineering Student
Vishwakarma Institute of Technology, Pune

* GitHub: [https://github.com/NamrataGaikwad25](https://github.com/NamrataGaikwad25)
* LinkedIn: [https://www.linkedin.com/in/namrata-gaikwad-5039152a1/](https://www.linkedin.com/in/namrata-gaikwad-5039152a1/)

---

