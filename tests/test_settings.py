import unittest
import settings
import os


class TestSettings(unittest.TestCase):

    def setUp(self):
        with open("vcap_example.json") as fp:
            os.environ['VCAP_SERVICES'] = fp.read()

    def test_cf_settings(self):
        os.environ['CF_DEPLOYMENT'] = "True"
        settings.get_env()
        self.assertEqual("postgres://postgres:secret@0.0.0.0:5432/postgres", settings.DB_URL)

    def test_non_cf_environments(self):
        del os.environ['CF_DEPLOYMENT']
        os.environ["SDX_SEQUENCE_POSTGRES_HOST"] = "Host"
        os.environ["SDX_SEQUENCE_POSTGRES_PORT"] = "Port"
        os.environ["SDX_SEQUENCE_POSTGRES_NAME"] = "DbName"
        os.environ["SDX_SEQUENCE_POSTGRES_USER"] = "User"
        os.environ["SDX_SEQUENCE_POSTGRES_PASSWORD"] = "Password"

        settings.get_env()

        self.assertEqual("postgres://User:Password@Host:Port/DbName", settings.DB_URL)

