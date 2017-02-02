from collections import OrderedDict
import datetime
import os
import unittest
import uuid

import psycopg2.extensions
import psycopg2.pool
import testing.postgresql

from pgsequences import SequenceStore
from pgsequences import ProcessSafePoolManager


@testing.postgresql.skipIfNotInstalled
class SQLTests(unittest.TestCase):
    factory = testing.postgresql.PostgresqlFactory(cache_initialized_db=True)

    def setUp(self):
        self.db = self.factory()

    def tearDown(self):
        self.db.stop()

    @classmethod
    def tearDownClass(cls):
        cls.factory.clear_cache()

    def test_create(self):
        pm = ProcessSafePoolManager(**self.db.dsn())
        try:
            con = pm.getconn()
            SequenceStore.Creation("sequence").run(con)

            cur = con.cursor()
            cur.execute("select * from pg_catalog.pg_tables")
            check = schema, name, owner, space, hasIndexes, hasRules, hasTriggers, rowSec = (
                "public", "responses", "postgres", None, True, False, False, False
            )
            self.assertIn(check, cur.fetchall())

        finally:
            pm.putconn(con)

    def test_query_miss(self):
        pm = ProcessSafePoolManager(**self.db.dsn())
        try:
            con = pm.getconn()
            rv = SequenceStore.Query("sequence").run(con)

            self.assertIsInstance(rv, int)
        finally:
            pm.putconn(con)


@testing.postgresql.skipIfNotInstalled
class PoolManagerTests(unittest.TestCase):

    def setUp(self):
        self.db = testing.postgresql.Postgresql()

    def tearDown(self):
        self.db.stop()

    def test_first_connect(self):
        pm = ProcessSafePoolManager(**self.db.dsn())
        self.assertIsNone(pm._pool)

        con = pm.getconn()
        self.assertIsInstance(pm._pool, psycopg2.pool.ThreadedConnectionPool)
        self.assertEqual(1, len(pm._pool._used))
        self.assertIsInstance(con, psycopg2.extensions.connection)

        pm.putconn(con)
        self.assertEqual(0, len(pm._pool._used))

    def test_connect_after_fork(self):
        pm = ProcessSafePoolManager(**self.db.dsn())
        self.assertEqual(os.getpid(), pm.pidLastSeen)

        pm.getconn()
        pools = [pm._pool]

        pm.pidLastSeen -= 1
        pm.getconn()
        pools.append(pm._pool)

        self.assertIsNot(pools[0], pools[1])
