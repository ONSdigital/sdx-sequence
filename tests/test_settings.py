import unittest
import settings
import os


class TestSettings(unittest.TestCase):

    def setUp(self):
        with open("vcap_example.json") as fp:
            os.environ['VCAP_SERVICES'] = fp.read()
        os.environ["SDX_SEQUENCE_POSTGRES_HOST"] = "Host"
        os.environ['SDX_SEQUENCE_POSTGRES_PORT'] = "Port"
        os.environ['SDX_SEQUENCE_POSTGRES_NAME'] = "DbName"
        os.environ['SDX_SEQUENCE_POSTGRES_USER'] = "User"
        os.environ['SDX_SEQUENCE_POSTGRES_PASSWORD'] = "Password"

    def test_cf_settings(self):
        db_url = settings.parse_vcap_services()
        self.assertEqual("postgres://postgres:secret@0.0.0.0:5432/postgres", db_url)

    def test_non_cf_settings(self):
        db_url = settings.build_db_url()
        self.assertEqual("postgres://User:Password@Host:Port/DbName", db_url)

    def test_empty_environ_variable_causes_value_error(self):
        os.environ["SDX_SEQUENCE_POSTGRES_HOST"] = ""
        with self.assertRaises(ValueError):
            settings.build_db_url()

    def test_missing_environ_variable_causes_value_error(self):
        del os.environ["SDX_SEQUENCE_POSTGRES_HOST"]
        with self.assertRaises(ValueError):
            settings.build_db_url()
