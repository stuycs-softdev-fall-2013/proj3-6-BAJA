__all__ = ["User"]

class User(object):
    """
    self.id: user database ID ref
    self.address: email address string
    self.first: first name unicode
    self.last: last name unicode
    self.pwhash: password hash string (not always available)
    self.pwsalt: password salt string (not always available)
    """

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
