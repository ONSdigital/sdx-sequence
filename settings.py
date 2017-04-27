import logging
import os

logger = logging.getLogger(__name__)

LOGGING_FORMAT = "%(asctime)s|%(levelname)s: sdx-sequence: %(message)s"
LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'DEBUG'))


DB_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
DB_PORT = os.getenv('POSTGRES_PORT', '15432')
DB_NAME = os.getenv('POSTGRES_NAME', 'sdx')
DB_USER = os.getenv('POSTGRES_USER', 'sdx')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'secret')

DB_URL = 'postgres://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
