import hashlib
from logging import getLogger
import sqlite3

from . import utils
from .attachment import Attachment
from .email import Email
from .user import User

__all__ = ["Database"]

SCHEMA_FILE = "schema.sql"
SCHEMA_VERSION = 1

EMAIL_SENDER = 0
EMAIL_TO = 1
EMAIL_CC = 2
EMAIL_BCC = 3

class Database(object):
    """Represents an SQLite database storing all game information."""

    def __init__(self, filename):
        self.filename = filename
        self._logger = getLogger("gunicorn.error")

    # Private helper methods

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

    # Generic object builders

    def get_user(self, user_id):
        """Return the User object associated with the given user ID.

        Raises IndexError if the user does not exist.
        """
        query = "SELECT * FROM qmail_users WHERE qmu_id = ?"
        result = self._execute(query, user_id)
        return User(*result[0])

    def get_email(self, email_id, user_id):
        """Get an email from an ID if the user has permission to view it.

        Returns None if no email could be found or the user isn't allowed to
        view it. Raises IndexError if the user does not exist.
        """
        user = self.get_user(user_id)
        query = """SELECT qmm_type, qmm_address, qmm_name
                   FROM qmail_email_members WHERE qmm_email = ?"""
        members = self._execute(query, email_id)
        if not [mem for mem in members if mem[1] == user.address]:
            return None  # User not permitted to view
        try:
            sender = [(mem[1], mem[2]) for mem in members if mem[0] == EMAIL_SENDER][0]
        except IndexError:
            return None  # No senders -> email doesn't exist
        to = [(mem[1], mem[2]) for mem in members if mem[0] == EMAIL_TO]
        cc = [(mem[1], mem[2]) for mem in members if mem[0] == EMAIL_CC]
        bcc = [(mem[1], mem[2]) for mem in members if mem[0] == EMAIL_BCC]

        query = "SELECT * FROM qmail_emails WHERE qme_id = ?"
        _, subject, body = self._execute(query, email_id)[0]

        attachments = []
        query = "SELECT * FROM qmail_attachments WHERE qma_email = ?"
        for aid, _, filename, content in self._execute(query, email_id):
            attachments.append(Attachment(aid, filename, content))

        return Email(email_id, sender, subject, body, to, cc, bcc, attachments)

    # Qmail

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

        Returns a 2-tuple: a boolean indicating success or failure, and either
        the created user's ID upon success or an error string on failure.
        """
        with self._connect() as conn:
            conn.execute("BEGIN EXCLUSIVE TRANSACTION")
                                                                                    # First, do an address validity check.
            query = "SELECT 1 FROM qmail_users WHERE qmu_address = ?"
            res = conn.execute(query)
            if res.fetchall():
                return (False, "Address taken.")
            res = conn.execute("SELECT MAX(qmu_id) FROM qmail_users")
            maxid = res.fetchone()[0]
            uid = maxid + 1 if maxid else 1
            pwsalt = utils.gen_password(64, utils.PW_ALPHANUM)
            pwhash = hashlib.sha256(password + pwsalt).hexdigest()
            query = "INSERT INTO qmail_users VALUES (?, ?, ?, ?, ?)"
            conn.execute(query, (uid, address, first, last, pwhash, pwsalt))
            conn.execute("END TRANSACTION")
            return (True, uid)

    def send_email(self, sender, subject, body, to, cc=None, bcc=None,
                   attachments=None):
        """Send an email from a given user with a given subject and body.

        `to` is a list of users in the "To:" field; `cc` is a list for the
        "CC:" field; and `bcc` is a list for the "BCC:" field. `attachments` is
        a list of Attachment objects.

        Return an Email object on success or raise an exception on failure.
        """
        pass

    # Missions

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

    # School

    def add_student(self, name):
        """Add a student to the school database with a name; return an ID."""
        pass

    def set_student_grade(self, student_id, subject, grade):
        """Set the grade of a given student in a given subject."""
        pass

    def get_student_grade(self, student_id, subject):
        """Get the grade of a given student in a given subject."""
        pass
