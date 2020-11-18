from panel import *
from user import *
from main_menu import *


def test():
    pass


def create_user_object(login_entries, label_parent, login_window_close_screen):
    username = login_entries["username"].get()
    if username == "":
        logger.warning("attempt to log in with no username")
    else:
        user = User(username, login_entries["password"].get())
        user.log_in(label_parent)
        if user.login_status:
            login_window_close_screen()
            main_menu_window_run()




login_window = Panel("log in / register")
login_tabs = login_window.create_tabs([{"tab_name": "log in"},
                                      {"tab_name": "register"}])
# log in
login_window.create_label(login_tabs["log in"],
                         [{"Label": {"text": "username:"}, "grid": {"row": 0, "column": 0}},
                         {"Label": {"text": "password:"}, "grid": {"row": 1, "column": 0}}])
login_entries = login_window.create_entry(login_tabs["log in"],
                                          [{"entry_name": "username", "Entry": {}, "grid": {"row": 0, "column": 1}},
                                           {"entry_name": "password", "Entry": {"show": "*"},
                                            "grid": {"row": 1, "column": 1}}])
login_window.create_button(login_tabs["log in"],
                           [{"Button": {"text": "log in",
                                        "command": lambda: create_user_object(login_entries, login_tabs["log in"],
                                                                              login_window.close_screen)},
                             "grid": {"row": 2, "column": 1}}])
# register
login_window.create_label(login_tabs["register"],
                         [{"Label": {"text": "username:"}, "grid": {"row": 0, "column": 0}},
                         {"Label": {"text": "password:"}, "grid": {"row": 1, "column": 0}}])
register_entries = login_window.create_entry(login_tabs["register"],
                                          [{"entry_name": "username", "Entry": {}, "grid": {"row": 0, "column": 1}},
                                           {"entry_name": "password", "Entry": {"show": "*"},
                                            "grid": {"row": 1, "column": 1}}])
login_window.create_button(login_tabs["register"],
                           [{"Button": {"text": "register", "command": test}, "grid": {"row": 2, "column": 1}}])

login_window.show_screen()