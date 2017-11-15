import json
import logging
import os
from structlog import wrap_logger

LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'DEBUG'))
LOGGING_FORMAT = "%(asctime)s.%(msecs)06dZ|%(levelname)s: sdx-sequence: %(message)s"

logging.basicConfig(format=LOGGING_FORMAT,
                    datefmt="%Y-%m-%dT%H:%M:%S",
                    level=LOGGING_LEVEL)

logger = wrap_logger(
    logging.getLogger(__name__)
)


def _get_value(key):
    value = os.getenv(key)
    if not value:
        logger.error("No value set for {}".format(key))
        raise ValueError()
    else:
        return value

try:
    if os.getenv("CF_DEPLOYMENT", False):
        vcap_services = os.getenv("VCAP_SERVICES")
        parsed_vcap_services = json.loads(vcap_services)
        rds_config = parsed_vcap_services.get('rds')
        DB_URL = rds_config[0].get('credentials').get('uri')
    else:
        DB_HOST = _get_value("SDX_SEQUENCE_POSTGRES_HOST")
        DB_PORT = _get_value('SDX_SEQUENCE_POSTGRES_PORT')
        DB_NAME = _get_value('SDX_SEQUENCE_POSTGRES_NAME')
        DB_USER = _get_value('SDX_SEQUENCE_POSTGRES_USER')
        DB_PASSWORD = _get_value('SDX_SEQUENCE_POSTGRES_PASSWORD')
        DB_URL = 'postgres://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

except ValueError:
    logger.error("Unable to start service - DB connection details not set")
