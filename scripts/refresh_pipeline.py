import os
import sys
import logging
import schedule
import time
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

from config.settings import REFRESH_TIME_DAILY, LOG_PATH
from scripts.fetch_data import run as daily_run

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, mode="a"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("scheduler")


def job():
    """Scheduled job — skips weekends."""

    weekday = datetime.today().weekday()
    if weekday >= 5:
        logger.info("Weekend — skipping refresh")
        return

    logger.info("Scheduled job triggered")
    try:
        daily_run()
    except Exception as e:
        logger.error(f"Scheduled job failed: {e}")


schedule.every().day.at(REFRESH_TIME_DAILY).do(job)

logger.info(f"Scheduler active — daily job at {REFRESH_TIME_DAILY}")
logger.info("Press Ctrl+C to stop")

while True:
    schedule.run_pending()
    time.sleep(60)