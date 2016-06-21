import settings
import json
import html
import logging
import logging.handlers
from flask import Flask, request, Response, jsonify, abort
from pymongo import MongoClient
import pymongo.errors
from datetime import datetime
from bson.objectid import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)

app.config['MONGODB_URL'] = settings.MONGODB_URL
logger = settings.logger

mongo_client = MongoClient(app.config['MONGODB_URL'])
db = mongo_client.sdx_sequences


def get_next_sequence(seq_name):
    next_sequence = db.sequences.find_and_modify(query={'seq_name': seq_name},
                                       update={'$inc': {'sequence': 1}},
                                       upsert=True, new=True)
    sequence_no = next_sequence['sequence']
    return sequence_no


@app.route('/sequence', methods=['GET'])
def do_get_sequence():
    sequence_no = get_next_sequence('sequence')
    return jsonify({'sequence_no': sequence_no})


@app.route('/batch-sequence', methods=['GET'])
def do_get_batch_sequence():
    sequence_no = get_next_sequence('batch-sequence')
    return jsonify({'sequence_no': sequence_no})


@app.route('/image-sequence', methods=['GET'])
def do_get_image_sequence():
    sequence_no = get_next_sequence('image-sequence')
    return jsonify({'sequence_no': sequence_no})


if __name__ == '__main__':
    # Startup
    logging.basicConfig(level=settings.LOGGING_LEVEL,
                        format=settings.LOGGING_FORMAT)
    app.run(debug=True, host='0.0.0.0', port=5000)
