'''
Flask functional tests
'''
import tests  # NOQA: F420 - needed to modify env settings
import server
import unittest
import json


class ServerTestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def test_get_sequence(self):
        sequence_resp = self.app.get('/sequence')
        sequence_json = json.loads(sequence_resp.get_data(as_text=True))
        self.assertEqual(200, sequence_resp.status_code)
        sequence_start = 1000
        sequence_range = 9999
        sequence_no = sequence_json['sequence_no']
        self.assertTrue(sequence_no >= sequence_start, "Sequence should be great than 1000 was {}".format(sequence_no))
        self.assertTrue(sequence_no <= sequence_range, "Sequence should be less than 9999 was {}".format(sequence_no))

    def test_json_sequence(self):
        sequence_resp = self.app.get('/json-sequence')
        sequence_json = json.loads(sequence_resp.get_data(as_text=True))
        self.assertEqual(200, sequence_resp.status_code)
        sequence_start = 1
        sequence_range = 999999999
        sequence_no = sequence_json['sequence_no']
        self.assertTrue(sequence_no >= sequence_start, "Sequence should be great than 1000 was {}".format(sequence_no))
        self.assertTrue(sequence_no <= sequence_range, "Sequence should be less than 9999 was {}".format(sequence_no))

    def test_batch_sequence(self):
        sequence_resp = self.app.get('/batch-sequence')
        sequence_json = json.loads(sequence_resp.get_data(as_text=True))
        self.assertEqual(200, sequence_resp.status_code)
        sequence_start = 30000
        sequence_range = 39999
        sequence_no = sequence_json['sequence_no']
        self.assertTrue(sequence_no >= sequence_start, "Sequence should be great than 1000 was {}".format(sequence_no))
        self.assertTrue(sequence_no <= sequence_range, "Sequence should be less than 9999 was {}".format(sequence_no))

    def test_image_sequence(self):
        sequence_resp = self.app.get('/image-sequence')
        sequence_json = json.loads(sequence_resp.get_data(as_text=True))
        self.assertEqual(200, sequence_resp.status_code)
        sequence_start = 1
        sequence_range = 999999999
        sequence_no = sequence_json['sequence_no']
        self.assertTrue(sequence_no >= sequence_start, "Sequence should be great than 1000 was {}".format(sequence_no))
        self.assertTrue(sequence_no <= sequence_range, "Sequence should be less than 9999 was {}".format(sequence_no))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
