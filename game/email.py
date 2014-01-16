__all__ = ["Email"]

class Email(object):
    def __init__(self, eid, sender, subject, body, recipients,
                 attachments=None):
        self.eid = eid
        self.sender = sender
        self.subject = subject
        self.body = body
        self.recipients = recipients
        self.attachments = attachments
