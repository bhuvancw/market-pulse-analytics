# Market Pulse Analytics

A personal analytics project I built to understand how financial data 
pipelines work in practice.

The idea was simple: instead of using a static CSV from Kaggle, build a 
system that pulls real market data, stores it properly, runs business-focused 
analysis, and updates itself automatically.

---

## What This Project Does

- Fetches 5 years of daily stock data for 12 equities across 4 sectors
- Stores and structures data in a SQLite database (star schema)
- Runs SQL-based KPI analysis: sector performance, risk ranking, signal scanning
- Forecasts price trends using Linear Regression (30/90/180-day horizons)
- Visualizes everything in a Power BI executive dashboard
- Refreshes automatically every weekday after market close

---

## Tech Stack

Python · Pandas · SQLite3 · SQL · Scikit-learn · Power BI · Git

---

## Status

Actively building. Notebooks 1-5 complete. Dashboard in progress.