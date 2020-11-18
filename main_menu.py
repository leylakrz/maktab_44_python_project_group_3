from panel import *


def test():
    pass


def main_menu_window_run():
    main_menu_window = Panel()

    main_menu_tabs = main_menu_window.create_tabs([{"tab_name": "inbox"},
                                                  {"tab_name": "draft"},
                                                 {"tab_name": "sent"},
                                                 {"tab_name": "compose"},
                                                 {"tab_name": "log out"}])

    # inbox
    main_menu_window.create_label(main_menu_tabs["inbox"],
                                 [{"Label": {"text": "num"}, "grid": {"row": 0, "column": 0}},
                                  {"Label": {"text": "sender"}, "grid": {"row": 0, "column": 1}},
                                  {"Label": {"text": "title"}, "grid": {"row": 0, "column": 2}},
                                  {"Label": {"text": "date"}, "grid": {"row": 0, "column": 3}},
                                  {"Label": {"text": "time"}, "grid": {"row": 0, "column": 4}}])

    # draft
    main_menu_window.create_label(main_menu_tabs["draft"],
                                 [{"Label": {"text": "num"}, "grid": {"row": 0, "column": 0}},
                                  {"Label": {"text": "receiver"}, "grid": {"row": 0, "column": 1}},
                                  {"Label": {"text": "title"}, "grid": {"row": 0, "column": 2}}])

    # sent
    main_menu_window.create_label(main_menu_tabs["sent"],
                                 [{"Label": {"text": "num"}, "grid": {"row": 0, "column": 0}},
                                     {"Label": {"text": "receiver"}, "grid": {"row": 0, "column": 1}},
                                     {"Label": {"text": "title"}, "grid": {"row": 0, "column": 2}},
                                     {"Label": {"text": "date"}, "grid": {"row": 0, "column": 3}},
                                     {"Label": {"text": "time"}, "grid": {"row": 0, "column": 4}}])

    # compose
    main_menu_window.create_label(main_menu_tabs["compose"],
                                 [{"Label": {"text": "receiver:"}, "grid": {"row": 0, "column": 0}},
                                  {"Label": {"text": "title:"}, "grid": {"row": 1, "column": 0}},
                                    {"Label": {"text": "text:"}, "grid": {"row": 2, "column": 0}}])

    main_menu_entries = main_menu_window.create_entry(main_menu_tabs["compose"],
                                  [{"entry_name": "receiver", "Entry": {}, "grid": {"row": 0, "column": 1}},
                                   {"entry_name": "title", "Entry": {}, "grid": {"row": 1, "column": 1}},
                                   {"entry_name": "text", "Entry": {}, "grid": {"row": 2, "column": 1}}])

    main_menu_window.create_button(main_menu_tabs["compose"],
                                   [{"Button": {"text": "send", "command": test}, "grid": {"row": 3, "column": 1}}])

    # log out
    main_menu_window.create_button(main_menu_tabs["log out"],
                                   [{"Button": {"text": "log out", "command": main_menu_window.close_screen},
                                     "grid": {"row": 0, "column": 0}}])

    main_menu_window.show_screen()

    return main_menu_entries
