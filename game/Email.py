class Email(object):
    def __init__(self, eid, sender, mailbox, recipients, subject, body, attachments=None):
        self.eid = eid
        self.sender = sender
        self.mailbox = mailbox
        self.recipients = recipients
        self.subject = subject
        self.body = body
        self.attachments = attachments
