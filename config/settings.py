# config/settings.py
# ─────────────────────────────────────────────────────────────────
# Project-wide configuration settings
# Non-sensitive — safe to push to GitHub
# ─────────────────────────────────────────────────────────────────

import datetime

# ── Stock Universe ────────────────────────────────────────────────
# 12 stocks across 4 sectors

TICKERS = [
    "AAPL",   # Apple Inc.             — Technology
    "MSFT",   # Microsoft Corporation  — Technology
    "GOOGL",  # Alphabet Inc.          — Technology
    "JPM",    # JPMorgan Chase         — Financials
    "GS",     # Goldman Sachs          — Financials
    "BAC",    # Bank of America        — Financials
    "JNJ",    # Johnson & Johnson      — Healthcare
    "PFE",    # Pfizer Inc.            — Healthcare
    "XOM",    # ExxonMobil             — Energy
    "CVX",    # Chevron Corporation    — Energy
    "AMZN",   # Amazon.com             — Consumer
    "WMT",    # Walmart Inc.           — Consumer
]

SECTOR_MAP = {
    "AAPL":  "Technology",
    "MSFT":  "Technology",
    "GOOGL": "Technology",
    "JPM":   "Financials",
    "GS":    "Financials",
    "BAC":   "Financials",
    "JNJ":   "Healthcare",
    "PFE":   "Healthcare",
    "XOM":   "Energy",
    "CVX":   "Energy",
    "AMZN":  "Consumer",
    "WMT":   "Consumer",
}

COMPANY_NAMES = {
    "AAPL":  "Apple Inc.",
    "MSFT":  "Microsoft Corporation",
    "GOOGL": "Alphabet Inc.",
    "JPM":   "JPMorgan Chase & Co.",
    "GS":    "Goldman Sachs Group",
    "BAC":   "Bank of America Corp.",
    "JNJ":   "Johnson & Johnson",
    "PFE":   "Pfizer Inc.",
    "XOM":   "ExxonMobil Corporation",
    "CVX":   "Chevron Corporation",
    "AMZN":  "Amazon.com Inc.",
    "WMT":   "Walmart Inc.",
}

SUB_SECTOR_MAP = {
    "AAPL":  "Consumer Electronics",
    "MSFT":  "Enterprise Software",
    "GOOGL": "Internet Services",
    "JPM":   "Banking",
    "GS":    "Investment Banking",
    "BAC":   "Banking",
    "JNJ":   "Pharmaceuticals",
    "PFE":   "Biotechnology",
    "XOM":   "Oil & Gas",
    "CVX":   "Oil & Gas",
    "AMZN":  "E-Commerce & Cloud",
    "WMT":   "Retail",
}

# ── Date Range ────────────────────────────────────────────────────
START_DATE = "2020-01-01"
END_DATE   = datetime.date.today().strftime("%Y-%m-%d")

# ── ML Configuration ──────────────────────────────────────────────
LOOKBACK_DAYS = 60             # 60-day rolling window (~1 quarter)
TRAIN_SPLIT_RATIO = 0.80       # 80% train, 20% test

# Forecast horizons
FORECAST_HORIZON_SHORT  = 30   # 30 trading days  — tactical view
FORECAST_HORIZON_MEDIUM = 90   # 90 trading days  — quarterly planning
FORECAST_HORIZON_LONG   = 180  # 180 trading days — semi-annual outlook

# ── File Paths ────────────────────────────────────────────────────
DB_PATH             = "data/market_pulse.db"
LOG_PATH            = "logs/pipeline.log"
RAW_DATA_PATH       = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"
MODEL_PATH          = "models/lr_model.pkl"

# ── Pipeline Behavior ─────────────────────────────────────────────
API_CALL_DELAY_SECONDS = 1.0       # pause between ticker fetches
REFRESH_TIME_DAILY     = "18:30"   # 6:30 PM — 90 min after US market close