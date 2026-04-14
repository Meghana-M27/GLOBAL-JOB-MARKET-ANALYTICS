"""
backend/middleware/logger.py
Request/response logging middleware.
"""
import time
import logging
import os

LOG_DIR  = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('gjm')

def log_request(endpoint, params=None, duration_ms=None):
    msg = f"[REQUEST] {endpoint}"
    if params:   msg += f" | params={params}"
    if duration_ms: msg += f" | {duration_ms:.1f}ms"
    logger.info(msg)

def log_error(endpoint, error):
    logger.error(f"[ERROR] {endpoint} | {error}")

def log_db_query(sql, params=None):
    short = sql.strip().replace('\n',' ')[:80]
    logger.debug(f"[SQL] {short} | params={params}")

class Timer:
    """Context manager to measure execution time."""
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, *args):
        self.elapsed_ms = (time.time() - self.start) * 1000

    @property
    def ms(self):
        return round(self.elapsed_ms, 2)
