# ⚡ 5-Minute Quickstart Guide

Get Financial Intelligence running in 5 minutes with Docker.

---

## Prerequisites

- **Docker** & **Docker Compose** installed
- **Supabase account** (free tier: https://supabase.com)
- **~2GB disk space**

---

## Step 1: Get Supabase Credentials (1 min)

1. Go to https://supabase.com and sign up (free)
2. Create a new project
3. Go to **Settings → API Keys**
4. Copy:
   - `SUPABASE_URL` (Project URL)
   - `SUPABASE_KEY` (Anon key)
   - `SUPABASE_SERVICE_KEY` (Service role key)

---

## Step 2: Clone & Configure (1 min)

```bash
# Clone repository
git clone https://github.com/ayush108108/financial-intel.git
cd financial-intel

# Create .env file
cp .env.example .env

# Edit .env with your Supabase credentials
# On macOS/Linux:
nano .env

# On Windows (PowerShell):
# notepad .env
```

**Required .env variables:**
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_role_key_here
```

---

## Step 3: Start Services (1 min)

```bash
# Start all services in background
docker-compose up -d

# Watch the logs
docker-compose logs -f
```

Wait for "Application startup complete" message (~30-60 seconds).

---

## Step 4: Initialize Database (1 min)

```bash
# Open a new terminal (keep logs running in first one)

# Initialize database schema
docker-compose exec backend python -m backend.db.init
```

Or manually via Supabase dashboard:
1. Go to your Supabase project → SQL Editor
2. Copy-paste contents of `scripts/db/schema.sql`
3. Click "Run"

---

## Step 5: Access Services (1 min)

| Service | URL |
|---------|-----|
| **API Server** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Frontend** | http://localhost |

**Test the API:**
```bash
curl http://localhost:8000/api/pairs/top?limit=5
```

---

## ✅ You're Done!

### Next Steps

**Option A: Run the pipeline (automatic ingestion)**
```bash
docker-compose exec backend python scripts/pipelines/daily_eod_pipeline.py
```

**Option B: Explore the API**
- Visit http://localhost:8000/docs
- Try different endpoints to see pair correlations, backtests, etc.

**Option C: Check the frontend**
- Visit http://localhost
- Browse correlation matrices, pair analytics, etc.

---

## 🆘 Troubleshooting

### Issue: "Connection refused"
```bash
# Check if services are running
docker-compose ps

# Start them if needed
docker-compose up -d

# View logs
docker-compose logs backend
```

### Issue: "Database connection failed"
```bash
# Verify Supabase credentials in .env
cat .env | grep SUPABASE

# Test connection
docker-compose exec backend python -c \
  "from backend.clients.supabase_client import get_client; print(get_client().ping())"
```

### Issue: "Port already in use"
```bash
# Change ports in docker-compose.yml
# Or stop existing containers:
docker-compose down

# Free up port 8000:
lsof -i :8000
kill -9 <PID>
```

### Issue: "Out of disk space"
```bash
# Clean up Docker
docker system prune -a

# Remove old data
docker volume rm financial-intel_postgres_data
```

---

## 🚀 What's Running?

```
Backend (FastAPI)
  ├─ REST API for pair analysis
  ├─ Pipeline orchestrator
  └─ WebSocket support (coming soon)

Frontend (Vue 3)
  ├─ Pair screener dashboard
  ├─ Correlation heatmap
  └─ Backtest results viewer

Database (PostgreSQL via Supabase)
  ├─ Assets & price history
  ├─ Correlation scores
  ├─ Cointegration results
  └─ Backtest records
```

---

## 📊 Sample API Calls

### Get top correlated pairs
```bash
curl "http://localhost:8000/api/pairs/top?limit=10&method=spearman"
```

### Check cointegration
```bash
curl "http://localhost:8000/api/cointegration/AAPL.US/MSFT.US"
```

### Run a backtest
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

For more API examples, see [API.md](./docs/API.md).

---

## 📚 Learn More

- **Full README**: [README.md](./README.md)
- **API Reference**: [docs/API.md](./docs/API.md)
- **Deployment Guide**: [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)
- **Contributing**: [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 💡 Tips

1. **First run takes ~5 mins** to fetch historical data. Be patient!
2. **Check logs** for real-time status:
   ```bash
   docker-compose logs -f backend
   ```
3. **Stop everything**: `docker-compose down`
4. **Full cleanup** (⚠️ deletes data): `docker-compose down -v`

---

## 🎯 What Next?

- [ ] Run the data pipeline to populate price data
- [ ] Explore the correlation matrix via frontend
- [ ] Run backtests on cointegrated pairs
- [ ] Set up scheduled pipeline runs (see [DEPLOYMENT.md](./docs/DEPLOYMENT.md))
- [ ] Deploy to DigitalOcean/AWS (see [DEPLOYMENT.md](./docs/DEPLOYMENT.md))

---

**Questions?** Open an issue on [GitHub](https://github.com/ayush108108/financial-intel/issues) or visit [Discussions](https://github.com/ayush108108/financial-intel/discussions).

**Ready to code?** See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup.

---

**Happy trading!** 🚀📈
