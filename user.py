import binascii

from message import Message
import os
import hashlib
import codecs
from datetime import datetime
from user_json import *
from logger import *


class User:
    """
    Attributes:
        username:       string, the name of user
        hash_password:  string, the hash of the password
        inbox:  list , keep messages received by user
        draft: list, keep a draft of messages
        send: list, keep messages sent bby user
        login_status:   boolean, show whether the user has logged in to the system or not
        SAlT: class attribute, keep a random value for hash function
        CREATE: class attribute, boolean: allow to create a new user

    Methods:
        login:       check username and password and if they are correct, let the user to log in to the mail box
        sign_out:    let the user to exit from the mail box
        send_message: let the user to send a message to another user
        update_message: let the user to edit message
        read_message: read a message from the inbox of the user by its number
        write_message: let the user to write a message
        delete_message: let the user to delete any message
        get_info_user: return info of inbox, draft, send box of user as string
        find_message: let user to find a message through its number
    """
    SALT = os.urandom(32)
    CREATE = False

    def __init__(self, username, password):
        self.username = username
        self.hash_password = hashlib.pbkdf2_hmac('sha256', password.encode(), binascii.hexlify(User.SALT), 100000)
        self.inbox = []
        self.draft = []
        self.send = []
        self.found = False
        self.login_status = False
        # self.unread_messages = 0
        # self.message_count = 0
        register_data = read_json()
        for item in register_data['data']:
            if item['User'] == self.username:
                self.text = "{} already in use!".format(self.username) + '\n\n' + "Change Your Username"
                self.found = True
                break
        if not self.found and User.CREATE:
            user_info = {
                "User": self.username,
                "Password": self.hash_password.decode(errors="ignore"),
                "Inbox": self.inbox,
                "Draft": self.draft,
                "Send": self.send,
                "Salt": binascii.hexlify(User.SALT).decode()
            }
            add_user_info(user_info)
            # add_user_info('user.json', user_info)
            self.text = "Register is Complete {}".format(self.username)
            User.CREATE = False

    # login: check username and password and if they are correct, let the user to log in to the mail box
    def login(self, username_input, password_input):
        # num_lock = 1  # count the number of unsuccessful login
        # check username and password
        login_data = read_json()
        for item in login_data['data']:
            if item['User'] == username_input and item["Password"] == hashlib.pbkdf2_hmac('sha256',
                                                                                          password_input.encode(),
                                                                                          item['Salt'].encode(),
                                                                                          100000
                                                                                          ).decode(errors="ignore"):
                self.login_status = True
                # ** *Welcome! {} ** * ".format(self.username)
                self.text = "                                                        "
                break
        else:
            self.text = "Password is Wrong!"
        return self.login_status

    # sign_out: let the user to exit from mail box
    def sign_out(self):
        self.login_status = False  # change the login_status to False
        # self.text =
        return "*** Bye! {} ***".format(self.username)  # print Bye! message to user

    # check_login_status: check if the user logged in or not to allow the user to do an action
    def check_login_status(self):
        while not self.login_status:  # if the user did not log in
            print("Please Login ...")  # ask the user to log in
            username = input("Enter username: ")  # ask username
            password = input("Enter Password: ")  # ask password
            self.login(username_input=username, password_input=password)  # log in to the mail box

    # send_message: let the user to send a message to another user
    def send_message(self, receiver_username, message):
        self.check_login_status()  # check login status to allow to send a message
        print()
        try:
            send_data = read_json()
            found_receiver = False
            if message.status == 'written':         # check status of message
                for item in send_data['data']:
                    if item['User'] == receiver_username:   # find receiver
                        found_receiver = True               # if receiver finding  is successful
                        for user in send_data['data']:
                            if user['User'] == self.username:       # find sender
                                # delete message from sender draft box
                                user['Draft'].remove(json.dumps(message.__dict__))
                                message.status = 'Sent'         # change message status to sent
                                # add message to sender send box
                                user['Send'].append(json.dumps(message.__dict__))
                        message.status = 'Unread'           # change message status to unread
                        # add message to sender inbox
                        item['Inbox'].append(json.dumps(message.__dict__))
                    write_json(send_data)       # write changes to json file
            if not found_receiver:
                print("*** Receiver not found ***")
            print("{}: The message was sent to {}!".format(self.username, receiver_username))  # print message was sent
            return message.status
        except AttributeError:
            pass
            logger.error("AttributeError")

    # update_message: let the user to edit message
    def update_message(self, num_message, receiver=None, body=None, title=None, date=datetime.now().date().isoformat()):
        self.check_login_status()  # check login status to allow to update a message
        print()
        data = read_json()
        for item_read in data['data']:
            if item_read["User"] == self.username:  # find user
                try:
                    content = item_read["Draft"][num_message]  # try find message in draft bax by its number
                    message_content = Message.from_json(content)        # extract message from json file
                    # update message with new entries
                    update_content = message_content.update(receiver=receiver, body=body, title=title, date=date)
                    # add updated message to draft box
                    item_read["Draft"][num_message] = json.dumps(update_content.__dict__)
                    write_json(data)        # and write in json file
                    return "Successfully Update"        # show success
                except IndexError:                      # if message not found
                    return "Message not Found"          # show error

    # write_message: let the user to write a message
    def write_message(self, receiver, body=None, title=None, date=datetime.now().date()):
        # create an instance of Message class with write_message arguments
        found_receiver = False
        write_data = read_json()
        for write_item in write_data['data']:
            if write_item['User'] == receiver:  # check receiver is available or not
                found_receiver = True
                # create message
                message = Message(sender=self.username, receiver=receiver, body=body, title=title, date=date)
                # change the status of the message to written
                message.status = "written"
                for item in write_data['data']:
                    if item["User"] == self.username:  # found sender
                        item["Draft"].append(json.dumps(message.__dict__))  # add the message to the draft of the sender
                    write_json(write_data)  # update json file
                print(" The message is written! ")  # print the message is written
                return message  # return message
        if not found_receiver:  # if receiver not found
            return "Receiver not Found"

    # get a message by the number in inbox
    def read_message(self, num_message):
        data = read_json()
        for item_read in data['data']:
            if item_read["User"] == self.username:
                try:
                    content = item_read["Inbox"][num_message]
                    message_content = Message.from_json(content)
                    read_content = message_content.read()
                    item_read["Inbox"][num_message] = json.dumps(read_content[1].__dict__)
                    write_json(data)
                    return read_content
                except IndexError:
                    return "Message not Found"

    def get_user_info(self):
        # write titles of string
        space_inbox = "----------------------------------------------------------------------"
        space = "------------------------------------------"
        inbox_text = '{:5} {:15s} {:30} {:25s} {:15} '.format("No", "Sender", "Title", "Date", "Read Status") + \
                     '\n' + space_inbox + '\n'
        draft_text = '{:5} {:15s} {:20s} {:15s} '.format("No", "Receiver", "Title", "Date") + '\n' + space + '\n'
        send_text = '{:5} {:15s} {:20s} {:15s} '.format("No", "Receiver", "Title", "Date") + '\n' + space + '\n'
        data = read_json()
        check_read = ''

        for item in data['data']:
            if item['User'] == self.username:
                for message in item['Inbox']:
                    # find message from inbox by its number
                    number_message_inbox = str(item['Inbox'].index(message) + 1)
                    # if the message status is read show tick elif it is unread show cross else show nothing
                    m = Message.from_json(message)
                    if m.status == 'Read':
                        check_read = '\u2713'
                    elif m.status == 'Unread':
                        check_read = '\u2613'
                    else:
                        check_read = ''
                    # get information of message and show in a string
                    inbox_text += '{:5} {:15s} {:30s} {:25s} {:15}  '.format(number_message_inbox, m.sender,
                                                                             m.title, m.date, check_read) + \
                                  '\n' + space_inbox + '\n'
                for message in item['Draft']:
                    # find message from draft by its number
                    number_message_draft = str(item['Draft'].index(message) + 1)
                    m = Message.from_json(message)
                    # get information of message and show in a string
                    draft_text += '{:7} {:15s} {:20s} {:15s} '.format(number_message_draft, m.receiver,
                                                                      m.title, m.date) + '\n' + space + '\n'
                for message in item['Send']:
                    # find message from send by its number
                    number_message_sent = str(item['Send'].index(message) + 1)
                    m = Message.from_json(message)
                    # get information of message and show in a string
                    send_text += '{:5} {:15s} {:20s} {:15s} '.format(number_message_sent, m.receiver,
                                                                     m.title, m.date) + '\n' + space + '\n'
        return inbox_text, draft_text, send_text        # return info as a string

    # delete_message: let the user to delete any message from any box with its number
    def delete_message(self, num_message, box):
        self.check_login_status()  # check login status to allow the user to delete a message
        print()
        data = read_json()
        for item_delete in data['data']:
            if item_delete["User"] == self.username:
                try:
                    content = item_delete[box][num_message]
                    delete_message = Message.from_json(content)
                    item_delete[box].pop(num_message)
                    write_json(data)
                    del delete_message  # delete message
                    return "Successfully Deleted"
                except IndexError:
                    return "Message not Found"

    # find_message: let user to find a message through its number
    def find_message(self, box, num_message):
        find_date = read_json()
        try:
            for find_item in find_date['data']:
                if find_item['User'] == self.username:
                    find_message_json = find_item[box][num_message]
                    find_message = Message.from_json(find_message_json)
                    return find_message
        except IndexError:
            return "Message not Found"
