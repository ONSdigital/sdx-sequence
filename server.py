"""Scalable service for generating sequences for SDX (backed by Postgres)."""
import datetime
import logging.handlers
import os

from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, event, select
from sqlalchemy.exc import SQLAlchemyError
from structlog import wrap_logger
from structlog.processors import JSONRenderer
from structlog.stdlib import filter_by_level, add_log_level
import psycopg2

import settings
from sequences import sequence, batch_sequence, image_sequence, json_sequence
from sdx.common.logger_config import logger_initial_config

__service__ = "sdx-sequence"
__version__ = "2.0.0"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def add_timestamp(_, __, event_dict):
    event_dict['created'] = datetime.datetime.utcnow().isoformat()
    return event_dict


def add_service_and_version(_, __, event_dict):
    event_dict['service'] = __service__
    event_dict['version'] = __version__
    return event_dict

logger_initial_config(service_name='sdx-sequence', log_level=settings.LOGGING_LEVEL)
logger = wrap_logger(logging.getLogger(__name__),
                     processors=[add_log_level,
                                 filter_by_level,
                                 add_timestamp,
                                 add_service_and_version,
                                 JSONRenderer(indent=1, sort_keys=True)])
logger.info("START", version=__version__)


def _get_next_sequence(seq):
    logger.debug("Obtaining next sequence number")
    try:
        logger.debug("Getting DB connection")
        result = db.engine.execute(seq.next_value())
        logger.debug("Executing get next value on sequence")
        sequence_no = result.first()[0]
        logger.debug("Retrieved sequence", sequence=sequence_no)
        return sequence_no
    except (psycopg2.Error, SQLAlchemyError) as e:
        logger.error("Error executing sequence", exception=str(e))
        return abort(500)


@app.route('/sequence', methods=['GET'])
def do_get_sequence():
    """Get the next sequence number. Starts at 1000 and increments to 9999."""
    sequence_no = _get_next_sequence(sequence)

    # Sequence numbers start at 1000 and increment to 9999
    sequence_start = 1000
    sequence_range = 9000

    sequence_no = (sequence_no - 1) % sequence_range + sequence_start

    return jsonify({'sequence_no': sequence_no})


@app.route('/batch-sequence', methods=['GET'])
def do_get_batch_sequence():
    """Get the next batch sequence number. Starts at 30000 and increments to 39999."""
    sequence_no = _get_next_sequence(batch_sequence)

    sequence_start = 30000
    sequence_range = 10000

    sequence_no = (sequence_no - 1) % sequence_range + sequence_start

    return jsonify({'sequence_no': sequence_no})


@app.route('/image-sequence', methods=['GET'])
def do_get_image_sequence():
    """Get the next batch sequence number. Starts at 1 and increments to 999999999."""
    sequence_no = _get_next_sequence(image_sequence)

    # start = 1
    sequence_range = 1000000000

    sequence_no = sequence_no % sequence_range

    return jsonify({'sequence_no': sequence_no})


@app.route('/json-sequence', methods=['GET'])
def do_get_json_sequence():
    """Get the next sequence number for json files. Starts at 1 and increments to 999999999."""
    sequence_no = _get_next_sequence(json_sequence)

    # start = 1
    sequence_range = 1000000000

    sequence_no = sequence_no % sequence_range

    return jsonify({'sequence_no': sequence_no})


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    try:
        conn = db.engine.connect()
        test_sql(conn)
    except SQLAlchemyError as e:
        logger.error("Failed to connect to database", exception=str(e))
        abort(500)
    return jsonify({'status': 'OK'})


@event.listens_for(db.engine, "engine_connect")
def test_connection(connection, branch):
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother testing on these.
        return

    save_should_close_with_result = connection.should_close_with_result
    connection.should_close_with_result = False
    try:
        logger.debug("Testing pooled connection")
        test_sql(connection)
        logger.debug("Connection successful")
    except exc.DBAPIError:
        try:
            logger.warning("Pooled connection failed - retrying")
            # try it again, this will recreate a stale or broke connection
            connection.scalar(select([1]))
            logger.debug("Connection successful")
        except exc.DBAPIError:
            # However if we get a database err again, forcibly close the connection
            logger.warning("Connection failed again - removing from pool")
            connection.close()
    finally:
        # restore "close with result"
        connection.should_close_with_result = save_should_close_with_result


def test_sql(connection):
    # Run a SELECT 1 to test the database connection
    logger.debug("Executing select 1")
    connection.scalar(select([1]))


if __name__ == '__main__':
    # Startup
    app.logger.info("Starting server: version='{}'".format(__version__))
    port = int(os.getenv("PORT"))
    app.run(debug=True, host='0.0.0.0', port=port)
