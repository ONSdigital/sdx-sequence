"""Scalable service for generating sequences for SDX (backed by PostgreSQL)."""
import settings
import sys
import logging
import logging.handlers
import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

logger = settings.logger

SQL_GET_SEQUENCE = """
    SELECT nextval(%(sequence_type)s)
"""

db = None

db_config = {'host': settings.DB_HOST,
             'port': settings.DB_PORT,
             'database': settings.DB_NAME,
             'password': settings.DB_PASSWORD,
             'user': settings.DB_USER}


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


def use_db(func=None):
    def inner(*args, **kwargs):
        global db
        if not db:
            db = connect(db_config)
        return func(*args, **kwargs)
    return inner


@use_db
def get_next_sequence(seq_name):
    """Get the next sequence number from the database."""
    with db() as cursor:
        cursor.execute(SQL_GET_SEQUENCE,
                       {'sequence_type': '%s' % seq_name})

        return cursor.fetchone()[0]


@app.before_first_request
def _run_on_start():

    # Create sequences if they don't exist
    with db() as cursor:
        cursor.execute("""SELECT 0 FROM pg_class where relname = 'sequence'""")
        if not cursor.fetchone():
            cursor.execute("""CREATE SEQUENCE "sequence" MINVALUE 1000 MAXVALUE 9999 CYCLE;""")

    with db() as cursor:
        cursor.execute("""SELECT 0 FROM pg_class where relname = 'batch-sequence'""")
        if not cursor.fetchone():
            cursor.execute("""CREATE SEQUENCE "batch-sequence" MINVALUE 30000 MAXVALUE 39999 CYCLE;""")

    with db() as cursor:
        cursor.execute("""SELECT 0 FROM pg_class where relname = 'image-sequence'""")
        if not cursor.fetchone():
            cursor.execute("""CREATE SEQUENCE "image-sequence" MINVALUE 1 MAXVALUE 999999999 CYCLE;""")


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
