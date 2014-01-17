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

    def register(self, address, first, last, password):
        """Register an account on the qmail server.

        Return None on success or an error string on failure.
        """
        pass

    def send_email(self, sender, subject, body, to, cc=None, bcc=None,
                   attachments=None):
        """Send an email from a given user with a given subject and body.

        `to` is a list of users in the "To:" field; `cc` is a list for the
        "CC:" field; and `bcc` is a list for the "BCC:" field. `attachments` is
        a list of Attachment objects.

        Return an Email object on success or raise an exception on failure.
        """
        pass

    def get_missions(self, user, status):
        """Get a list of all mission IDs associated with a user and status."""
        pass

    def update_mission(self, user, mission_id, status):
        """Update the status of the mission for the given user."""
        pass
