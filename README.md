# Financial Intelligence Platform

> **Intelligent financial data pipeline with real-time pair trading analysis. Detect statistical arbitrage opportunities via cointegration testing and correlation-based pair screening.**

![License](https://img.shields.io/badge/license-MIT%20%2B%20Proprietary-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

---

## ⚠️ Proprietary Components Notice

This repository contains **minimal demo versions** of certain high-value analytical components.
The full production implementations are proprietary and available exclusively for enterprise customers.

### Components with Proprietary Full Versions:

| Component | Demo Status | Full Version Features |
|-----------|------------|----------------------|
| **Cointegration Engine** | ✅ Demo stub | Engle-Granger testing, Johansen method, ADF testing, mean-reversion detection, half-life computation, optimal hedging ratios |
| **Correlation Analysis** | ✅ Demo stub | Multi-method analysis, rolling windows (20/60/252-day), hierarchical clustering, real-time screening, factor-adjusted correlations |
| **Interactive Heatmap UI** | ✅ Basic table | D3.js/Plotly interactive visualization, zoom/pan/clustering display, real-time updates, correlation network graphs |
| **Advanced Analytics** | ✅ Limited | Machine learning pair prediction, regime detection, risk assessment models, portfolio optimization |

### Request Full Access

For production-grade statistical arbitrage and advanced analytics:

**Email**: `license@financial-intel.com`  
**Subject**: "Financial Intelligence Enterprise License"

**Enterprise package includes:**
- Full source code for all proprietary components
- Unlimited commercial usage rights
- 24/7 priority support and updates
- Custom integration training and consulting
- Backtesting framework with advanced metrics
- Real-time alert systems

See [LICENSE](./LICENSE) for complete feature matrix and terms.

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
| **Cointegration Testing** | Statistical significance testing (demo version; full version includes Engle-Granger, Johansen, ADF) |
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
│  ├─ Correlation Heatmap       ├─ Cointegration Engine*     │
│  ├─ Backtest Results          ├─ Correlation Analysis      │
│  └─ Real-time Metrics         └─ REST API                  │
│                                                               │
│  * Full version available with enterprise license            │
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
  
Note: Tier 4 in this repo is a demo. Full version available via enterprise license.
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

* Tier 3B-4 functionality in this repo is demo only.
  Full production version available with enterprise license.
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
│  │  │  ├─ correlation_service.py (demo)
│  │  │  ├─ cointegration_service.py (demo - full version proprietary)
│  │  │  └─ data_writer_service.py
│  │  └─ routers/              # REST endpoints
│  ├─ clients/
│  │  └─ yfinance_client.py    # Market data fetcher
│  └─ run.py                   # FastAPI app entry
├─ frontend-v2/               # Vue 3 + Vite
│  ├─ src/
│  │  ├─ components/
│  │  │  └─ CorrelationHeatmapDemo.vue (demo - full UI proprietary)
│  │  ├─ views/
│  │  └─ App.vue
│  └─ vite.config.ts
├─ scripts/
│  ├─ pipelines/
│  │  ├─ daily_eod_pipeline.py      # Tier 1-2 (public)
│  │  ├─ analytics_computation_pipeline_v2.py  # Tier 3 (demo)
│  │  └─ populate_precomputed.py    # Tier 4 (demo)
│  └─ db/
│     └─ schema.sql                  # Schema definition
├─ docker-compose.yml
├─ .github/workflows/
│  └─ multi-tier-pipeline.yml       # CI/CD
├─ LICENSE                          # MIT + Proprietary terms
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
- **[LICENSE](./LICENSE)** — MIT + Proprietary components notice with complete feature matrix

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
- Real-time alerts when cointegration thresholds are crossed (enterprise version)

### For Fintech Platforms
- Embed pair-trading modules in your app
- White-label the UI for your brand
- Use the REST API to power your recommendation engine
- Access advanced analytics via enterprise license

### For Portfolio Managers
- Understand asset correlations across your holdings
- Identify hedging opportunities
- Analyze factor exposure and residual risk
- Detect statistical arbitrage opportunities (enterprise version)

### For Researchers
- Study statistical arbitrage across different markets
- Benchmark cointegration methods
- Publish academic papers on empirical pair trading
- Access full research implementations (enterprise version)

---

## 🚦 Status & Roadmap

### Open Source (MIT)
- ✅ Data ingestion (stocks, ETFs, crypto, international)
- ✅ Correlation analysis (Spearman/Pearson)
- ✅ Rolling metrics & factor analysis
- ✅ Backtesting engine (basic)
- ✅ REST API with swagger docs
- ✅ Docker & CI/CD

### Enterprise (Proprietary License)
- 🔒 Advanced cointegration testing (Engle-Granger, Johansen, ADF)
- 🔒 Interactive correlation heatmap visualization
- 🔒 Machine learning pair prediction
- 🔒 Real-time WebSocket updates
- 🔒 Risk alerts and notifications
- 🔒 Advanced backtesting with optimization
- 🔒 Custom integration and training

*Contact `license@financial-intel.com` to upgrade to enterprise.*

---

## 💡 Contributing

We welcome contributions to the open-source components! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

Quick wins:
- Add new asset classes or exchanges
- Improve data validation logic
- Build additional analysis tools and dashboards
- Optimize database queries
- Improve documentation and examples

**Note**: Proprietary components (cointegration engine, advanced heatmap UI) are not open for contributions at this time but are available via enterprise license.

---

## 📞 Support & Community

- **GitHub Issues** — Bug reports and feature requests (open-source components)
- **Discussions** — Q&A, ideas, best practices
- **Enterprise Support** — Email `license@financial-intel.com` for SLA-backed 24/7 support

---

## 📄 License

Dual-licensed:
- **Open Source Components**: MIT License
- **Proprietary Components**: Custom Enterprise License (see [LICENSE](./LICENSE))

See [LICENSE](./LICENSE) for complete details.

---

## 🙏 Acknowledgments

- **yfinance** — Free market data access
- **Supabase** — PostgreSQL hosting and APIs
- **FastAPI** — Modern Python web framework
- **Vue.js** — Reactive frontend framework
- **pandas & NumPy** — Data science foundations

---

**Made with ❤️ for traders, researchers, and fintech builders.**

[⭐ Star us on GitHub](https://github.com/ayush108108/financial-intel) | [📧 Enterprise](mailto:license@financial-intel.com) | [🔐 License](./LICENSE)
