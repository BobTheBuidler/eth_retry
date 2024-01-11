
import os

ETH_RETRY_DISABLED = bool(os.environ.get("ETH_RETRY_DISABLED"))
ETH_RETRY_DEBUG = bool(os.environ.get("ETH_RETRY_DEBUG"))
MIN_SLEEP_TIME = int(os.environ.get("MIN_SLEEP_TIME", 10))
MAX_SLEEP_TIME = int(os.environ.get("MAX_SLEEP_TIME", 20))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", 10))
