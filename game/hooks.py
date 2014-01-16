from threading import Timer
from . import messages
AGENT_ID=1
MISSION_NOT_STARTED = 0
MISSION_IN_PROGRESS = 1
MISSION_SUCCESS = 2
MISSION_FAILED = 3

def post_create(db):
    """
        Called after database is created

        register needs to be filled out with a random password
        and needs to have UID of AGENT_ID
    """
    db.register("jblack", "John", "Black", "password") 

def post_register(db, user):
    """ 
        Called by database after a user registers
        time delay sends an email
    """
    def send_email():
        """
            Forks off, waits for a second and then sends the first email
        """
        subject = "" #load from template
        body = ""
        db.send_email(user, db.get_user(AGENT_ID), subject, body)

    Timer(5, send_email).start()

def post_send(db, email):
    """

    """
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
            db.send_email(email.recipients[0], email.sender, reply_success['subject'], reply_success['body'])

        Timer(5, send_email).start()
    else:
        #failure
     def send_email():
         """
            Sends a failed email response
        """

        reply_failed = messages.load_response(mission_id, False) 
        db.send_email(email.recipients[0], email.sender, reply_failed['subject'], reply_failed['body'])

    Timer(5, send_email).start()

