import hashlib
from logging import getLogger
import sqlite3

__all__ = ["Database"]

SCHEMA_FILE = "schema.sql"
SCHEMA_VERSION = 1

class Database(object):
    """Represents an SQLite database storing all game information."""

    def __init__(self, filename):
        self.filename = filename
        self._logger = getLogger("gunicorn.error")
        self._clear_locks()

    def _create(self, conn):
        """Creates a fresh database, assuming one doesn't exist."""
        with open(SCHEMA_FILE) as fp:
            script = fp.read()
        conn.executescript(script % {"version": SCHEMA_VERSION})

    def _execute(self, query, *args):
        """Execute a query, creating/updating the database if necessary."""
        with sqlite3.connect(self.filename) as conn:
            try:
                result = conn.execute("SELECT version FROM version")
                current = result.fetchone()[0]
                if current < SCHEMA_VERSION:
                    logmsg = "Upgrading old schema ({0} < {1})!"
                    self._logger.info(logmsg.format(current, SCHEMA_VERSION))
                    self._create(conn)
            except sqlite3.OperationalError:
                self._create(conn)
            return conn.execute(query, args).fetchall()
