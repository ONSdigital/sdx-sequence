from server import app
import unittest
import json
import mock

import pgsequences
import server
import testing.postgresql

class TestSequenceService(unittest.TestCase):

    sequence_endpoint = "/sequence"
    batch_sequence_endpoint = "/batch-sequence"
    image_sequence_endpoint = "/image-sequence"
    json_sequence_endpoint = "/json-sequence"

    @classmethod
    def setUpClass(cls):
        cls.pm = server.pm

    def setUp(self):
        self.db = testing.postgresql.Postgresql()
        self.pm.kwargs = self.db.dsn()
        server.create_sequences()

        # creates a test client
        self.app = app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        self.pm.closeall()
        self.db.stop()

    def test_increments_sequence(self):
        seqStart = 1000
        seqRange = 9000

        prev = seqStart - 1
        for i in range(seqRange * 2):
            with self.subTest(i=i):
                resp = self.app.get("/sequence")
                rslt = json.loads(resp.data.decode("utf-8"))
                rv = rslt.get("sequence_no")
                self.assertTrue(seqStart <= rv < seqStart + seqRange)
                self.assertEqual(prev + 1 if (rv != seqStart + seqRange - 1) else seqStart, rv)
            prev = rv

    def test_increments_batch_sequence(self):
        seqStart = 30000
        seqRange = 39999

        for i in range(seqRange * 2):
            with self.subTest(i=i):
                resp = self.app.get("/batch-sequence")
                res = json.loads(resp.data.decode("utf-8"))
                self.assertTrue(seqStart <= res.get("sequence_no") < seqStart + seqRange)

    def test_increments_image_sequence(self):
        seqStart = 1
        seqRange = 1E10
        testRange = 1E4

        for i in range(int(testRange)):
            with self.subTest(i=i):
                resp = self.app.get("/image-sequence")
                res = json.loads(resp.data.decode("utf-8"))
                self.assertTrue(seqStart <= res.get("sequence_no") < seqStart + seqRange)

    def test_increments_json_sequence(self):
        seqStart = 1
        seqRange = 1E10
        testRange = 1E4

        for i in range(int(testRange)):
            with self.subTest(i=i):
                resp = self.app.get("/json-sequence")
                res = json.loads(resp.data.decode("utf-8"))
                self.assertTrue(seqStart <= res.get("sequence_no") < seqStart + seqRange)
