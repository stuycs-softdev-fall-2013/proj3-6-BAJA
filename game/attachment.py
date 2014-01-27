__all__ = ["Attachment"]

class Attachment(object):
    def __init__(self, aid, filename, content):
        self.id = aid
        self.filename = filename
        self.content = content
