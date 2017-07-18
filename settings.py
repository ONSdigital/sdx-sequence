import logging
import os
from sdx.common.logger_config import logger_initial_config

logger_initial_config(service_name='sdx-sequence')
logger = logging.getLogger(__name__)
LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'DEBUG'))


def _get_value(key):
    value = os.getenv(key)
    if not value:
        logger.error("No value set for {}".format(key))
        raise ValueError()
    else:
        return value

try:
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "sdx"
    DB_USER = "sdx"
    DB_PASSWORD = "sdx"
    # DB_HOST = _get_value("SDX_SEQUENCE_POSTGRES_HOST")
    # DB_PORT = _get_value('SDX_SEQUENCE_POSTGRES_PORT')
    # DB_NAME = _get_value('SDX_SEQUENCE_POSTGRES_NAME')
    # DB_USER = _get_value('SDX_SEQUENCE_POSTGRES_USER')
    # DB_PASSWORD = _get_value('SDX_SEQUENCE_POSTGRES_PASSWORD')
    DB_URL = 'postgres://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

except ValueError:
    logger.error("Unable to start service - DB connection details not set")
