import os  # used for hashing
import hashlib  # used for hashing
import binascii  # used for hashing

from user_json import *  # used to work with users.json
from logger import *  # used to log
from panel import Panel


class User:
    SALT = os.urandom(32)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_status = False

    def log_in(self, label_parent):
        register_data = read_json()
        user_found = False
        for item in register_data['data']:
            print(item['User'], self.username)
            if item['User'] == self.username:
                user_found = True
                if item["Password"] == hashlib.pbkdf2_hmac('sha256',
                                                           self.password.encode(),
                                                           item['Salt'].encode(),
                                                           100000).decode(errors="ignore"):
                    logger.info("log in")
                    self.login_status = True
                else:
                    logger.warning("attempt to log in with wrong password")
                    Panel.create_label(label_parent,
                                       [{"Label": {"text": "wrong password"}, "grid": {"row": 5, "column": 1}}])
                    # print(item['Password'], hash_password)

        if not user_found:
            logger.warning("attempt to log in with wrong username")
            Panel.create_label(label_parent,
                               [{"Label": {"text": "username not found"}, "grid": {"row": 5, "column": 1}}])
