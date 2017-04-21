"""Scalable service for generating sequences for SDX (backed by PostgreSQL)."""
import settings
import sys
import logging
import logging.handlers
import os
from flask import Flask, jsonify

from pgsequences import get_dsn
from pgsequences import SequenceStore
from pgsequences import ProcessSafePoolManager

logger = settings.logger

app = Flask(__name__)
pm = ProcessSafePoolManager(**get_dsn(settings))


def create_sequences():
    con = pm.getconn()
    for seq in ("sequence", "batch_sequence", "image_sequence", "json_sequence"):
        SequenceStore.Creation(seq).run(con)
    pm.putconn(con)


@app.route('/sequence', methods=['GET'])
def do_get_sequence():
    """Get the next sequence number. Starts at 1000 and increments to 9999."""
    con = pm.getconn()
    rv = SequenceStore.Query("sequence").run(con)
    pm.putconn(con)

    return jsonify({'sequence_no': rv})


@app.route('/batch-sequence', methods=['GET'])
def do_get_batch_sequence():
    """Get the next batch sequence number. Starts at 30000 and increments to 39999."""
    con = pm.getconn()
    rv = SequenceStore.Query("batch_sequence").run(con)
    pm.putconn(con)

    return jsonify({'sequence_no': rv})


@app.route('/image-sequence', methods=['GET'])
def do_get_image_sequence():
    """Get the next batch sequence number. Starts at 1 and increments to 999999999."""
    con = pm.getconn()
    rv = SequenceStore.Query("image_sequence").run(con)
    pm.putconn(con)

    return jsonify({'sequence_no': rv})


@app.route('/json-sequence', methods=['GET'])
def do_get_json_sequence():
    """Get the next sequence number for json files. Starts at 1 and increments to 999999999."""
    con = pm.getconn()
    rv = SequenceStore.Query("json_sequence").run(con)
    pm.putconn(con)

    return jsonify({'sequence_no': rv})


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
