
import os

ETH_RETRY_DISABLED = bool(os.environ.get("ETH_RETRY_DISABLED"))
ETH_RETRY_DEBUG = bool(os.environ.get("ETH_RETRY_DEBUG"))
ETH_RETRY_SUPPRESS_LOGS = int(os.environ.get("ETH_RETRY_SUPPRESS_LOGS", 0))
MIN_SLEEP_TIME = int(os.environ.get("MIN_SLEEP_TIME", 5))
MAX_SLEEP_TIME = int(os.environ.get("MAX_SLEEP_TIME", 15))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", 10))
# NOTE: this will suppress logs up to `` times, then they will log as usual
