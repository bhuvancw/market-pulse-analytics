import os
import sys
import sqlite3
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

from config.settings import DB_PATH

EXPORT_DIR = "dashboards/data_exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

TABLES = [
    "dim_ticker",
    "fact_daily",
    "fact_monthly",
    "fact_sector",
    "fact_forecast",
    "ml_metrics",
]

conn = sqlite3.connect(DB_PATH)

print("Exporting SQLite tables to CSV for Power BI...")

for table in TABLES:
    try:
        df   = pd.read_sql(f"SELECT * FROM {table}", conn)
        path = f"{EXPORT_DIR}/{table}.csv"
        df.to_csv(path, index=False)
        print(f"  ✓ {table}: {len(df):,} rows → {path}")
    except Exception as e:
        print(f"  ✗ {table}: {e}")

conn.close()
print("\n✓ All exports complete. Refresh Power BI to update visuals.")