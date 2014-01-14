class User(object):
    def __init__(self, uid, address, first, last, pwhash, pwsalt):
        self.uid = uid
        self.address = address
        self.first = first
        self.last = last
        self.pwhash = pwhash
        self.pwsalt = pwsalt
