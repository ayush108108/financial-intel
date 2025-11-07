"""
Yahoo Finance client using yfinance library.
Free, no API key required, supports all asset types.

Ticker Format Examples:
- US Stocks: AAPL, MSFT, TSLA
- US ETFs: SPY, QQQ, DIA
- Crypto: BTC-USD, ETH-USD, SOL-USD
- India NSE: NIFTYBEES.NS, RELIANCE.NS
- India BSE: SENSEX.BO
"""

import asyncio
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import pandas as pd
import yfinance as yf
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class YFinanceConfig:
    """Configuration for yfinance client."""

    auto_adjust: bool = True
    repair: bool = True
    keepna: bool = False
    timeout: int = 30
    threads: bool = False
    delay_between_requests: float = 60.0
    respect_server: bool = True


class YFinanceClient:
    """
    Yahoo Finance client using yfinance library.

    Benefits:
    - Free, no API key required
    - No rate limits (reasonable use)
    - Supports stocks, ETFs, crypto, international markets
    - Auto-adjusted prices (splits & dividends)
    - Multiple intervals: 1d, 4h, 1h, etc.

    Limitations:
    - Unofficial API (can break without notice)
    - For personal/educational use only
    - Intraday data limited to last 60 days
    """

    def __init__(self, config: Optional[YFinanceConfig] = None):
        """Initialize Yahoo Finance client."""
        self.config = config or YFinanceConfig()
        self.last_request_time = 0.0
        logger.info(
            f"Initialized Yahoo Finance client (no API key required) - "
            f"Rate limit: 1 request per {self.config.delay_between_requests}s"
        )

    def _convert_symbol_to_yfinance(
        self, symbol: str, asset_type: Optional[str] = None
    ) -> str:
        """Convert symbol to Yahoo Finance format."""
        if any(suffix in symbol for suffix in [".NS", ".BO", "-USD"]):
            return symbol

        if asset_type == "crypto" or ".CC" in symbol:
            if ".CC" in symbol:
                symbol = symbol.replace(".CC", "")
            if not symbol.endswith("-USD"):
                base = symbol.split("-")[0]
                return f"{base}-USD"
            return symbol

        if ".NSE" in symbol:
            return symbol.replace(".NSE", ".NS")

        if symbol.endswith(".BSE"):
            return symbol.replace(".BSE", ".BO")

        if symbol.endswith(".US"):
            return symbol.replace(".US", "")

        return symbol

    def _yfinance_to_hedgevision_df(
        self, yf_df: pd.DataFrame, symbol: str
    ) -> pd.DataFrame:
        """Convert yfinance DataFrame to standardized format."""
        if yf_df.empty:
            return pd.DataFrame()

        df = yf_df.reset_index()

        df.columns = [
            col.lower() if isinstance(col, str) else str(col[0]).lower()
            for col in df.columns
        ]

        column_mapping = {"date": "timestamp", "datetime": "timestamp"}
        df = df.rename(columns=column_mapping)

        if "timestamp" not in df.columns and df.index.name:
            df["timestamp"] = df.index
            df = df.reset_index(drop=True)

        if "close" in df.columns and "adjusted_close" not in df.columns:
            df["adjusted_close"] = df["close"]

        df["source"] = "yfinance"
        df["data_quality"] = 1.0

        required_cols = [
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "adjusted_close",
            "source",
            "data_quality",
        ]

        available_cols = [col for col in required_cols if col in df.columns]
        df = df[available_cols]

        return df

    async def fetch_historical_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
        asset_type: Optional[str] = None,
    ) -> pd.DataFrame:
        """Fetch historical data from Yahoo Finance with rate limiting."""
        if self.config.respect_server:
            current_time = asyncio.get_event_loop().time()
            time_since_last = current_time - self.last_request_time

            if time_since_last < self.config.delay_between_requests:
                sleep_duration = self.config.delay_between_requests - time_since_last
                logger.info(
                    f"Rate limiting: waiting {sleep_duration:.1f}s before next request"
                )
                await asyncio.sleep(sleep_duration)

            self.last_request_time = asyncio.get_event_loop().time()

        yf_symbol = self._convert_symbol_to_yfinance(symbol, asset_type)

        logger.info(
            f"Fetching Yahoo Finance data for {yf_symbol} "
            f"from {start_date.date()} to {end_date.date()} "
            f"(interval: {interval})"
        )

        try:
            loop = asyncio.get_event_loop()
            yf_df = await loop.run_in_executor(
                None,
                lambda: yf.download(
                    yf_symbol,
                    start=start_date,
                    end=end_date,
                    interval=interval,
                    auto_adjust=self.config.auto_adjust,
                    repair=self.config.repair,
                    keepna=self.config.keepna,
                    progress=False,
                    timeout=self.config.timeout,
                ),
            )

            if yf_df.empty:
                logger.warning(f"No data returned for {yf_symbol}")
                return pd.DataFrame()

            df = self._yfinance_to_hedgevision_df(yf_df, symbol)
            logger.info(f"Fetched {len(df)} records for {yf_symbol}")
            return df

        except Exception as e:
            logger.error(f"Failed to fetch data for {yf_symbol}: {e}")
            return pd.DataFrame()

    async def fetch_batch_multi(
        self,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
        asset_types: Optional[Dict[str, str]] = None,
        group_size: int = 5,
    ) -> Dict[str, pd.DataFrame]:
        """Fetch multiple symbols using yfinance multi-ticker download in groups.

        Uses a single Yahoo request per group of up to `group_size` symbols.
        Respects the client's delay_between_requests between groups.
        """
        asset_types = asset_types or {}

        symbol_map: Dict[str, str] = {}
        for s in symbols:
            symbol_map[s] = self._convert_symbol_to_yfinance(s, asset_types.get(s))

        def chunk(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i : i + n]

        results: Dict[str, pd.DataFrame] = {}
        for group in chunk(symbols, group_size):
            yf_group = [symbol_map[s] for s in group]

            if self.config.respect_server:
                current_time = asyncio.get_event_loop().time()
                time_since_last = current_time - self.last_request_time
                if time_since_last < self.config.delay_between_requests:
                    sleep_duration = self.config.delay_between_requests - time_since_last
                    logger.info(
                        f"Rate limiting: waiting {sleep_duration:.1f}s before next multi-ticker request"
                    )
                    await asyncio.sleep(sleep_duration)
                self.last_request_time = asyncio.get_event_loop().time()

            logger.info(
                f"Fetching Yahoo Finance data for group: {', '.join(yf_group)} "
                f"from {start_date.date()} to {end_date.date()} (interval: {interval})"
            )

            try:
                loop = asyncio.get_event_loop()
                yf_df = await loop.run_in_executor(
                    None,
                    lambda: yf.download(
                        tickers=yf_group,
                        start=start_date,
                        end=end_date,
                        interval=interval,
                        auto_adjust=self.config.auto_adjust,
                        repair=self.config.repair,
                        keepna=self.config.keepna,
                        progress=False,
                        timeout=self.config.timeout,
                        group_by="ticker",
                        threads=False,
                    ),
                )

                if isinstance(yf_df, pd.DataFrame) and not isinstance(
                    yf_df.columns, pd.MultiIndex
                ):
                    only = group[0]
                    results[only] = self._yfinance_to_hedgevision_df(yf_df, only)
                else:
                    for orig in group:
                        yf_t = symbol_map[orig]
                        try:
                            sub = yf_df[yf_t]
                            if isinstance(sub, pd.Series):
                                sub = sub.to_frame()
                            results[orig] = self._yfinance_to_hedgevision_df(sub, orig)
                        except Exception:
                            results[orig] = pd.DataFrame()
                            logger.warning(f"No data segment for {yf_t} in group response")

            except Exception as e:
                logger.error(f"Failed multi-ticker download for group {yf_group}: {e}")
                for orig in group:
                    results[orig] = pd.DataFrame()

        return results

    async def close(self):
        """Close client (no-op for yfinance)."""
        logger.info("Yahoo Finance client closed")


def get_yfinance_client() -> YFinanceClient:
    """Get singleton YFinanceClient instance with environment overrides."""
    try:
        delay = float(os.getenv("YF_DELAY_BETWEEN_REQUESTS", "20.0"))
    except Exception:
        delay = 20.0
    respect = str(os.getenv("YF_RESPECT_SERVER", "true")).lower() in (
        "true",
        "1",
        "yes",
    )
    cfg = YFinanceConfig(delay_between_requests=delay, respect_server=respect)
    return YFinanceClient(config=cfg)
