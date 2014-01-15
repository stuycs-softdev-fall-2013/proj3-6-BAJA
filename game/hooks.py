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
    if( messages.mission_number(email.subject) in in_progress ):
        #success
        
    else:
        #failure
