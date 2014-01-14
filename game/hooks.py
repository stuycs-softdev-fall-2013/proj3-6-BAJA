import threading
AGENT_ID=1
def post_create(db):
    """
        Called after database is created

        register needs to be filled out with a random password
        and needs to have UID of AGENT_ID
    """
    db.register("jblack", "John", "Black", "password") 
    agent = 
def post_register(db, user):
    """ 
        Called by database after a user registers
        time delay sends an email
    """
    def send_email():
        
        db.send_email(user, agent, 

