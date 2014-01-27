from threading import Timer
from urlparse import urlparse
from flask import request
from . import messages, utils

AGENT_ID = 1

MISSION_NOT_STARTED = 0
MISSION_IN_PROGRESS = 1
MISSION_SUCCESS = 2
MISSION_FAILED = 3

def post_create(db):
    """Called after the database is created."""
    password = utils.gen_password(64, utils.PW_ALPHANUM + utils.PW_SYMBOLS)
    db.register("jblack", "John", "Black", password)

def post_register(db, user):
    """Called by the database after a user registers."""
    def send_email():
        """Sends the initial email to the user from the agent."""
        kid_name = utils.generate_name(last="Black")
        mission_message = messages.get_mission(1)
        link = "http://" + urlparse(request.url).netloc + utils.get_port("school")
        subject = mission_message['brief']['body']
        body = mission_message['brief']['body'].format({"name": user.first, "kid_name": kid_name, "link": link})
        db.send_email(user, subject, body, [db.get_user(AGENT_ID)])
        #Register kid into database
        k_id = db.add_student(kid_name)
        db.set_mission_data(user, 1, "kid", k_id)
        db.set_student_grade(k_id, "math", 60)
    if user.id != AGENT_ID:
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
        in_progress = db.get_missions(email.sender, MISSION_IN_PROGRESS)
        mission_id = messages.mission_number(email.subject)
        if( mission_id in in_progress ):
            #We're currently working on the mission we tried to solve
            if mission_successful(db, email, mission_id):
                db.update_mission(email.sender, mission_id, MISSION_SUCCESS)
                reply = messages.load_response(messages.next_mission(mission_id), False)
            else:
                reply = messages.load_response(mission_id, False)
        else:
            reply = messages.load_response(mission_id, False)
        db.send_email(email.recipients[0], reply['subject'], reply['body'], [email.sender])
    #Wait five seconds before responding to email
    Timer(5, send_email).start()

def mission_successful(db, email, mission_id):
    """
        Confirms that the mission was completed successfully.
        This process depends upon the level, for some it is
        checking with the database to confirm something was updated,
        other times its reading through the content of the email.
    """
    if mission_id == 1:
        if( db.get_student_grade(user, db.get_mission_data(email.sender, 1, "kid")) == 80):
            return True
        return False
    elif: mission_id == 2:
        if( db.get_

