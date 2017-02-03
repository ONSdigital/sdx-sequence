import logging
import os

logger = logging.getLogger(__name__)

LOGGING_FORMAT = "%(asctime)s|%(levelname)s: sdx-sequence: %(message)s"
LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'DEBUG'))

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '15432')
DB_NAME = os.getenv('DB_NAME', 'sdx')
DB_USER = os.getenv('DB_USER', 'sdx')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'secret')
