__all__ = ["Attachment"]

class Attachment(object):
    """
    self.id: attachment database ID ref
    self.filename: download target file name string
    self.content: content string
    """

    def __init__(self, aid, filename, content):
        self.id = aid
        self.filename = filename
        self.content = content

    def serialize(self):
        """Convert the attachment into a dictionary for serialization."""
        return {
            "id": self.id,
            "filename": self.filename,
            "content": self.content
        }
