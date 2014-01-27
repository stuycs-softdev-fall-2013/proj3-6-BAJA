__all__ = ["User"]

class User(object):
    def __init__(self, uid, address, first, last, pwhash=None, pwsalt=None):
        self.id = uid
        self.address = address
        self.first = first
        self.last = last
        self.pwhash = pwhash
        self.pwsalt = pwsalt

    def serialize(self):
        """Convert the user into a dictionary for serialization."""
        return {
            "id": self.id,
            "address": self.address,
            "first": self.first,
            "last": self.last
        }
