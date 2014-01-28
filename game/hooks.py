from math import ceil
from random import choice, randint, shuffle
from threading import Timer
from urlparse import urlparse

from flask import request

from . import messages, utils

AGENT_ID = 1
AGENT_EMAIL = "jconnelly@qmail.com"
AGENT_FIRST = "Jon"
AGENT_LAST = "Connelly"
AGENT_TUPLE = (AGENT_EMAIL, AGENT_FIRST + " " + AGENT_LAST)

WIFE_ID = 2
WIFE_EMAIL = "lcat64@qmail.com"
WIFE_FIRST = "Lola"
WIFE_LAST = "Connelly"
WIFE_TUPLE = (WIFE_EMAIL, WIFE_FIRST + " " + WIFE_LAST)

MISSION_NOT_STARTED = 0
MISSION_IN_PROGRESS = 1
MISSION_SUCCESS = 2
MISSION_FAILED = 3

SUBJECTS = [
    ["Writing", "British Literature", "American Literature"],
    ["Algebra", "Geometry", "Trigonometry", "Pre-Calculus", "Calculus"],
    ["World History", "US History", "Economics", "Government"],
    ["Intro to CS", "AP Computer Science"],
    ["Biology", "Physics", "Chemistry", "Earth Science"],
    ["Art Appreciation", "Music Appreciation"]
]
WIFE_CODE = "AS1F5sg2af619"

messages.load_messages()

def post_create(db):
    """Called after the database is created."""
    password = utils.gen_password(64, utils.PW_ALPHANUM + utils.PW_SYMBOLS)
    db.register(AGENT_EMAIL, AGENT_FIRST, AGENT_LAST, password)

    password = utils.gen_password(64, utils.PW_ALPHANUM + utils.PW_SYMBOLS)
    db.register(WIFE_EMAIL, WIFE_FIRST, WIFE_LAST, password)
    db.send_email(("BillDonovan@mail.gov", "Bill Donovan"), "Data", WIFE_CODE, [WIFE_TUPLE])

    students = []
    for i in xrange(randint(1200, 3600)):
        password = utils.gen_password(12, utils.PW_ALPHA)
        students.append(db.add_student(utils.gen_name(), password))
    for group in SUBJECTS:
        temp = students[:]
        shuffle(temp)
        glen = int(ceil(float(len(students)) / len(group)))
        group_students = [temp[i * glen:(i + 1) * glen] for i in xrange(glen)]
        for i, subject in enumerate(group):
            subject_students = group_students[i]
            tlen = randint(75, 150)
            for j in xrange(len(subject_students) / tlen):
                teacher = db.add_teacher(utils.gen_name(), subject)
                for student in subject_students[j * tlen:(j + 1) * tlen]:
                    db.grade_student(student, teacher, utils.gen_grade())

def post_register(db, user):
    """Called by the database after a user registers."""
    try:
        link = "http://{0}:{1}/".format(urlparse(request.url).netloc.split(":")[0], utils.get_port("school"))
    except RuntimeError:
        link = ""
    def send_email():
        """Sends the initial email to the user from the agent."""
        kid_name = utils.gen_name(last="Connelly")
        password = utils.gen_password(12, utils.PW_ALPHA)
        k_id = db.add_student(kid_name, password)
        for group in SUBJECTS:
            subject = choice(group)
            teacher = choice([t[0] for t in db.get_teachers() if t[2] == subject])
            db.grade_student(k_id, teacher, utils.gen_grade(max=75))
        db.update_mission(user, 1, MISSION_IN_PROGRESS)
        db.set_mission_data(user, 1, "kid", k_id)

        mission_message = messages.get_mission(1)
        subject = mission_message['brief']['subject']
        body = mission_message['brief']['body'].format(name=user.first, kid_name=kid_name, kid_first_name=kid_name.rsplit(" ", 1)[0], link=link, password=password)
        sender = db.get_user(AGENT_ID).tuple()
        db.send_email(sender, subject, body, [user.tuple()])

    if user.id not in (AGENT_ID, WIFE_ID):
        Timer(5, send_email).start()

def post_send(db, email):
    """Called by the database after an email is sent."""
    def send_email():
        """
            Responds to email with either a "Try again" message or
            a "Success" message and the next job offer.
            Confirms that we are proposing a solution to the mission
            we attempted to solve and that we actually solved the problem
            and then sends out a response.
        """
        in_progress = db.get_missions(sender, MISSION_IN_PROGRESS)
        mission_id = messages.mission_number(email.subject)
        if mission_id in in_progress:
            # We're currently working on the mission we tried to solve
            if mission_successful(db, email, sender, mission_id):
                db.update_mission(sender, mission_id, MISSION_SUCCESS)
                reply = messages.load_response(messages.next_mission(mission_id), True)
            else:
                reply = messages.load_response(mission_id, False)
        else:
            reply = messages.load_response(-1, False)
            if email.subject.startswith("Re:"):
                reply["subject"] = email.subject
            else:
                reply["subject"] = "Re: " + email.subject
        db.send_email(AGENT_TUPLE, reply["subject"], reply["body"].format(name=sender.first), [email.sender])

    # Wait five seconds before responding to email
    if any([to[0] == AGENT_EMAIL for to in email.to]):
        sender = db.get_user_from_address(email.sender[0])
        Timer(5, send_email).start()

def mission_successful(db, email, user, mission_id):
    """
        Confirms that the mission was completed successfully.
        This process depends upon the level, for some it is
        checking with the database to confirm something was updated,
        other times its reading through the content of the email.
    """
    if mission_id == 1:
        return all([grade[2] >= 80 for grade in db.get_grades(db.get_mission_data(user, 1, "kid"))])
    elif mission_id == 2:
        return WIFE_CODE in email.body
    elif mission_id == 3:
        return False
