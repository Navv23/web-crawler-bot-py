import os

BROWSERS = ['edge', 'chrome']
PLATFORMS = ['pc']

MAX_RETRIES = 3
DEFAULT_TIMEOUT = 20
REQUEST_COUNT = 0

MIN_DELAY = 1
MAX_DELAY = 3

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')