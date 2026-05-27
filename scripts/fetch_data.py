import os
import sys
import sqlite3
import logging
import warnings
import time
from datetime import datetime, timedelta

import yfinance as yf
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

# Set working directory to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

from config.settings import (
    TICKERS, SECTOR_MAP, DB_PATH, LOG_PATH,
    API_CALL_DELAY_SECONDS
)

# ── Logging ──────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="a"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("fetch_data")


def fetch_recent(ticker, days_back=7):
    """Download last N days of data for a ticker."""

    end   = datetime.today().strftime("%Y-%m-%d")
    start = (datetime.today() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    try:
        raw = yf.download(ticker, start=start, end=end,
                          auto_adjust=True, progress=False, show_errors=False)

        if raw is None or raw.empty:
            logger.warning(f"  No data returned for {ticker}")
            return None

        raw = raw.reset_index()

        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = [col[0] for col in raw.columns]

        raw.columns = [str(c).lower().strip() for c in raw.columns]
        raw["date"]   = pd.to_datetime(raw["date"]).astype(str)
        raw["ticker"] = ticker
        raw["sector"] = SECTOR_MAP.get(ticker, "Unknown")
        raw           = raw.dropna(subset=["close"])

        col_map = {"open": "open_price", "high": "high_price",
                   "low":  "low_price",  "close": "close_price"}
        raw = raw.rename(columns=col_map)

        logger.info(f"  ✓ {ticker}: {len(raw)} rows")
        return raw

    except Exception as e:
        logger.error(f"  ✗ {ticker}: {e}")
        return None


def upsert_rows(df, conn):
    """Insert rows into fact_daily, replacing duplicates on (ticker, date)."""

    cols         = ["date", "ticker", "sector",
                    "open_price", "high_price", "low_price",
                    "close_price", "volume"]
    available    = [c for c in cols if c in df.columns]
    placeholders = ", ".join(["?" for _ in available])
    col_str      = ", ".join(available)
    sql          = (f"INSERT OR REPLACE INTO fact_daily ({col_str}) "
                    f"VALUES ({placeholders})")

    for _, row in df[available].iterrows():
        conn.execute(sql, tuple(row))

    conn.commit()


def run():
    """Main daily refresh pipeline."""

    logger.info("=" * 55)
    logger.info(f"DAILY REFRESH STARTED — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    logger.info("=" * 55)

    if not os.path.exists(DB_PATH):
        logger.error(f"Database not found: {DB_PATH}. Run notebooks 01-04 first.")
        return

    conn    = sqlite3.connect(DB_PATH)
    success = 0
    failed  = []

    for ticker in TICKERS:

        df = fetch_recent(ticker, days_back=7)

        if df is not None:
            try:
                upsert_rows(df, conn)
                success += 1
            except Exception as e:
                logger.error(f"  DB error for {ticker}: {e}")
                failed.append(ticker)
        else:
            failed.append(ticker)

        time.sleep(API_CALL_DELAY_SECONDS)

    conn.close()

    logger.info("=" * 55)
    logger.info(f"REFRESH COMPLETE")
    logger.info(f"  Success : {success}/{len(TICKERS)}")
    logger.info(f"  Failed  : {failed if failed else 'None'}")
    logger.info("=" * 55)


if __name__ == "__main__":
    run()