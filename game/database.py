from datetime import datetime
import hashlib
from json import dumps, loads
from logging import getLogger
import re
import sqlite3
import time

from . import utils
from .attachment import Attachment
from .hooks import post_create, post_register, post_send
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
        post_create(self)

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

    def get_user_from_address(self, address):
        """Return the User object associated with the given address.

        Raises IndexError if the user does not exist.
        """
        query = "SELECT * FROM qmail_users WHERE qmu_address = ?"
        result = self._execute(query, address)
        return User(*result[0])

    def get_email(self, email_id):
        """Get an Email object from an ID."""
        query = """SELECT qmm_type, qmm_address, qmm_name
                   FROM qmail_email_members WHERE qmm_email = ?"""
        members = self._execute(query, email_id)
        sender = [(mem[1], mem[2]) for mem in members if mem[0] == EMAIL_SENDER][0]
        to = [(mem[1], mem[2]) for mem in members if mem[0] == EMAIL_TO]
        cc = [(mem[1], mem[2]) for mem in members if mem[0] == EMAIL_CC]
        bcc = [(mem[1], mem[2]) for mem in members if mem[0] == EMAIL_BCC]

        query = "SELECT * FROM qmail_emails WHERE qme_id = ?"
        _, subject, body, stime = self._execute(query, email_id)[0]

        attachments = []
        query = "SELECT * FROM qmail_attachments WHERE qma_email = ?"
        for aid, _, filename, content in self._execute(query, email_id):
            attachments.append(Attachment(aid, filename, content))

        return Email(email_id, sender, subject, body,
                     datetime.fromtimestamp(stime), to, cc, bcc, attachments)

    # Qmail

    def verify(self, address, password):
        """Verify that the given address's password is correct.

        Returns either None (incorrect) or a user ID.
        """
        query = """SELECT qmu_id, qmu_password_hash, qmu_password_salt
                   FROM qmail_users WHERE qmu_address = ?"""
        result = self._execute(query, address)
        if result:
            uid, pwhash, pwsalt = result[0]
            if hashlib.sha256(password + pwsalt).hexdigest() == pwhash:
                return uid

    def register(self, address, first, last, password):
        """Register an account on the qmail server.

        Returns a 2-tuple: a boolean indicating success or failure, and either
        the created user's ID upon success or an error string on failure.
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+$", address):
            return (False, "Address is invalid.")

        conn = self._connect()
        conn.isolation_level = "EXCLUSIVE"
        conn.execute("BEGIN EXCLUSIVE")

        query = "SELECT 1 FROM qmail_users WHERE qmu_address = ?"
        res = conn.execute(query, (address,))
        if res.fetchall():
            conn.commit()
            conn.close()
            return (False, "Address taken.")

        res = conn.execute("SELECT MAX(qmu_id) FROM qmail_users")
        maxid = res.fetchone()[0]
        uid = maxid + 1 if maxid else 1
        pwsalt = utils.gen_password(64, utils.PW_ALPHANUM)
        pwhash = hashlib.sha256(password + pwsalt).hexdigest()

        query = "INSERT INTO qmail_users VALUES (?, ?, ?, ?, ?, ?)"
        conn.execute(query, (uid, address, first, last, pwhash, pwsalt))
        conn.commit()
        conn.close()
        post_register(self, self.get_user(uid))
        return (True, uid)

    def get_inbox(self, user_id):
        """Generate over list of all emails in the inbox of a user ID."""
        address = self.get_user(user_id).address
        query = """SELECT qmm_email FROM qmail_email_members
                   WHERE qmm_address = ? AND qmm_type != ?"""
        for eid, in self._execute(query, address, EMAIL_SENDER):
            yield self.get_email(eid)

    def get_sentbox(self, user_id):
        """Generate over list of all emails in the sent box of a user ID."""
        address = self.get_user(user_id).address
        query = """SELECT qmm_email FROM qmail_email_members
                   WHERE qmm_address = ? AND qmm_type = ?"""
        for eid, in self._execute(query, address, EMAIL_SENDER):
            yield self.get_email(eid)

    def send_email(self, sender, subject, body, to, cc=None, bcc=None,
                   attachments=None):
        """Send an email from a given user with a given subject and body.

        `sender` is a tuple (address string, full name unicode). `subject` and
        `body` are unicode. `to` is a list of tuples in the "To:" field; `cc`
        is a tuple list for the "CC:" field; and `bcc` is a tuple list for the
        "BCC:" field. `attachments` is a list of Attachment objects.

        Return an Email object on success or raise an exception on failure.
        """
        conn = self._connect()
        conn.isolation_level = "EXCLUSIVE"
        conn.execute("BEGIN EXCLUSIVE")

        res = conn.execute("SELECT MAX(qme_id) FROM qmail_emails")
        maxid = res.fetchone()[0]
        eid = maxid + 1 if maxid else 1
        res = conn.execute("SELECT MAX(qmm_id) FROM qmail_email_members")
        maxid = res.fetchone()[0]
        mid = maxid + 1 if maxid else 1
        res = conn.execute("SELECT MAX(qma_id) FROM qmail_attachments")
        maxid = res.fetchone()[0]
        aid = maxid + 1 if maxid else 1
        stime = time.mktime(time.localtime())

        query1 = "INSERT INTO qmail_emails VALUES (?, ?, ?, ?)"
        query2 = "INSERT INTO qmail_email_members VALUES (?, ?, ?, ?, ?)"
        query3 = "INSERT INTO qmail_attachments VALUES (?, ?, ?, ?)"
        conn.execute(query1, (eid, subject, body, stime))
        conn.execute(query2, (mid, eid, EMAIL_SENDER, sender[0], sender[1]))
        mid += 1
        for addr, name in to:
            conn.execute(query2, (mid, eid, EMAIL_TO, addr, name))
            mid += 1
        if cc:
            for addr, name in cc:
                conn.execute(query2, (mid, eid, EMAIL_CC, addr, name))
                mid += 1
        if bcc:
            for addr, name in bcc:
                conn.execute(query2, (mid, eid, EMAIL_BCC, addr, name))
                mid += 1
        if attachments:
            for att in attachments:
                conn.execute(query3, (aid, eid, att.filename, att.content))
                aid += 1

        conn.commit()
        conn.close()
        email = Email(eid, sender, subject, body, stime, to, cc, bcc,
                      attachments)
        post_send(self, email)
        return email

    # Missions

    def get_missions(self, user, status):
        """Get a list of all mission IDs associated with a user and status."""
        query = """SELECT gd_mission FROM game_data
                   WHERE gd_user = ? and gd_status = ?"""
        results = self._execute(query, user.id, status)
        return [mid for (mid,) in results]

    def update_mission(self, user, mission_id, status):
        """Update the status of the mission for the given user."""
        query = "SELECT 1 FROM game_data WHERE gd_user = ? and gd_mission = ?"
        if self._execute(query, user.id, mission_id):
            query = """UPDATE game_data SET gd_status = ?
                       WHERE gd_user = ? AND gd_mission = ?"""
            self._execute(query, status, user.id, mission_id)
        else:
            query = "INSERT INTO game_data VALUES (?, ?, ?, ?)"
            self._execute(query, user.id, mission_id, status, "{}")

    def get_mission_data(self, user, mission_id, key):
        """Get an attribute of a mission associated with a given user."""
        query = """SELECT gd_attributes FROM game_data
                   WHERE gd_user = ? and gd_mission = ?"""
        result = self._execute(query, user.id, mission_id)
        return loads(result[0][0])[key]

    def set_mission_data(self, user, mission_id, key, value):
        """Set an attribute of a mission associated with a given user."""
        query = """SELECT gd_attributes FROM game_data
                   WHERE gd_user = ? and gd_mission = ?"""
        data = loads(self._execute(query, user.id, mission_id)[0][0])
        data[key] = value
        query = """UPDATE game_data SET gd_attributes = ?
                   WHERE gd_user = ? AND gd_mission = ?"""
        self._execute(query, dumps(data), user.id, mission_id)

    # School

    def add_student(self, name, password):
        """Add a student to the school database with a name; return an ID."""
        conn = self._connect()
        conn.isolation_level = "EXCLUSIVE"
        conn.execute("BEGIN EXCLUSIVE")

        res = conn.execute("SELECT MAX(s_id) FROM students")
        maxid = res.fetchone()[0]
        sid = maxid + 1 if maxid else 1

        query = "INSERT INTO students VALUES (?, ?, ?)"
        conn.execute(query, (sid, name, password))

        conn.commit()
        conn.close()
        return sid

    def add_teacher(self, name, subject):
        """Add a teacher to the school database with a name and a subject."""
        conn = self._connect()
        conn.isolation_level = "EXCLUSIVE"
        conn.execute("BEGIN EXCLUSIVE")

        res = conn.execute("SELECT MAX(t_id) FROM teachers")
        maxid = res.fetchone()[0]
        tid = maxid + 1 if maxid else 1

        query = "INSERT INTO teachers VALUES (?, ?, ?)"
        conn.execute(query, (tid, name, subject))

        conn.commit()
        conn.close()
        return tid

    def enroll_student(self, student_id, teacher_id, grade):
        """Add a student to a course with a grade."""
        query = "SELECT 1 FROM grades WHERE g_student = ? AND g_teacher = ?"
        if self._execute(query, student_id, teacher_id):
            query = """UPDATE grades SET g_grade = ?
                       WHERE g_student = ? AND g_teacher = ?"""
            self._execute(query, grade, student_id, teacher_id)
        else:
            query = "INSERT INTO grades VALUES (?, ?, ?)"
            self._execute(query, student_id, teacher_id, grade)

    def get_teachers(self):
        """Return a list of tuples of (id, name, subject)."""
        return self._execute("SELECT * FROM teachers")
