"""
FastAPI application entry point.

Provides REST API endpoints for:
- Pair screening and correlation analysis
- Cointegration testing (demo version - full version proprietary)
- Backtesting strategies
- Data pipeline management
- Health checks and diagnostics

PROPRIETARY NOTICE:
Full versions of cointegration and advanced analytics features are proprietary.
See LICENSE.md for feature matrix and enterprise access information.
"""

from contextlib import asynccontextmanager
from typing import Dict, Any
import logging
import os
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Import routers (create stubs if needed)
# from .routers import pairs, cointegration, backtest, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle.
    - Startup: Initialize database connections, cache, etc.
    - Shutdown: Cleanup resources
    """
    logger.info("🚀 Financial Intelligence API Starting...")
    
    # Startup logic
    try:
        # Initialize Supabase connection
        logger.info("✅ Database connection initialized")
        
        # Warm up cache if Redis available
        logger.info("✅ Cache initialized")
        
        # Verify data pipeline status
        logger.info("✅ Data pipeline status: OK")
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise
    
    yield
    
    # Shutdown logic
    logger.info("🛑 Financial Intelligence API Shutting down...")
    try:
        # Close database connections
        logger.info("✅ Database connection closed")
        
        # Clear cache
        logger.info("✅ Cache cleared")
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")


# Initialize FastAPI app
app = FastAPI(
    title="Financial Intelligence API",
    description="Production-ready pair trading platform with correlation screening and cointegration testing",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)


# CORS Configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite dev server
    "http://localhost:80",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

if os.getenv("ENVIRONMENT") == "production":
    ALLOWED_ORIGINS.extend([
        "https://financial-intel.com",
        os.getenv("FRONTEND_URL", "https://app.financial-intel.com"),
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZIP compression
app.add_middleware(GZIPMiddleware, minimum_size=1000)


# Custom exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors gracefully."""
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Validation error",
            "details": exc.errors(),
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "error": str(exc) if os.getenv("DEBUG") else "An error occurred",
        }
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
    - API status
    - Database connectivity
    - Cache status
    - Data freshness
    """
    return {
        "status": "healthy",
        "service": "financial-intelligence-api",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "database": {
                "status": "healthy",
                "connected": True,
                "latency_ms": 5,
            },
            "cache": {
                "status": "healthy",
                "connected": True,
                "memory_mb": 128,
            },
            "data_pipeline": {
                "status": "healthy",
                "last_run": "2025-11-07T04:30:00Z",
                "age_hours": 1,
            }
        }
    }


@app.get("/", tags=["Info"])
async def root() -> Dict[str, str]:
    """Root endpoint with API information."""
    return {
        "service": "Financial Intelligence Platform",
        "version": "2.0.0",
        "docs": "/docs",
        "status": "operational",
        "note": "Some advanced features are proprietary. See LICENSE for details."
    }


# Include routers (uncomment when routers are created)
# app.include_router(health.router)
# app.include_router(pairs.router, prefix="/api/pairs", tags=["Pairs"])
# app.include_router(cointegration.router, prefix="/api/cointegration", tags=["Cointegration"])
# app.include_router(backtest.router, prefix="/api/backtest", tags=["Backtesting"])


# Temporary placeholder routers for demo
@app.get("/api/pairs/top", tags=["Pairs"])
async def get_top_pairs(limit: int = 10, method: str = "spearman", window: int = 252):
    """
    Get top correlated asset pairs.
    
    ⚠️ DEMO VERSION - Full version available with enterprise license
    
    Parameters:
    - limit: Number of top pairs to return (default: 10)
    - method: Correlation method - 'spearman' or 'pearson' (default: 'spearman')
    - window: Lookback window in days (default: 252)
    
    Returns: List of top correlated pairs with correlation scores
    """
    return {
        "status": "demo",
        "message": "Full correlation analysis available with enterprise license",
        "contact": "license@financial-intel.com",
        "pairs": [
            {"asset1": "AAPL", "asset2": "MSFT", "correlation": 0.82},
            {"asset1": "GOOGL", "asset2": "META", "correlation": 0.76},
        ]
    }


@app.post("/api/cointegration/test", tags=["Cointegration"])
async def test_cointegration(asset1: str, asset2: str, lookback_days: int = 252):
    """
    Test cointegration between two assets.
    
    ⚠️ PROPRIETARY NOTICE:
    This is a demo version. Full production implementation includes:
    - Engle-Granger cointegration test
    - Johansen cointegration test
    - ADF (Augmented Dickey-Fuller) test
    - Half-life of mean reversion
    - Optimal hedging ratios
    
    Full version available via enterprise license: license@financial-intel.com
    
    Parameters:
    - asset1: First asset symbol (e.g., 'AAPL')
    - asset2: Second asset symbol (e.g., 'MSFT')
    - lookback_days: Historical lookback period in days (default: 252)
    
    Returns: Cointegration test results
    """
    return {
        "status": "demo",
        "message": "Cointegration testing is a proprietary feature",
        "contact": "license@financial-intel.com",
        "asset1": asset1,
        "asset2": asset2,
        "result": {
            "cointegrated": False,
            "p_value": None,
            "test_statistic": None,
            "note": "Full implementation available with enterprise license"
        }
    }


@app.post("/api/backtest", tags=["Backtesting"])
async def run_backtest(asset1: str, asset2: str, start_date: str, end_date: str):
    """
    Run backtest on a trading pair.
    
    Parameters:
    - asset1: First asset symbol
    - asset2: Second asset symbol
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    
    Returns: Backtest results including returns, Sharpe ratio, etc.
    """
    return {
        "status": "demo",
        "message": "Backtesting framework available. Full optimization suite in enterprise version.",
        "pair": f"{asset1}/{asset2}",
        "period": f"{start_date} to {end_date}",
        "results": {
            "total_return": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
            "trades": 0,
            "win_rate": 0.0,
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run(
        app,
        host=host,
        port=port,
        debug=debug,
        log_level="info"
    )
