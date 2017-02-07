import os
import unittest

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

    def test_query_no_sequence(self):
        pm = ProcessSafePoolManager(**self.db.dsn())
        try:
            con = pm.getconn()
            for s in SequenceStore.SQLSequence.seqs:
                with self.subTest(seq=s):
                    rv = SequenceStore.Query("sequence").run(con)
                    self.assertIsNone(rv)
        finally:
            pm.putconn(con)

    def test_create_sequence(self):
        pm = ProcessSafePoolManager(**self.db.dsn())
        try:
            con = pm.getconn()
            SequenceStore.Creation("sequence").run(con)

            cur = con.cursor()
            cur.execute("select * from pg_catalog.pg_class")
            results = cur.fetchall()
            self.assertTrue(any(i[0] == "sequence" for i in results))
            self.assertFalse(any(i[0] == "batch_sequence" for i in results))
            self.assertFalse(any(i[0] == "image_sequence" for i in results))

            # Check second attempt throws no error
            SequenceStore.Creation("sequence").run(con)
        finally:
            pm.putconn(con)

    def test_create_batch_sequence(self):
        pm = ProcessSafePoolManager(**self.db.dsn())
        try:
            con = pm.getconn()
            SequenceStore.Creation("batch_sequence").run(con)

            cur = con.cursor()
            cur.execute("select * from pg_catalog.pg_class")
            results = cur.fetchall()
            self.assertFalse(any(i[0] == "sequence" for i in results))
            self.assertTrue(any(i[0] == "batch_sequence" for i in results))
            self.assertFalse(any(i[0] == "image_sequence" for i in results))

            # Check second attempt throws no error
            SequenceStore.Creation("batch_sequence").run(con)
        finally:
            pm.putconn(con)

    def test_create_image_sequence(self):
        pm = ProcessSafePoolManager(**self.db.dsn())
        try:
            con = pm.getconn()
            SequenceStore.Creation("image_sequence").run(con)

            cur = con.cursor()
            cur.execute("select * from pg_catalog.pg_class")
            results = cur.fetchall()
            self.assertFalse(any(i[0] == "sequence" for i in results))
            self.assertFalse(any(i[0] == "batch_sequence" for i in results))
            self.assertTrue(any(i[0] == "image_sequence" for i in results))

            # Check second attempt throws no error
            SequenceStore.Creation("image_sequence").run(con)
        finally:
            pm.putconn(con)

    def test_create_json_sequence(self):
        pm = ProcessSafePoolManager(**self.db.dsn())
        try:
            con = pm.getconn()
            SequenceStore.Creation("json_sequence").run(con)

            cur = con.cursor()
            cur.execute("select * from pg_catalog.pg_class")
            results = cur.fetchall()
            self.assertFalse(any(i[0] == "sequence" for i in results))
            self.assertFalse(any(i[0] == "batch_sequence" for i in results))
            self.assertFalse(any(i[0] == "image_sequence" for i in results))
            self.assertTrue(any(i[0] == "json_sequence" for i in results))

            # Check second attempt throws no error
            SequenceStore.Creation("json_sequence").run(con)
        finally:
            pm.putconn(con)

    def test_query_sequences(self):
        pm = ProcessSafePoolManager(**self.db.dsn())
        try:
            con = pm.getconn()
            for seq in ("sequence", "batch_sequence"):  # other sequences too long
                SequenceStore.Creation(seq).run(con)
                start = SequenceStore.SQLSequence.seqs[seq].start
                stop = SequenceStore.SQLSequence.seqs[seq].stop
                prev = stop
                for i in range(2 * (stop - start + 1)):
                    with self.subTest(seq=seq, i=i):
                        rv = SequenceStore.Query(seq).run(con)
                        self.assertTrue(start <= rv <= stop)
                        self.assertNotEqual(prev, rv)
                        prev = rv
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
