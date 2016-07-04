import logging
import os

logger = logging.getLogger(__name__)

LOGGING_FORMAT = "%(asctime)s|%(levelname)s: sdx-sequence: %(message)s"
LOGGING_LOCATION = "logs/sdx-sequence.log"
LOGGING_LEVEL = logging.DEBUG

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
