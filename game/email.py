__all__ = ["Email"]

class Email(object):
    def __init__(self, eid, sender, subject, body, to, cc, bcc, attachments):
        self.id = eid
        self.sender = sender
        self.subject = subject
        self.body = body
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.attachments = attachments

    def serialize(self):
        """Convert the email into a dictionary for serialization."""
        return {
            "id": self.id,
            "sender": self.sender,
            "subject": self.subject,
            "body": self.body,
            "to": [recip.serialize() for recip in self.to],
            "cc": [recip.serialize() for recip in self.cc],
            "bcc": [recip.serialize() for recip in self.bcc],
            "attachments": [attach.serialize() for attach in self.attachments]
        }
