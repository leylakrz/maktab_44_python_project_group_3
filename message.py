from datetime import datetime
import json


class Message:
    """
    *** message Class ***
    Attributes:
        sender :    string, the name of sender of the message
        receiver :  string, the name of receiver of the message
        body :      string, the text of message
        title:      string, the title of message
        status:     string, Read/ Unread status of the message
        date:       datetime, show the date of message that the message is sent

    Methods:
        edit :      edit sender or receiver or text or title or date of the message
        read :      change status of message to Read & print the info of the message
        del :       override __del__() to enable it to delete a message object
    """

    def __init__(self, sender, receiver, body=None, title=None, status="written", date=datetime.now().date()):
        self.sender = sender
        self.receiver = receiver
        self.body = body
        self.title = title
        self.status = status
        self.date = datetime.strptime(date, '%Y-%m-%d').date().isoformat() if isinstance(date, str) else date.isoformat()

    # edit : edit sender or receiver or text or title or date of a message
    def update(self, receiver=None, body=None, title=None, date=datetime.now().date().isoformat()):
        self.status = "Update"
        if receiver is not None:
            self.receiver = receiver
        if body is not None:
            self.body = body
        if title is not None:
            self.title = title
        self.date = date
        return self

    # read : change the status of the message to Read & print the info of the message
    def read(self):
        self.status = "Read"  # change the status of the message to Read
        # print the info of the message
        space = "___________________________________"
        text = ""
        text += "Title: {}".format(self.title) + '\n' + \
                "Date: {}".format(self.date) + '\n' + space + '\n' + \
                "Sender: {}".format(self.sender) + '\n' + \
                "to: {}".format(self.receiver) + '\n' + space + '\n' + \
                "Body: " + "\n" +\
                self.body
        return text, self

    # del : override __del__() to enable it to delete a message object and return the message  was destroyed
    def __del__(self):
        class_name = self.__class__.__name__
        return class_name + " Destroyed"

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)