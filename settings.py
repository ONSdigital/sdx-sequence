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


def get_env():
    """Evaluates DB_URL in a variety of environments in a testable manner"""
    try:
        if os.getenv("CF_DEPLOYMENT", False):
            vcap_services = os.getenv("VCAP_SERVICES")
            parsed_vcap_services = json.loads(vcap_services)
            globals()['DB_URL'] = parsed_vcap_services.get('rds').get('credentials').get('uri')
        else:
            db_host = _get_value("SDX_SEQUENCE_POSTGRES_HOST")
            db_port = _get_value('SDX_SEQUENCE_POSTGRES_PORT')
            db_name = _get_value('SDX_SEQUENCE_POSTGRES_NAME')
            db_user = _get_value('SDX_SEQUENCE_POSTGRES_USER')
            db_password = _get_value('SDX_SEQUENCE_POSTGRES_PASSWORD')
            globals()['DB_URL'] = 'postgres://{}:{}@{}:{}/{}'.format(db_user, db_password, db_host, db_port, db_name)

    except ValueError:
        logger.error("Unable to start service - DB connection details not set")

get_env()

