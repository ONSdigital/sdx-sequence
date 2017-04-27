"""Scalable service for generating sequences for SDX (backed by MongoDB)."""
import settings
import logging.handlers
import os
import psycopg2
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence
from sqlalchemy.exc import SQLAlchemyError
from structlog import wrap_logger


__version__ = "1.3.1"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


logging.basicConfig(level=settings.LOGGING_LEVEL, format=settings.LOGGING_FORMAT)
logger = wrap_logger(logging.getLogger(__name__))
logger.debug("START", version=__version__)


sequence = Sequence("sequence")
batch_sequence = Sequence("batch_sequence")
image_sequence = Sequence("image_sequence")
json_sequence = Sequence("json_sequence")


def _get_next_sequence(seq):
    logger.debug("Obtaining next sequence number")
    try:
        logger.debug("Getting DB connection")
        result = db.engine.execute(seq.next_value())
        logger.debug("Executing get next value on sequence")
        sequence_no = result.first()[0]
        logger.debug("Database sequence no is: {}".format(sequence_no))
        return sequence_no
    except (psycopg2.Error, SQLAlchemyError) as e:
        logger.error("Error executing sequence")
        logger.exception(e)
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
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    # Startup
    app.logger.info("Starting server: version='{}'".format(__version__))
    port = int(os.getenv("PORT"))
    app.run(debug=True, host='0.0.0.0', port=port)
