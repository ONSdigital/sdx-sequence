"""Scalable service for generating sequences for SDX (backed by PostgreSQL)."""
import settings
import sys
import logging
import logging.handlers
import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

app.config['DB_HOST'] = settings.DB_HOST
app.config['DB_PORT'] = settings.DB_PORT
app.config['DB_NAME'] = settings.DB_NAME
app.config['DB_USER'] = settings.DB_USER
app.config['DB_PASSWORD'] = settings.DB_PASSWORD

logger = settings.logger

SQL_GET_SEQUENCE = """
    SELECT nextval(%(sequence_type)s)
"""


def connect(params):
    def factory():
        try:
            with factory.connection.cursor() as cursor:
                cursor.execute('SELECT 1')
        except psycopg2.OperationalError as e:
            factory.connection = psycopg2.connect(**params)
            factory.connection.autocommit = True

        return factory.connection.cursor()

    factory.connection = psycopg2.connect(**params)
    factory.connection.autocommit = True

    return factory


db = connect(
    dict(host=app.config['DB_HOST'],
         port=app.config['DB_PORT'],
         database=app.config['DB_NAME'],
         password=app.config['DB_PASSWORD'],
         user=app.config['DB_USER']))


def get_next_sequence(seq_name):
    """Get the next sequence number from the database."""
    with db() as cursor:
        cursor.execute(SQL_GET_SEQUENCE,
                       {'sequence_type': '%s' % seq_name})

        return cursor.fetchone()[0]


@app.route('/sequence', methods=['GET'])
def do_get_sequence():
    """Get the next sequence number. Starts at 1000 and increments to 9999."""
    sequence_no = get_next_sequence('sequence')

    # Sequence numbers start at 1000 and increment to 9999
    sequence_start = 1000
    sequence_range = 9000

    sequence_no = (sequence_no - 1) % sequence_range + sequence_start

    return jsonify({'sequence_no': sequence_no})


@app.route('/batch-sequence', methods=['GET'])
def do_get_batch_sequence():
    """Get the next batch sequence number. Starts at 30000 and increments to 39999."""
    sequence_no = get_next_sequence('batch-sequence')

    sequence_start = 30000
    sequence_range = 10000

    sequence_no = (sequence_no - 1) % sequence_range + sequence_start

    return jsonify({'sequence_no': sequence_no})


@app.route('/image-sequence', methods=['GET'])
def do_get_image_sequence():
    """Get the next batch sequence number. Starts at 1 and increments to 999999999."""
    sequence_no = get_next_sequence('image-sequence')

    # start = 1
    sequence_range = 1000000000

    sequence_no = sequence_no % sequence_range

    return jsonify({'sequence_no': sequence_no})


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    # Startup
    logging.basicConfig(level=settings.LOGGING_LEVEL, format=settings.LOGGING_FORMAT)
    handler = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(handler)
    port = int(os.getenv("PORT"))
    app.run(debug=True, host='0.0.0.0', port=port)
