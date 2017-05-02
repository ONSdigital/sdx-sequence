import logging
import os

logger = logging.getLogger(__name__)

LOGGING_FORMAT = "%(message)s"
LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'DEBUG'))


def _get_value(key):
    value = os.getenv(key)
    if not value:
        raise ValueError("No value set for " + key)
    else:
        return value

try:
    DB_HOST = _get_value("POSTGRES_HOST")
    DB_PORT = _get_value('POSTGRES_PORT')
    DB_NAME = _get_value('POSTGRES_NAME')
    DB_USER = _get_value('POSTGRES_USER')
    DB_PASSWORD = _get_value('POSTGRES_PASSWORD')
    DB_URL = 'postgres://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

except ValueError as e:
    logger.error("Unable to start service - DB connection details not set")
    raise RuntimeError(e)
