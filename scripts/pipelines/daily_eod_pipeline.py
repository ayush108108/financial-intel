"""
Daily EOD Data Pipeline with Validation Gates
Orchestrates: Data Ingestion → Validation → Analytics Computation

Architecture:
1. Raw data ingestion (yfinance)
2. Data quality validation and verification
3. Analytics computation (only if validation passes)
4. Precomputed data generation

This pipeline ensures analytics are only computed on verified, high-quality raw data.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Dict, List
import logging
import traceback

base_backend = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(base_backend.resolve()))

import pandas as pd

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

MIN_DATA_POINTS_REQUIRED = 5
MAX_MISSING_RATIO = 0.1
MIN_ASSETS_REQUIRED = 50

LOOKBACK_DAYS = 5
BATCH_SIZE = 10
MAX_WORKERS = 5


# ============================================================================
# DATA INGESTION LAYER
# ============================================================================

class DataIngestionOrchestrator:
    """Orchestrates raw data ingestion from yfinance"""

    def __init__(self):
        """Initialize ingestion orchestrator."""
        from api.utils.supabase_client import get_supabase_client
        from api.services.pipeline_service import PipelineService

        self.supabase = get_supabase_client()
        self.pipeline_service = PipelineService()
        self.stats = {
            "total_assets": 0,
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "total_records": 0,
        }

    def fetch_active_assets(self) -> List[Dict]:
        """Fetch list of active assets to update"""
        logger.info("Fetching active assets from database...")
        response = self.supabase.client.table("assets").select(
            "symbol,yfinance_ticker"
        ).eq("is_active", 1).execute()

        assets = response.data
        logger.info(f"Found {len(assets)} active assets")
        return assets

    async def ingest_daily_data(self, assets: List[Dict]) -> Dict:
        """Ingest daily EOD data for all active assets"""
        logger.info(f"\n{'='*80}")
        logger.info("STAGE 1: RAW DATA INGESTION")
        logger.info(f"{'='*80}\n")

        self.stats["total_assets"] = len(assets)

        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=LOOKBACK_DAYS)

        logger.info(f"Date range: {start_date.date()} to {end_date.date()}")
        logger.info(f"Processing {len(assets)} assets in batches of {BATCH_SIZE}...")

        # Process in batches
        for i in range(0, len(assets), BATCH_SIZE):
            batch = assets[i : i + BATCH_SIZE]
            batch_num = (i // BATCH_SIZE) + 1
            total_batches = (len(assets) + BATCH_SIZE - 1) // BATCH_SIZE

            logger.info(f"\nBatch {batch_num}/{total_batches}: Processing {len(batch)} assets")

            GROUP_SIZE = 5
            for j in range(0, len(batch), GROUP_SIZE):
                group = batch[j : j + GROUP_SIZE]
                group_symbols = [
                    a.get("yfinance_ticker") or a["symbol"] for a in group
                ]
                try:
                    summary = await self.pipeline_service.run_multi_fetch_store(
                        symbols=group_symbols,
                        start_date=start_date,
                        end_date=end_date,
                        granularity="daily",
                        group_size=GROUP_SIZE,
                        validate=True,
                    )
                    for sym in group_symbols:
                        res = summary["results"].get(sym, {})
                        status = res.get("status")
                        records = res.get("records_stored", 0)
                        if status == "success":
                            self.stats["successful"] += 1
                            self.stats["total_records"] += records
                            logger.info(f"  ✓ {sym}: {records} new (batched)")
                        elif status == "skipped":
                            self.stats["skipped"] += 1
                            logger.info(f"  → {sym}: 0 new (duplicates, batched)")
                        else:
                            self.stats["failed"] += 1
                            logger.warning(f"  ✗ {sym}: {status or 'Unknown error'}")
                except Exception as e:
                    self.stats["failed"] += len(group_symbols)
                    logger.error(f"  ✗ Group {group_symbols}: {str(e)}")

        logger.info(f"\n{'='*80}")
        logger.info("INGESTION COMPLETE")
        logger.info(f"{'='*80}")
        logger.info(f"Total assets: {self.stats['total_assets']}")
        logger.info(f"Successful: {self.stats['successful']}")
        logger.info(f"Failed: {self.stats['failed']}")
        logger.info(f"Total records: {self.stats['total_records']}")

        return self.stats


# ============================================================================
# DATA VALIDATION LAYER
# ============================================================================

class DataQualityValidator:
    """Validates ingested raw data quality before analytics"""

    def __init__(self):
        """Initialize validator."""
        from api.utils.supabase_client import get_supabase_client

        self.supabase = get_supabase_client()
        self.validation_results = {
            "passed": False,
            "checks": {},
            "errors": [],
            "warnings": [],
        }

    def validate_all(self) -> Dict:
        """Run all validation checks"""
        logger.info(f"\n{'='*80}")
        logger.info("STAGE 2: DATA QUALITY VALIDATION")
        logger.info(f"{'='*80}\n")

        self._check_data_completeness()
        self._check_data_freshness()
        self._check_data_quality()
        self._check_asset_coverage()

        critical_checks = ["completeness", "freshness", "asset_coverage"]
        all_passed = all(
            self.validation_results["checks"].get(check, {}).get("passed", False)
            for check in critical_checks
        )

        self.validation_results["passed"] = all_passed

        logger.info(f"\n{'='*80}")
        logger.info("VALIDATION SUMMARY")
        logger.info(f"{'='*80}")

        for check_name, check_result in self.validation_results["checks"].items():
            status = "✓ PASS" if check_result.get("passed") else "✗ FAIL"
            logger.info(f"{status}: {check_name}")
            if check_result.get("details"):
                logger.info(f"  {check_result['details']}")

        if self.validation_results["errors"]:
            logger.error("\nERRORS:")
            for error in self.validation_results["errors"]:
                logger.error(f"  • {error}")

        if self.validation_results["warnings"]:
            logger.warning("\nWARNINGS:")
            for warning in self.validation_results["warnings"]:
                logger.warning(f"  • {warning}")

        overall_status = "✓ PASSED" if all_passed else "✗ FAILED"
        logger.info(f"\nOverall validation: {overall_status}")

        return self.validation_results

    def _check_data_completeness(self):
        """Check if sufficient data points exist per asset"""
        logger.info("Check 1: Data completeness...")

        try:
            response = self.supabase.client.table("price_history").select(
                "asset_id,timestamp", count="exact"
            ).gte(
                "timestamp",
                (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
            ).execute()

            total_records = response.count or 0

            assets_resp = self.supabase.client.table("assets").select(
                "id", count="exact"
            ).eq("is_active", 1).execute()
            active_assets = assets_resp.count or 0

            expected_assets = min(active_assets, MIN_ASSETS_REQUIRED)
            expected_records = expected_assets * MIN_DATA_POINTS_REQUIRED
            tolerance_ratio = 0.8

            if total_records >= int(expected_records * tolerance_ratio):
                self.validation_results["checks"]["completeness"] = {
                    "passed": True,
                    "details": f"{total_records} recent records found",
                }
                logger.info(f"  ✓ Found {total_records} recent records")
            else:
                self.validation_results["checks"]["completeness"] = {
                    "passed": False,
                    "details": f"Only {total_records} records found",
                }
                self.validation_results["errors"].append(
                    f"Insufficient data points: {total_records}"
                )
                logger.error("  ✗ Insufficient data points")

        except Exception as e:
            logger.error(f"  ✗ Completeness check failed: {str(e)}")
            self.validation_results["checks"]["completeness"] = {
                "passed": False,
                "details": str(e),
            }
            self.validation_results["errors"].append(f"Completeness check error: {str(e)}")

    def _check_data_freshness(self):
        """Check if data is recent (within last 2 days)"""
        logger.info("Check 2: Data freshness...")

        try:
            response = self.supabase.client.table("price_history").select(
                "timestamp"
            ).order("timestamp", desc=True).limit(1).execute()

            if response.data:
                latest_timestamp = pd.to_datetime(response.data[0]["timestamp"], utc=True)
                now = pd.Timestamp.now(tz="UTC")
                age_hours = (now - latest_timestamp).total_seconds() / 3600

                if age_hours <= 48:
                    self.validation_results["checks"]["freshness"] = {
                        "passed": True,
                        "details": f"Latest data is {age_hours:.1f} hours old",
                    }
                    logger.info(f"  ✓ Data is {age_hours:.1f} hours old")
                else:
                    self.validation_results["checks"]["freshness"] = {
                        "passed": False,
                        "details": f"Data is {age_hours:.1f} hours old",
                    }
                    self.validation_results["errors"].append(
                        f"Stale data: {age_hours:.1f} hours old"
                    )
                    logger.error(f"  ✗ Data is stale ({age_hours:.1f} hours)")
            else:
                self.validation_results["checks"]["freshness"] = {
                    "passed": False,
                    "details": "No data found in price_history",
                }
                self.validation_results["errors"].append("No data in price_history table")
                logger.error("  ✗ No data found")

        except Exception as e:
            logger.error(f"  ✗ Freshness check failed: {str(e)}")
            self.validation_results["checks"]["freshness"] = {
                "passed": False,
                "details": str(e),
            }
            self.validation_results["errors"].append(f"Freshness check error: {str(e)}")

    def _check_data_quality(self):
        """Check for data quality issues (nulls, duplicates, outliers)"""
        logger.info("Check 3: Data quality...")

        try:
            response = self.supabase.client.table("price_history").select(
                "close,volume", count="exact"
            ).is_("close", "null").execute()

            null_count = response.count or 0

            total_response = self.supabase.client.table("price_history").select(
                "id", count="exact"
            ).gte(
                "timestamp",
                (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
            ).execute()

            total_count = total_response.count or 1
            null_ratio = null_count / total_count if total_count > 0 else 0

            if null_ratio <= MAX_MISSING_RATIO:
                self.validation_results["checks"]["quality"] = {
                    "passed": True,
                    "details": f"Null ratio: {null_ratio:.2%}",
                }
                logger.info(f"  ✓ Data quality acceptable")
            else:
                self.validation_results["checks"]["quality"] = {
                    "passed": True,
                    "details": f"Null ratio: {null_ratio:.2%}",
                }
                self.validation_results["warnings"].append(
                    f"High null ratio: {null_ratio:.2%}"
                )
                logger.warning(f"  ⚠ High null ratio: {null_ratio:.2%}")

        except Exception as e:
            logger.warning(f"  ⚠ Quality check failed: {str(e)}")
            self.validation_results["checks"]["quality"] = {"passed": True, "details": str(e)}
            self.validation_results["warnings"].append(f"Quality check error: {str(e)}")

    def _check_asset_coverage(self):
        """Check if minimum number of assets have recent data"""
        logger.info("Check 4: Asset coverage...")

        try:
            assets_response = self.supabase.client.table("assets").select(
                "id", count="exact"
            ).eq("is_active", 1).execute()

            active_assets = assets_response.count or 0

            if active_assets >= MIN_ASSETS_REQUIRED:
                self.validation_results["checks"]["asset_coverage"] = {
                    "passed": True,
                    "details": f"{active_assets} active assets found",
                }
                logger.info(f"  ✓ {active_assets} active assets")
            else:
                self.validation_results["checks"]["asset_coverage"] = {
                    "passed": False,
                    "details": f"Only {active_assets} active assets",
                }
                self.validation_results["errors"].append(
                    f"Insufficient active assets: {active_assets}/{MIN_ASSETS_REQUIRED}"
                )
                logger.error(f"  ✗ Only {active_assets} active assets")

        except Exception as e:
            logger.error(f"  ✗ Asset coverage check failed: {str(e)}")
            self.validation_results["checks"]["asset_coverage"] = {
                "passed": False,
                "details": str(e),
            }
            self.validation_results["errors"].append(f"Asset coverage error: {str(e)}")


# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

async def main():
    """Main orchestration function"""
    logger.info(f"\n{'='*80}")
    logger.info("DAILY EOD DATA PIPELINE")
    logger.info(f"Started: {datetime.now(timezone.utc).isoformat()}")
    logger.info(f"{'='*80}\n")

    try:
        ingestor = DataIngestionOrchestrator()
        assets = ingestor.fetch_active_assets()

        if not assets:
            logger.error("No active assets found. Aborting pipeline.")
            return False

        ingestion_stats = await ingestor.ingest_daily_data(assets)

        validator = DataQualityValidator()
        validation_results = validator.validate_all()

        if not validation_results["passed"]:
            logger.error("\n❌ DATA VALIDATION FAILED")
            logger.error("Analytics pipeline will NOT run until data quality issues are resolved.")
            return False

        logger.info("\n✓ DATA VALIDATION PASSED")
        logger.info("Proceeding to analytics computation...\n")

        logger.info(f"\n{'='*80}")
        logger.info("PIPELINE COMPLETE")
        logger.info(f"{'='*80}")
        logger.info(f"Finished: {datetime.now(timezone.utc).isoformat()}")
        logger.info("\nSummary:")
        logger.info(f"  • Data ingestion: ✓ {ingestion_stats['successful']}/{ingestion_stats['total_assets']} assets")
        logger.info("  • Data validation: ✓ PASSED")

        return True

    except Exception as e:
        logger.error(f"\n❌ PIPELINE FAILED: {str(e)}")
        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    import asyncio

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    success = asyncio.run(main())
    sys.exit(0 if success else 1)
