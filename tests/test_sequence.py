from server import app
import unittest
import json
import mock


class TestSequenceService(unittest.TestCase):

    sequence_endpoint = "/sequence"
    batch_sequence_endpoint = "/batch-sequence"
    image_sequence_endpoint = "/image-sequence"

    def setUp(self):

        # creates a test client
        self.app = app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True

    def mock_sequence_response(self, endpoint, mock_value, seq_start, seq_range, expected_sequence_no=False):
        # Use the loop index as to mock a return param
        with mock.patch('server.get_next_sequence', return_value=mock_value):
            r = self.app.get(endpoint)

            expected = expected_sequence_no if expected_sequence_no else seq_start + (mock_value - 1) % seq_range

            actual_response = json.loads(r.data.decode('UTF8'))
            expected_response = {'sequence_no': expected}

            self.assertEqual(actual_response, expected_response)

    def test_increments_sequence(self):
        sequence_start = 1000
        sequence_range = 9000

        test_start = 1
        test_end = 10

        for i in range(test_start, test_end):
            self.mock_sequence_response(self.sequence_endpoint, i, sequence_start, sequence_range)

    def test_increment_wraps_sequence(self):
        sequence_start = 1000
        sequence_range = 9000

        test_start = 8998
        test_end = 9003

        for i in range(test_start, test_end):
            self.mock_sequence_response(self.sequence_endpoint, i, sequence_start, sequence_range)

    def test_increments_batch_sequence(self):
        sequence_start = 30000
        sequence_range = 10000

        test_start = 8998
        test_end = 9003

        for i in range(test_start, test_end):
            self.mock_sequence_response(self.batch_sequence_endpoint, i, sequence_start, sequence_range)

    def test_increment_wraps_batch_sequence(self):
        sequence_start = 30000
        sequence_range = 10000

        test_start = 39998
        test_end = 40003

        for i in range(test_start, test_end):
            self.mock_sequence_response(self.batch_sequence_endpoint, i, sequence_start, sequence_range)

    def test_increments_image_sequence(self):
        sequence_start = 1
        sequence_range = 1000000000

        test_start = 1
        test_end = 10

        for i in range(test_start, test_end):
            expected_seq_no = i % sequence_range
            self.mock_sequence_response(self.image_sequence_endpoint, i, sequence_start, sequence_range, expected_sequence_no=expected_seq_no)

    def test_increment_wraps_image_sequence(self):
        sequence_start = 1
        sequence_range = 1000000000

        test_start = 9999999998
        test_end = 1000000005

        for i in range(test_start, test_end):
            expected_seq_no = i % sequence_range
            self.mock_sequence_response(self.image_sequence_endpoint, i, sequence_start, sequence_range, expected_sequence_no=expected_seq_no)
