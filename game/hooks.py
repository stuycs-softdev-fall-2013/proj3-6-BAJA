from threading import Timer

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
        subject = "" #load from template
        body = ""
        db.send_email(user, subject, body, [db.get_user(AGENT_ID)])
    if user.id != AGENT_ID:
        Timer(5, send_email).start()

def post_send(db, email):
    """Called by the database after an email is sent."""
    in_progress = db.get_missions(email.sender, MISSION_IN_PROGRESS)
    mission_id = messages.mission_number(email.subject)
    if( mission_id in in_progress ):
        #success
        db.update_mission(email.sender, mission_id, MISSION_SUCCESS)
        def send_email():
            """
                Sends a successful email response
            """

            reply_success = messages.load_response(messages.next_mission(mission_id), False)
            db.send_email(email.recipients[0], reply_success['subject'], reply_success['body'], [email.sender])

        Timer(5, send_email).start()
    else:
        #failure
     def send_email():
         """
            Sends a failed email response
        """

        reply_failed = messages.load_response(mission_id, False)
        db.send_email(email.recipients[0], reply_failed['subject'], reply_failed['body'], [email.sender])

    Timer(5, send_email).start()
