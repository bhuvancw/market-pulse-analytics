-- MARKET PULSE ANALYTICS — SQLite3 Database Schema
--
-- Star Schema Design:
--   Dimension table  : dim_ticker  (ticker master)
--   Fact tables      : fact_daily, fact_monthly, fact_sector,
--                      fact_forecast, ml_metrics

DROP TABLE IF EXISTS dim_ticker;
DROP TABLE IF EXISTS fact_daily;
DROP TABLE IF EXISTS fact_monthly;
DROP TABLE IF EXISTS fact_sector;
DROP TABLE IF EXISTS fact_forecast;
DROP TABLE IF EXISTS ml_metrics;

-- ── Dimension: Ticker Master ──────────────────────────────────────
CREATE TABLE dim_ticker (
    ticker        TEXT PRIMARY KEY,
    company_name  TEXT NOT NULL,
    sector        TEXT NOT NULL,
    sub_sector    TEXT,
    exchange      TEXT,
    currency      TEXT DEFAULT 'USD'
);

-- ── Fact: Daily OHLCV + Features ─────────────────────────────────
CREATE TABLE fact_daily (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    date                 TEXT    NOT NULL,
    ticker               TEXT    NOT NULL,
    sector               TEXT,
    open_price           REAL,
    high_price           REAL,
    low_price            REAL,
    close_price          REAL    NOT NULL,
    volume               INTEGER,
    daily_return         REAL,
    cumulative_return    REAL,
    ma_20                REAL,
    ma_50                REAL,
    ma_200               REAL,
    volatility_30d       REAL,
    volatility_ann       REAL,
    rsi_14               REAL,
    vwap                 REAL,
    bb_upper             REAL,
    bb_lower             REAL,
    bb_width             REAL,
    bb_pct               REAL,
    drawdown             REAL,
    above_ma50           INTEGER,
    above_ma200          INTEGER,
    golden_cross         INTEGER,
    rsi_zone             TEXT,
    year                 INTEGER,
    month                INTEGER,
    quarter              INTEGER,
    month_name           TEXT,
    year_month           TEXT,
    week                 INTEGER,
    day_name             TEXT,
    UNIQUE(ticker, date),
    FOREIGN KEY (ticker) REFERENCES dim_ticker(ticker)
);

-- ── Fact: Monthly Summary per Ticker ─────────────────────────────
CREATE TABLE fact_monthly (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker             TEXT    NOT NULL,
    sector             TEXT,
    year               INTEGER NOT NULL,
    month              INTEGER NOT NULL,
    quarter            INTEGER,
    month_name         TEXT,
    year_month         TEXT,
    open_price         REAL,
    close_price        REAL,
    high_price         REAL,
    low_price          REAL,
    avg_close          REAL,
    total_volume       INTEGER,
    avg_volume         REAL,
    monthly_return     REAL,
    avg_daily_return   REAL,
    monthly_volatility REAL,
    avg_volatility     REAL,
    max_drawdown       REAL,
    end_rsi            REAL,
    avg_rsi            REAL,
    end_ma50           REAL,
    end_ma200          REAL,
    golden_cross       INTEGER,
    mom_pct_change     REAL,
    trading_days       INTEGER,
    UNIQUE(ticker, year, month),
    FOREIGN KEY (ticker) REFERENCES dim_ticker(ticker)
);

-- ── Fact: Sector Monthly ──────────────────────────────────────────
CREATE TABLE fact_sector (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    sector           TEXT    NOT NULL,
    year             INTEGER NOT NULL,
    month            INTEGER NOT NULL,
    quarter          INTEGER,
    year_month       TEXT,
    avg_close        REAL,
    avg_daily_return REAL,
    avg_volatility   REAL,
    avg_rsi          REAL,
    max_drawdown     REAL,
    total_volume     INTEGER,
    ticker_count     INTEGER,
    avg_ma50         REAL,
    avg_ma200        REAL,
    UNIQUE(sector, year, month)
);

-- ── Fact: ML Forecasts ────────────────────────────────────────────
CREATE TABLE fact_forecast (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker           TEXT    NOT NULL,
    forecast_date    TEXT    NOT NULL,
    predicted_close  REAL,
    horizon_days     INTEGER,
    model_type       TEXT DEFAULT 'LinearRegression',
    created_at       TEXT DEFAULT (datetime('now')),
    UNIQUE(ticker, forecast_date, horizon_days)
);

-- ── ML Model Performance Metrics ─────────────────────────────────
CREATE TABLE ml_metrics (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker        TEXT,
    horizon       TEXT,
    horizon_days  INTEGER,
    train_r2      REAL,
    test_r2       REAL,
    test_mae      REAL,
    test_rmse     REAL,
    test_mape     REAL
);