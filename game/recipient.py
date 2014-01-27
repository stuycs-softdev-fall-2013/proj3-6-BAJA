__all__ = ["Recipient"]

RTYPE_TO = 1
RTYPE_CC = 2
RTPYE_BCC = 3

class Recipient(object):
    def __init__(self, rid, user, rtype, address, name):
        """
        self.id: recipient database ID ref
        self.user: corresponding User object OR None if not in qmail
        self.type: RTYPE_TO | RTYPE_CC | RTPYE_BCC
        self.address: full email address string
        self.name: full name string
        """
        self.id = rid
        self.user = user
        self.type = rtype
        self.address = address
        self.name = name

    def serialize(self):
        """Convert the Recipient into a dictionary for serialization."""
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "type": self.type,
            "address": self.address,
            "name": self.name
        }
