# API Reference - Financial Intelligence Platform

The Financial Intelligence Platform exposes a REST API for accessing pair data, backtest results, and analytical metrics.

**Base URL**: `http://localhost:8000/api/` (development) or `https://api.financial-intel.com/api/` (production)

**Interactive Docs**: 
- Swagger UI: `{BASE_URL}../docs`
- ReDoc: `{BASE_URL}../redoc`

---

## Table of Contents
- [Authentication](#authentication)
- [Pairs Endpoints](#pairs-endpoints)
- [Correlation Endpoints](#correlation-endpoints)
- [Cointegration Endpoints](#cointegration-endpoints)
- [Backtest Endpoints](#backtest-endpoints)
- [Metrics Endpoints](#metrics-endpoints)
- [Error Handling](#error-handling)

---

## Authentication

Currently, the API is **open without authentication** (great for internal tools and proof-of-concept).

For production deployments with API key authentication:
```bash
curl -X GET "http://localhost:8000/api/pairs/top" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## Pairs Endpoints

### List Top Correlation Pairs

**GET** `/pairs/top`

Find the most correlated asset pairs.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 10 | Number of pairs to return |
| `method` | string | "spearman" | Correlation method: `spearman` or `pearson` |
| `window` | integer | 252 | Lookback window in days |
| `min_correlation` | float | 0.5 | Minimum correlation threshold |

**Example:**
```bash
curl "http://localhost:8000/api/pairs/top?limit=20&method=spearman&window=252"
```

**Response:**
```json
{
  "pairs": [
    {
      "asset1": "AAPL.US",
      "asset2": "MSFT.US",
      "correlation": 0.87,
      "cointegration_score": 0.82,
      "p_value": 0.003,
      "mean_reversion_half_life": 12.5
    }
  ],
  "total": 1250,
  "limit": 20,
  "method": "spearman",
  "window_days": 252
}
```

---

### Get Pair Details

**GET** `/pairs/{asset1}/{asset2}`

Get detailed analytics for a specific pair.

**Path Parameters:**
- `asset1`: First asset symbol (e.g., `AAPL.US`)
- `asset2`: Second asset symbol (e.g., `MSFT.US`)

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `granularity` | string | "daily" | `daily` or `intraday` |

**Example:**
```bash
curl "http://localhost:8000/api/pairs/AAPL.US/MSFT.US?granularity=daily"
```

**Response:**
```json
{
  "asset1": "AAPL.US",
  "asset2": "MSFT.US",
  "correlation": 0.87,
  "cointegration_score": 0.82,
  "p_value": 0.003,
  "mean_reversion_half_life": 12.5,
  "last_updated": "2025-11-07T10:30:00Z",
  "metrics": {
    "asset1_volatility": 0.18,
    "asset2_volatility": 0.16,
    "asset1_beta": 1.05,
    "asset2_beta": 1.02
  }
}
```

---

## Correlation Endpoints

### Get Correlation Matrix

**GET** `/correlation/matrix`

Retrieve the precomputed correlation matrix for all assets.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `method` | string | "spearman" | `spearman` or `pearson` |
| `window` | integer | 252 | Lookback window in days |
| `format` | string | "json" | `json` or `csv` |

**Example:**
```bash
curl "http://localhost:8000/api/correlation/matrix?method=spearman&window=252&format=json"
```

**Response:**
```json
{
  "matrix": [
    ["AAPL.US", "MSFT.US", "GOOG.US"],
    [1.0, 0.87, 0.92],
    [0.87, 1.0, 0.89],
    [0.92, 0.89, 1.0]
  ],
  "assets": ["AAPL.US", "MSFT.US", "GOOG.US"],
  "method": "spearman",
  "window_days": 252,
  "last_updated": "2025-11-07T10:30:00Z"
}
```

---

### Filter Pairs by Correlation Range

**GET** `/correlation/filter`

Find all pairs within a specific correlation range.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `min_correlation` | float | 0.5 | Minimum correlation |
| `max_correlation` | float | 1.0 | Maximum correlation |
| `method` | string | "spearman" | Correlation method |
| `window` | integer | 252 | Lookback window in days |

**Example:**
```bash
curl "http://localhost:8000/api/correlation/filter?min_correlation=0.7&max_correlation=0.95"
```

---

## Cointegration Endpoints

### Get Cointegration Score

**GET** `/cointegration/{asset1}/{asset2}`

Check if two assets are cointegrated (move together long-term).

**Path Parameters:**
- `asset1`: First asset symbol
- `asset2`: Second asset symbol

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `granularity` | string | "daily" | `daily` or `intraday` |

**Example:**
```bash
curl "http://localhost:8000/api/cointegration/AAPL.US/MSFT.US?granularity=daily"
```

**Response:**
```json
{
  "asset1": "AAPL.US",
  "asset2": "MSFT.US",
  "cointegrated": true,
  "p_value": 0.003,
  "half_life_days": 12.5,
  "spread_mean": -0.02,
  "spread_std": 0.15,
  "zscore": 1.2,
  "entry_signal": null,
  "exit_signal": true
}
```

---

### List Top Cointegrated Pairs

**GET** `/cointegration/top`

Get the most statistically significant cointegrated pairs.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 10 | Number of pairs to return |
| `p_value_threshold` | float | 0.05 | Statistical significance (1% = 0.01, 5% = 0.05) |

**Example:**
```bash
curl "http://localhost:8000/api/cointegration/top?limit=15&p_value_threshold=0.01"
```

---

## Backtest Endpoints

### Run Backtest

**POST** `/backtest`

Backtest a trading strategy on a specific pair.

**Request Body:**
```json
{
  "asset1": "AAPL.US",
  "asset2": "MSFT.US",
  "entry_threshold": 2.0,
  "exit_threshold": 1.0,
  "start_date": "2023-01-01",
  "end_date": "2025-11-07",
  "position_size": 10000,
  "granularity": "daily"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/backtest" \
  -H "Content-Type: application/json" \
  -d '{
    "asset1": "AAPL.US",
    "asset2": "MSFT.US",
    "entry_threshold": 2.0,
    "exit_threshold": 1.0,
    "start_date": "2023-01-01",
    "end_date": "2025-11-07"
  }'
```

**Response:**
```json
{
  "total_return": 0.145,
  "sharpe_ratio": 1.28,
  "max_drawdown": -0.12,
  "win_rate": 0.62,
  "total_trades": 25,
  "winning_trades": 15,
  "losing_trades": 10,
  "avg_win": 0.032,
  "avg_loss": -0.018,
  "profit_factor": 1.78,
  "trades": [
    {
      "entry_date": "2023-01-15",
      "exit_date": "2023-02-10",
      "entry_price": 0.05,
      "exit_price": 0.08,
      "pnl": 0.03,
      "return": 0.06
    }
  ]
}
```

---

### Get Backtest Results

**GET** `/backtest/{asset1}/{asset2}`

Retrieve precomputed backtest results for a pair.

**Example:**
```bash
curl "http://localhost:8000/api/backtest/AAPL.US/MSFT.US"
```

---

## Metrics Endpoints

### Get Rolling Metrics

**GET** `/metrics/{asset}`

Get volatility, beta, and Sharpe ratio for an asset.

**Path Parameters:**
- `asset`: Asset symbol (e.g., `AAPL.US`)

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `window` | integer | 252 | Lookback window in days |

**Example:**
```bash
curl "http://localhost:8000/api/metrics/AAPL.US?window=252"
```

**Response:**
```json
{
  "asset": "AAPL.US",
  "volatility_252d": 0.18,
  "volatility_60d": 0.22,
  "volatility_20d": 0.25,
  "beta_252d": 1.05,
  "sharpe_ratio_252d": 0.92,
  "max_drawdown": -0.35,
  "recovery_time_days": 120,
  "last_updated": "2025-11-07T10:30:00Z"
}
```

---

### Get Factor Exposures

**GET** `/factors/{asset1}/{asset2}`

Analyze how much of pair movement is driven by market factors.

**Example:**
```bash
curl "http://localhost:8000/api/factors/AAPL.US/MSFT.US"
```

**Response:**
```json
{
  "market_beta": 0.05,
  "market_beta_pvalue": 0.45,
  "residual_correlation": 0.82,
  "r_squared": 0.15,
  "alpha": 0.002,
  "factors": {
    "market": 0.05,
    "size": -0.02,
    "value": 0.03,
    "momentum": 0.01
  }
}
```

---

## Error Handling

The API returns standard HTTP status codes:

| Status | Description |
|--------|-------------|
| 200 | OK |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found (asset/pair doesn't exist) |
| 500 | Internal Server Error |

**Error Response Format:**
```json
{
  "error": "Invalid asset symbol",
  "detail": "Asset 'XYZ.US' not found in database",
  "status": 404
}
```

---

## Rate Limiting

- **Free Tier**: 100 requests/minute per IP
- **Authenticated**: 1000 requests/minute per API key
- Response headers include remaining quota:
  ```
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 87
  X-RateLimit-Reset: 1630707600
  ```

---

## SDK Examples

### Python
```python
import requests

BASE_URL = "http://localhost:8000/api"

# Get top pairs
response = requests.get(f"{BASE_URL}/pairs/top?limit=10")
pairs = response.json()

# Run backtest
backtest_params = {
    "asset1": "AAPL.US",
    "asset2": "MSFT.US",
    "entry_threshold": 2.0,
    "exit_threshold": 1.0
}
response = requests.post(f"{BASE_URL}/backtest", json=backtest_params)
results = response.json()
```

### JavaScript/TypeScript
```typescript
const BASE_URL = "http://localhost:8000/api";

// Get top pairs
const response = await fetch(`${BASE_URL}/pairs/top?limit=10`);
const pairs = await response.json();

// Run backtest
const backtestParams = {
  asset1: "AAPL.US",
  asset2: "MSFT.US",
  entry_threshold: 2.0,
  exit_threshold: 1.0
};
const response = await fetch(`${BASE_URL}/backtest`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(backtestParams)
});
const results = await response.json();
```

---

## Webhooks (Roadmap)

- Real-time alerts when cointegration crosses threshold
- Daily digest of top new pairs
- Backtest completion notifications

Subscribe to updates in [Discussions](https://github.com/ayush108108/financial-intel/discussions).

---

For more details, visit the interactive API docs at `http://localhost:8000/docs`
