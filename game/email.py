import time

__all__ = ["Email"]

class Email(object):
    """
    self.id: email database ID ref
    self.sender: sender tuple (address string, full name unicode)
    self.subject: subject unicode
    self.body: body unicode
    self.time: send time datetime
    self.to: list of tuples (address string, full name unicode)
    self.cc: list of tuples (address string, full name unicode)
    self.bcc: list of tuples (address string, full name unicode)
    self.attachments: list of Attachment objects
    """

    def __init__(self, eid, sender, subject, body, stime, to, cc, bcc,
                 attachments):
        self.id = eid
        self.sender = sender
        self.subject = subject
        self.body = body
        self.time = stime
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.attachments = attachments

    def serialize(self):
        """Convert the Email into a dictionary for serialization."""
        return {
            "id": self.id,
            "sender": self.sender,
            "subject": self.subject,
            "body": self.body,
            "time": time.mktime(self.time.timetuple()),
            "to": self.to,
            "cc": self.cc,
            "bcc": self.bcc,
            "attachments": [attach.serialize() for attach in self.attachments]
        }
