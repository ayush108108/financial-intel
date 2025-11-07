# Financial Intelligence Platform

> **Intelligent financial data pipeline with real-time pair trading analysis. Detect statistical arbitrage opportunities via cointegration testing and correlation-based pair screening.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

---

## 🎯 What It Does

Financial Intelligence is a production-ready platform that:

- **Ingests real-time market data** from Yahoo Finance for stocks, ETFs, and crypto across global exchanges
- **Analyzes pair correlations** using Spearman/Pearson methods to find statistically linked assets
- **Detects cointegration** to identify mean-reversion trading opportunities (pairs that move together)
- **Computes rolling metrics** (volatility, beta, Sharpe ratio) for risk assessment
- **Factors analysis** to understand what drives each pair's behavior
- **Backtests strategies** on historical data with entry/exit signals
- **Exposes REST APIs** for real-time pair scoring and backtest results

Perfect for **algorithmic traders**, **fintech platforms**, **portfolio managers**, and **research teams** looking to systematically identify trading pairs.

---

## ⚡ Key Features

| Feature | Details |
|---------|---------|
| **Multi-Asset Support** | US stocks, ETFs, crypto (BTC, ETH), international markets (India NSE/BSE, Forex) |
| **Daily & Intraday Data** | Daily EOD + 4-hour candles with 20-year historical depth |
| **Correlation Matrix** | Fast Spearman/Pearson analysis across 100+ asset pairs daily |
| **Cointegration Testing** | Statistical significance testing (Engle-Granger, 2-step OLS) |
| **Rolling Metrics** | 20-day, 60-day, 252-day windows for volatility, beta, Sharpe |
| **Backtesting Engine** | Walk-forward analysis with configurable entry/exit rules |
| **REST APIs** | Query pairs, backtest results, correlation matrices in milliseconds |
| **PostgreSQL Backend** | Supabase for scalability; easily self-hosted |
| **Docker Ready** | Pre-built images for backend, frontend, and full orchestration |
| **CI/CD Pipeline** | GitHub Actions multi-tier validation and scheduled daily runs |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Financial Intel Platform                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Frontend (Vue 3 + Vite)     Backend (FastAPI + AsyncIO)   │
│  ├─ Pair Screener             ├─ Data Ingestion Service    │
│  ├─ Correlation Heatmap       ├─ Cointegration Engine      │
│  ├─ Backtest Results          ├─ Correlation Analysis      │
│  └─ Real-time Metrics         └─ REST API                  │
│                                                               │
│                      ↓                                        │
│                                                               │
│          PostgreSQL Database (Supabase)                      │
│          ├─ assets (symbols, metadata)                       │
│          ├─ price_history (OHLCV, daily & intraday)         │
│          ├─ correlation_matrix (precomputed pairs)          │
│          ├─ cointegration_scores (test results)             │
│          ├─ rolling_metrics (volatility, beta)              │
│          └─ pair_trades (backtest signals & performance)    │
│                                                               │
│                      ↓                                        │
│                                                               │
│          External Data Sources                              │
│          ├─ Yahoo Finance (yfinance library)               │
│          └─ Market holidays (BSE, NSE, NYSE, NASDAQ)       │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Tiers:
  Tier 1: Data Ingestion       → Fetch & standardize OHLCV
  Tier 2: Validation & QA      → Check data quality, freshness
  Tier 3: Correlation Analysis → Compute pair scores
  Tier 4: Cointegration Tests  → Statistical arbitrage signals
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+**
- **PostgreSQL 14+** (or Supabase account — free tier OK)
- **Node.js 16+** (frontend only)
- **Docker** (optional, for containerized deployment)

### Local Setup (Backend + API)

1. **Clone and install**:
   ```bash
   git clone https://github.com/ayush108108/financial-intel.git
   cd financial-intel
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

3. **Run the data pipeline**:
   ```bash
   python scripts/pipelines/daily_eod_pipeline.py
   ```

4. **Start the API server**:
   ```bash
   cd backend
   python run.py
   # API available at http://localhost:8000
   # Docs: http://localhost:8000/docs
   ```

### Frontend Setup (Optional)

```bash
cd frontend-v2
npm install
npm run dev
# Frontend at http://localhost:5173
```

### Docker Deployment

```bash
docker-compose up -d
# Backend: http://localhost:8000
# Frontend: http://localhost:80
# PostgreSQL: localhost:5432
```

---

## 📊 API Examples

### Get Top Correlation Pairs
```bash
curl -X GET "http://localhost:8000/api/pairs/top?limit=10&method=spearman&window=252"
```

### Backtest a Pair Strategy
```bash
curl -X POST "http://localhost:8000/api/backtest" \
  -H "Content-Type: application/json" \
  -d '{
    "asset1": "AAPL.US",
    "asset2": "MSFT.US",
    "entry_threshold": 2.0,
    "exit_threshold": 1.0
  }'
```

### Check Cointegration Test Results
```bash
curl -X GET "http://localhost:8000/api/cointegration/AAPL.US/MSFT.US?granularity=daily"
```

---

## 📈 Pipeline Workflow

The platform runs a **multi-tier daily pipeline** (automated via GitHub Actions):

```
Tier 1: Data Ingestion
├─ Fetch 50 asset symbols from Yahoo Finance (daily + intraday)
├─ Standardize OHLCV format (handle splits, dividends)
└─ Store in price_history table
    ↓
Tier 2: Data Validation
├─ Check completeness (min 5 points per asset)
├─ Verify freshness (data within 48 hours)
├─ Detect duplicates and outliers
└─ Gate: Only proceed if data passes QA
    ↓
Tier 3A: Correlation Analysis
├─ Compute rolling correlation matrix (20/60/252-day windows)
├─ Filter top N pairs by absolute correlation
└─ Store in correlation_matrix table
    ↓
Tier 3B: Cointegration Testing
├─ Run Engle-Granger cointegration test on pairs
├─ Calculate half-life of mean reversion
└─ Store results in cointegration_scores table
    ↓
Tier 3C: Rolling Metrics
├─ Compute volatility, beta, Sharpe ratio
├─ Track drawdown and recovery
└─ Store in rolling_metrics table
    ↓
Tier 3D: Factor Exposure Analysis
├─ Regress each pair against market factors
├─ Compute residual analysis
└─ Store in factor_exposures table
    ↓
Tier 4: Precomputation & Caching
└─ Generate derived datasets for fast API queries
```

---

## 🛠️ Configuration

All configuration via environment variables ([`.env.example`](.env.example )):

```env
# Supabase (PostgreSQL)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_role_key

# Data Pipeline
LOOKBACK_DAYS=365
MIN_ASSETS_REQUIRED=50
YF_DELAY_BETWEEN_REQUESTS=20.0
YF_RESPECT_SERVER=true

# Analytics
CORRELATION_WINDOW_DAYS=252
COINTEGRATION_SIGNIFICANCE=0.05
MIN_PAIR_CORRELATION=0.5

# API
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 📦 Project Structure

```
financial-intel/
├─ backend/                    # FastAPI server & services
│  ├─ api/
│  │  ├─ services/             # Business logic
│  │  │  ├─ pipeline_service.py
│  │  │  ├─ correlation_service.py
│  │  │  ├─ cointegration_service.py
│  │  │  └─ data_writer_service.py
│  │  └─ routers/              # REST endpoints
│  ├─ clients/
│  │  └─ yfinance_client.py    # Market data fetcher
│  └─ run.py                   # FastAPI app entry
├─ frontend-v2/               # Vue 3 + Vite
│  ├─ src/
│  │  ├─ components/
│  │  ├─ views/
│  │  └─ App.vue
│  └─ vite.config.ts
├─ scripts/
│  ├─ pipelines/
│  │  ├─ daily_eod_pipeline.py      # Tier 1-2
│  │  ├─ analytics_computation_pipeline_v2.py  # Tier 3
│  │  └─ populate_precomputed.py    # Tier 4
│  └─ db/
│     └─ schema.sql                  # Schema definition
├─ docker-compose.yml
├─ .github/workflows/
│  └─ multi-tier-pipeline.yml       # CI/CD
└─ README.md                         # You are here
```

---

## 🧪 Testing & Development

### Run the pipeline locally (with sample data):
```bash
export YF_DELAY_BETWEEN_REQUESTS=20
python scripts/pipelines/daily_eod_pipeline.py
```

### Run tests:
```bash
pytest tests/ -v
```

### View API documentation:
```
http://localhost:8000/docs  (Swagger UI)
http://localhost:8000/redoc (ReDoc)
```

---

## 📚 Documentation

- **[Architecture Deep Dive](./docs/ARCHITECTURE.md)** — System design, data flow, scaling
- **[API Reference](./docs/API.md)** — Endpoint documentation and examples
- **[Database Schema](./docs/SCHEMA.md)** — Full table definitions and relationships
- **[Deployment Guide](./docs/DEPLOYMENT.md)** — AWS, Heroku, DigitalOcean, self-hosted
- **[Contributing](./CONTRIBUTING.md)** — How to contribute and development workflow

---

## 🔐 Security & Privacy

- **No API keys required** (uses Yahoo Finance free tier)
- **Market data only** (no PII or trading accounts stored)
- **Self-hosted ready** (full control over your data)
- **Environment-based secrets** (.env never committed)
- **Row-level security** (PostgreSQL RLS policies)

---

## 📊 Use Cases

### For Traders
- Screen for pairs with high correlation and mean-reversion potential
- Backtest strategies across decades of historical data
- Real-time alerts when cointegration thresholds are crossed

### For Fintech Platforms
- Embed pair-trading modules in your app
- White-label the UI for your brand
- Use the REST API to power your recommendation engine

### For Portfolio Managers
- Understand asset correlations across your holdings
- Identify hedging opportunities
- Analyze factor exposure and residual risk

### For Researchers
- Study statistical arbitrage across different markets
- Benchmark cointegration methods
- Publish academic papers on empirical pair trading

---

## 🚦 Status & Roadmap

- ✅ Data ingestion (stocks, ETFs, crypto, international)
- ✅ Correlation analysis
- ✅ Cointegration testing
- ✅ Rolling metrics & factor analysis
- ✅ Backtesting engine
- ✅ REST API with swagger docs
- ✅ Docker & CI/CD
- 🔜 Real-time WebSocket updates
- 🔜 Machine learning pair prediction
- 🔜 Risk alerts and notifications
- 🔜 Interactive charting with TradingView

---

## 💡 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

Quick wins:
- Add new asset classes or exchanges
- Improve cointegration algorithms
- Build analysis tools and dashboards
- Optimize database queries

---

## 📞 Support & Community

- **GitHub Issues** — Bug reports and feature requests
- **Discussions** — Q&A, ideas, best practices
- **Email** — ayush@example.com (replace with your contact)

---

## 📄 License

MIT License — See [LICENSE](./LICENSE) for details.

---

## 🙏 Acknowledgments

- **yfinance** — Free market data access
- **Supabase** — PostgreSQL hosting and APIs
- **FastAPI** — Modern Python web framework
- **Vue.js** — Reactive frontend framework

---

**Made with ❤️ for traders, researchers, and fintech builders.**

[⭐ Star us on GitHub](https://github.com/ayush108108/financial-intel) | [📧 Contact](mailto:ayush@example.com) | [🔗 Live Demo](https://financial-intel-demo.com)
