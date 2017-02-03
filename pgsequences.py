from collections import OrderedDict
import os
import re
import textwrap

import psycopg2
from psycopg2.extras import Json
from psycopg2.pool import ThreadedConnectionPool


def get_dsn(settings=None):
    rv = {
        k: getattr(settings, v)
        for k, v in (
            ("host", "DB_HOST"), ("port", "DB_PORT"),
            ("dbname", "DB_NAME"), ("user", "DB_USER"), ("password", "DB_PASSWORD")
        )
    }
    return rv


class SequenceStore:

    class SQLSequence:
        seqs = {
            "sequence": slice(1000, 9999),
            "batch_sequence": slice(30000, 39999),
            "image_sequence": slice(1, 999999999)
        }

        @staticmethod
        def sql():
            raise NotImplementedError

        def __init__(self, seq, criteria=None):
            self.seq = seq

        def run(self, con, cur=None, log=None):
            """
            Execute the SQL defined by this class.
            Returns the cursor for data extraction.

            """
            cur = cur or con.cursor()
            if self.seq in self.seqs:
                try:
                    cur.execute(self.sql(self.seq))
                except psycopg2.ProgrammingError:
                    con.rollback()
                else:
                    con.commit()
            return cur

    class Creation(SQLSequence):

        @staticmethod
        def check(seq):
            return (
                "SELECT 0 from pg_class where relname = '{seq}'"
            ).format(seq=seq)

        @staticmethod
        def sql(seq):
            criteria = SequenceStore.Creation.seqs.get(seq)
            return (
                "CREATE SEQUENCE {seq} MINVALUE {criteria.start} "
                "MAXVALUE {criteria.stop} CYCLE"
            ).format(seq=seq, criteria=criteria)

        def run(self, con, log=None):
            cur = con.cursor()
            cur.execute(self.check(self.seq))
            if not cur.fetchone():
                cur = super().run(con, cur)
            cur.close()

    class Query(SQLSequence):

        @staticmethod
        def sql(seq):
            return "SELECT nextval('{0}')".format(seq)

        def run(self, con, log=None):
            cur = super().run(con)
            try:
                row = cur.fetchone()
                return row[0] if row else None
            except psycopg2.ProgrammingError:
                return None
            finally:
                cur.close()


class ProcessSafePoolManager:
    """
    Connection pooling presents a challenge when gunicorn forks a worker
    after the pool is created. The result can be two worker processes claiming
    the same connection from the pool.

    See https://gist.github.com/jeorgen/4eea9b9211bafeb18ada for the basis of
    this solution.

    """

    @staticmethod
    def pool(*args, **kwargs):
        return ThreadedConnectionPool(*args, **kwargs)

    def __init__(self, **kwargs):
        self.pidLastSeen = os.getpid()
        self.kwargs = kwargs
        self._pool = None

    def getconn(self):
        pidNow = os.getpid()
        if self._pool is None or self._pool.closed or pidNow != self.pidLastSeen:
            minconn = self.kwargs.pop("minconn", 1)
            maxconn = self.kwargs.pop("maxconn", 16)
            self._pool = self.pool(minconn, maxconn, **self.kwargs)
            self.pidLastSeen = pidNow
        return self._pool.getconn()

    def putconn(self, conn):
        return self._pool.putconn(conn)

    def closeall(self):
        return self._pool.closeall()
