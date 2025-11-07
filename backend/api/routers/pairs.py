"""
Pairs screening router.

Endpoints:
- GET /api/pairs/top - Get top correlated pairs
- GET /api/pairs/{symbol} - Get pairs for a specific asset
- GET /api/pairs/search - Search pairs by criteria
"""

from fastapi import APIRouter, Query
from typing import Optional, List

router = APIRouter(prefix="/api/pairs", tags=["Pairs"])


@router.get("/top")
async def get_top_pairs(
    limit: int = Query(10, ge=1, le=100),
    method: str = Query("spearman", regex="^(spearman|pearson)$"),
    window: int = Query(252, ge=20, le=1000),
    min_correlation: float = Query(0.5, ge=0.0, le=1.0),
):
    """
    Get top correlated asset pairs.
    
    Parameters:
    - limit: Number of pairs to return (1-100, default: 10)
    - method: Correlation method (spearman or pearson, default: spearman)
    - window: Lookback window in days (20-1000, default: 252)
    - min_correlation: Minimum correlation threshold (0-1, default: 0.5)
    
    Returns:
    - List of top correlated pairs with statistics
    """
    return {
        "status": "demo",
        "pairs": [],
        "total_pairs": 0,
        "message": "Full correlation analysis available with enterprise license"
    }


@router.get("/{symbol}")
async def get_pairs_for_symbol(symbol: str, limit: int = Query(10, ge=1, le=50)):
    """
    Get correlated pairs for a specific asset.
    
    Parameters:
    - symbol: Asset symbol (e.g., AAPL)
    - limit: Number of pairs to return (default: 10)
    
    Returns:
    - Pairs correlated with the specified asset
    """
    return {
        "symbol": symbol,
        "pairs": [],
        "total_pairs": 0,
    }
