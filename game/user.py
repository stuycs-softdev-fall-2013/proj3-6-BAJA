__all__ = ["User"]

class User(object):
    def __init__(self, uid, address, first, last, pwhash=None, pwsalt=None):
        self.id = uid
        self.address = address
        self.first = first
        self.last = last
        self.pwhash = pwhash
        self.pwsalt = pwsalt
