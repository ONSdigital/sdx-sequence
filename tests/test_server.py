'''
Flask functional tests
'''

import unittest
import json
import testing.postgresql
import server


@testing.postgresql.skipIfNotInstalled
class SequenceNoTestCase(unittest.TestCase):

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
        self.assertTrue(sequence_no >= sequence_start, "Sequence should be greater than 1000 was {}".format(sequence_no))
        self.assertTrue(sequence_no <= sequence_range, "Sequence should be less than 9999 was {}".format(sequence_no))

    def test_json_sequence(self):
        sequence_resp = self.app.get('/json-sequence')
        sequence_json = json.loads(sequence_resp.get_data(as_text=True))
        self.assertEqual(200, sequence_resp.status_code)
        sequence_start = 1
        sequence_range = 999999999
        sequence_no = sequence_json['sequence_no']
        self.assertTrue(sequence_no >= sequence_start, "Sequence should be greater than 1 was {}".format(sequence_no))
        self.assertTrue(sequence_no <= sequence_range, "Sequence should be less than 999999999 was {}".format(sequence_no))

    def test_batch_sequence(self):
        sequence_resp = self.app.get('/batch-sequence')
        sequence_json = json.loads(sequence_resp.get_data(as_text=True))
        self.assertEqual(200, sequence_resp.status_code)
        sequence_start = 30000
        sequence_range = 39999
        sequence_no = sequence_json['sequence_no']
        self.assertTrue(sequence_no >= sequence_start, "Sequence should be greater than 30000 was {}".format(sequence_no))
        self.assertTrue(sequence_no <= sequence_range, "Sequence should be less than 39999 was {}".format(sequence_no))

    def test_image_sequence(self):
        sequence_resp = self.app.get('/image-sequence')
        sequence_json = json.loads(sequence_resp.get_data(as_text=True))
        self.assertEqual(200, sequence_resp.status_code)
        sequence_start = 1
        sequence_range = 999999999
        sequence_no = sequence_json['sequence_no']
        self.assertTrue(sequence_no >= sequence_start, "Sequence should be greater than 1 was {}".format(sequence_no))
        self.assertTrue(sequence_no <= sequence_range, "Sequence should be less than 999999999 was {}".format(sequence_no))

    def tearDown(self):
        pass


@testing.postgresql.skipIfNotInstalled
class SequenceListTestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def test_get_sequence_bad_query(self):
        sequence_resp = self.app.get('/sequence?n=abcd')
        self.assertEqual(400, sequence_resp.status_code)

    def test_get_sequence(self):
        sequence_start = 1000
        sequence_range = 9999

        for n in range(0, 13):
            with self.subTest(n=n):
                sequence_resp = self.app.get('/sequence?n={0}'.format(n))
                sequence_json = json.loads(sequence_resp.get_data(as_text=True))
                self.assertEqual(200, sequence_resp.status_code)
                sequence_list = sequence_json['sequence_list']
                self.assertEqual(n, len(sequence_list))

    def test_json_sequence(self):
        sequence_resp = self.app.get('/json-sequence')
        sequence_json = json.loads(sequence_resp.get_data(as_text=True))
        self.assertEqual(200, sequence_resp.status_code)
        sequence_start = 1
        sequence_range = 999999999
        sequence_list = sequence_json['sequence_list']
        self.assertTrue(sequence_list >= sequence_start, "Sequence should be greater than 1 was {}".format(sequence_list))
        self.assertTrue(sequence_list <= sequence_range, "Sequence should be less than 999999999 was {}".format(sequence_list))

    def test_batch_sequence(self):
        sequence_resp = self.app.get('/batch-sequence')
        sequence_json = json.loads(sequence_resp.get_data(as_text=True))
        self.assertEqual(200, sequence_resp.status_code)
        sequence_start = 30000
        sequence_range = 39999
        sequence_list = sequence_json['sequence_list']
        self.assertTrue(sequence_list >= sequence_start, "Sequence should be greater than 30000 was {}".format(sequence_list))
        self.assertTrue(sequence_list <= sequence_range, "Sequence should be less than 39999 was {}".format(sequence_list))

    def test_image_sequence(self):
        sequence_resp = self.app.get('/image-sequence')
        sequence_json = json.loads(sequence_resp.get_data(as_text=True))
        self.assertEqual(200, sequence_resp.status_code)
        sequence_start = 1
        sequence_range = 999999999
        sequence_list = sequence_json['sequence_list']
        self.assertTrue(sequence_list >= sequence_start, "Sequence should be greater than 1 was {}".format(sequence_list))
        self.assertTrue(sequence_list <= sequence_range, "Sequence should be less than 999999999 was {}".format(sequence_list))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
