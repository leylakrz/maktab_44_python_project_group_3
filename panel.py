from tkinter import *
from tkinter import ttk


class Panel:
    def __init__(self, title=''):
        self.window = Tk()
        self.window.title(title)
        self.window.geometry("300x200+10+10")
        self.tab_parent = ttk.Notebook(self.window)

    def show_screen(self):
        self.window.mainloop()

    def close_screen(self):
        self.window.destroy()

    # creat a new label.
    # tabs_features: list of dictionaries
    def create_tabs(self, tabs_features):
        tabs = {}
        for i in range(len(tabs_features)):
            tab_name = tabs_features[i]["tab_name"]
            tabs[tab_name] = Frame(self.tab_parent)
            self.tab_parent.add(tabs[tab_name], text=tab_name)
        self.tab_parent.pack(expand=1, fill="both")
        return tabs

    # creat a new label.
    # parent: tab or window
    # label_features: list of dictionaries of dictionaries. [{"label": {}, "grid":{}}]
    @staticmethod
    def create_label(parent, labels_features):
        for i in range(len(labels_features)):
            Label(parent, **labels_features[i]["Label"]).grid(**labels_features[i]["grid"])

    # creat a new button.
    # parent: tab or window
    # button_features: list of dictionaries of dictionaries. [{"button": {}, "grid":{}}]
    # command: function()
    @staticmethod
    def create_button(parent, buttons_features):
        for i in range(len(buttons_features)):
            Button(parent, **buttons_features[i]["Button"]).grid(**buttons_features[i]["grid"])

    # creat a new entry.
    # parent: tab or window
    @staticmethod
    def create_entry(parent, entries_features):
        entries = {}
        for i in range(len(entries_features)):
            entry_name = entries_features[i]["entry_name"]
            entries[entry_name] = Entry(parent, **entries_features[i]["Entry"])
            entries[entry_name].grid(**entries_features[i]["grid"])
        return entries
