import hashlib
from logging import getLogger
import sqlite3

from . import utils

__all__ = ["Database"]

SCHEMA_FILE = "schema.sql"
SCHEMA_VERSION = 1

class Database(object):
    """Represents an SQLite database storing all game information."""

    def __init__(self, filename):
        self.filename = filename
        self._logger = getLogger("gunicorn.error")

    def _create(self, conn):
        """Creates a fresh database, assuming one doesn't exist."""
        with open(SCHEMA_FILE) as fp:
            script = fp.read()
        conn.executescript(script % {"version": SCHEMA_VERSION})

    def _connect(self):
        """Create a connection with the database and update it if necessary."""
        conn = sqlite3.connect(self.filename)
        try:
            result = conn.execute("SELECT version FROM version")
            current = result.fetchone()[0]
            if current < SCHEMA_VERSION:
                logmsg = "Upgrading old schema ({0} < {1})!"
                self._logger.info(logmsg.format(current, SCHEMA_VERSION))
                self._create(conn)
        except sqlite3.OperationalError:
            self._create(conn)
        except Exception:
            conn.close()
            raise
        return conn

    def _execute(self, query, *args):
        """Execute a query, creating/updating the database if necessary."""
        with self._connect() as conn:
            return conn.execute(query, args).fetchall()

    def verify(self, address, password):
        """Verify that the given address's password is correct.

        Returns either None (incorrect) or a user ID.
        """
        query = """SELECT qmu_id, qmu_password_hash, qmu_password_salt
                   FROM qmail_users WHERE qmu_address = ?"""
        result = self._execute(query, address)
        if result:
            uid, pwsalt, pwhash = result[0]
            if hashlib.sha256(password + pwsalt).hexdigest() == pwhash:
                return uid

    def register(self, address, first, last, password):
        """Register an account on the qmail server.

        Return None on success or an error string on failure.
        """
        with self._connect() as conn:
            conn.execute("BEGIN EXCLUSIVE TRANSACTION")
            query = "SELECT 1 FROM qmail_users WHERE qmu_address = ?"
            res = conn.execute(query)
            if res.fetchall():
                return "Address taken."
            res = conn.execute("SELECT MAX(qmu_id) FROM qmail_users")
            maxid = res.fetchone()[0]
            uid = maxid + 1 if maxid else 1
            pwsalt = utils.gen_password(64, utils.PW_ALPHANUM)
            pwhash = hashlib.sha256(password + pwsalt).hexdigest()
            query = "INSERT INTO qmail_users VALUES (?, ?, ?, ?, ?)"
            conn.execute(query, (uid, address, first, last, pwhash, pwsalt))
            conn.execute("END TRANSACTION")

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

    def get_mission_data(self, user, mission_id, key):
        """Get an attribute of a mission associated with a given user."""
        pass

    def set_mission_data(self, user, mission_id, key, value):
        """Set an attribute of a mission associated with a given user."""
        pass

    def add_student(self, name):
        """Add a student to the school database with a name; return an ID."""
        pass

    def set_student_grade(self, student_id, subject, grade):
        """Set the grade of a given student in a given subject."""
        pass

    def get_student_grade(self, student_id, subject):
        """Get the grade of a given student in a given subject."""
        pass
