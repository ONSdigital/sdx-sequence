"""Scalable service for generating sequences for SDX (backed by MongoDB)."""
import settings
import sys
import logging
import logging.handlers
import os
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

app.config['MONGODB_URL'] = settings.MONGODB_URL
logger = settings.logger

mongo_client = MongoClient(app.config['MONGODB_URL'])
db = mongo_client.sdx_sequences


def get_next_sequence(seq_name):
    """Get the next sequence number from the database."""
    next_sequence = db.sequences.find_and_modify(query={'seq_name': seq_name},
                                                 update={'$inc': {'sequence': 1}},
                                                 upsert=True, new=True)

    return next_sequence['sequence']


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
