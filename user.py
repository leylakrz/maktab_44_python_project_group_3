import binascii

from message import Message
import os
import hashlib
import codecs
from datetime import datetime
from user_json import *


class User:
    """
    Attributes:
        username:       string, the name of user
        hash_password:  string, the hash of the password
        message_list:   list , keep messages of the user
        login_status:   boolean, show whether the user has logged in to the system or not
        unread_messages: int , the number of unread messages
        message_count:  int, the number of messages

    Methods:
        login:       check username and password and if they are correct, let the user to log in to the mail box
        sign_out:    let the user to exit from the mail box
        send_message: let the user to send a message to another user
        update_message: let the user to edit message
        read_message: read a message from the inbox of the user by its number
        delete_message: let the user to delete any message
        show_inbox:     show the inbox of the user
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
        self.unread_messages = 0
        self.message_count = 0
        register_data = read_json()
        for item in register_data['data']:
            if item['User'] == self.username:
                self.text = "ُThere is {}".format(self.username) + '\n' + "Change username"
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
            self.text = "ُRegister is complete! {}".format(self.username)
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

        # while data['data']username_input \
        #         or self.hash_password != hashlib.pbkdf2_hmac('sha256', password_input.encode('utf-8'), self.salt,
        #                                                      100000):
        #     if num_lock >= 3:  # lock Account if the user enter wrong username / password more than 3 times
        #         print("Account is Locked!")
        #         break
        #     else:  # Ask to log in again if username or password is wrong
        #         print("Username or Password is wrong! Try Again ...")
        #         username_input = input("Enter Username: ")
        #         password_input = input("Enter password: ")
        #
        #     num_lock += 1
        # else:  # let log in if username or password is correct and change the login_status of the user
        #     self.login_status = True
        #     print("*** Welcome! {} ***".format(self.username))

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
            if message.status == 'written':
                for item in send_data['data']:
                    if item['User'] == receiver_username:
                        found_receiver = True
                        for user in send_data['data']:
                            if user['User'] == self.username:
                                user['Draft'].remove(json.dumps(message.__dict__))
                                message.status = 'Sent'
                                user['Send'].append(json.dumps(message.__dict__))
                        message.status = 'Unread'
                        item['Inbox'].append(json.dumps(message.__dict__))
                    write_json(send_data)
            if not found_receiver:
                print("*** Receiver not found ***")
            # receiver.inbox.append(message)  # add message to the inbox list of the receiver
            # receiver.unread_messages += 1  # increment the number of unread messages
            # receiver.message_count += 1  # increment the number of messages
            # self.send.append(message)  # add message to the send list of the sender
            print("{}: The message was sent to {}!".format(self.username, receiver_username))  # print message was sent
            return message.status
        except AttributeError:
            pass

    # update_message: let the user to edit message
    def update_message(self, num_message, receiver=None, body=None, title=None, date=datetime.now().date().isoformat()):
        self.check_login_status()  # check login status to allow to update a message
        print()
        data = read_json()
        for item_read in data['data']:
            if item_read["User"] == self.username:
                try:
                    content = item_read["Draft"][num_message]
                    message_content = Message.from_json(content)
                    update_content = message_content.update(receiver=receiver, body=body, title=title, date=date)
                    item_read["Draft"][num_message] = json.dumps(update_content.__dict__)
                    write_json(data)
                    return "Successfully Update"
                except IndexError:
                    return "Message not Found"

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
        inbox_text = "No    Sender        Title        Data " + '\n'
        draft_text = "No    Receiver      Title      Data " + '\n'
        send_text = "No     Receiver       Title       Data " + '\n'
        data = read_json()

        for item in data['data']:
            if item['User'] == self.username:
                for message in item['Inbox']:
                    number_message_inbox = str(item['Inbox'].index(message) + 1)
                    m = Message.from_json(message)
                    inbox_text += number_message_inbox + '        ' + m.sender + '         ' + m.title + '\t' + m.date + '\n'
                for message in item['Draft']:
                    number_message_draft = str(item['Draft'].index(message) + 1)
                    m = Message.from_json(message)
                    draft_text += number_message_draft + '        ' + m.receiver + '          ' + m.title + '\t' + m.date + '\n'
                for message in item['Send']:
                    number_message_sent = str(item['Send'].index(message) + 1)
                    m = Message.from_json(message)
                    send_text += number_message_sent + '        ' + m.receiver + '             ' + m.title + '\t' + m.date + '\n'
        return inbox_text, draft_text, send_text

    # read_message: read a message from the inbox of the user by its number or the message
    # def read_message(self, message):
    #     self.check_login_status()  # check login status to allow to read a message
    #     print()
    #     try:
    #         if isinstance(message, int):  # if input is the number of the message
    #             # find the message in the message list by its number, then read by the read method of Message class
    #             return self.message_list[message - 1].read()
    #         elif isinstance(message, Message):  # if input is the message
    #             return message.read()  # return the message read by the read method
    #         self.unread_messages -= 1  # decrement the number of unread messages list
    #
    #     except IndexError:  # handle IndexError exception for the message list
    #         print("*** This message does not exist ***")  # print the message does not exist

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
        # message = self.message_list[num_message - 1]  # find the message by its index in the message list
        # self.message_list.remove(message)  # remove the message from the message list
        # self.message_count -= 1  # decrement the number of messages

    # show_inbox: show the inbox of the user
    # def show_inbox(self):
    #     self.check_login_status()  # check login status to allow the user to show the inbox
    #     print()
    #     print("Inbox:             Sender   Read   Title")  # print the menu of the inbox
    #     print("                   ------   -----  -----")
    #     for i in range(1, len(self.message_list) + 1):  # for every message in message list
    #         # read check :  tick symbol if the status of the message is read else print ⨉
    #         read_check = '\u2713' if self.message_list[i - 1].status == 'Read' else '\u2613'
    #         # print sender , read_check , title of the message
    #         print("       message {}   {}      {}     {}".format(i, self.message_list[i - 1].sender,
    #                                                              read_check,
    #                                                              self.message_list[i - 1].title)
    #               )

#