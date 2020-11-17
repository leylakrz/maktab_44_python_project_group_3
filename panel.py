from tkinter import *
from tkinter import messagebox
from user import User
from tkinter import ttk
from message import Message

from message import Message
from user_json import *
from functools import partial

c = ["roya   ick    fire", "e      f       c"]


# add widgets here
class Panel:
    def __init__(self, title=''):
        self.window = Tk()
        self.window.title(title)
        self.window.geometry("400x300+10+10")

    def show_screen(self):
        self.window.mainloop()

    def open_inbox_window(self, data_label=[]):
        app2 = Tk()
        app2.title('Inbox')
        app2.geometry("300x200")
        f = Label(app2, text="Sender    Read    Title")
        f.grid(row=0, column=0)
        for i in range(len(data_label)):
            f = Label(app2, text=data_label[i])
            f.grid(row=i + 1, column=0)
            d = Button(app2, text='Read',
                       bg='pink',
                       fg='Red',
                       width=5, height=1,
                       font="Courier 10 bold",
                       )
            d.grid(row=i + 1, column=1)
        self.window.destroy()
        app2.mainloop()

    def destroy(self):
        self.window.destroy()

    def withdraw(self):
        self.window.withdraw()

    def deiconify(self):
        self.window.deiconify()

    @staticmethod
    def open_menu_window():
        menu = Panel(title='Menu')
        buttons = ['Inbox', 'Draft', 'Send']
        for i in range(3):
            d = Button(menu.window, text=buttons[i],
                       bg='light green',
                       fg='black',
                       width=5, height=1,
                       font="Courier 10 bold",
                       command=lambda: menu.open_inbox_window(data_label=c)
                       )
            d.grid(row=i + 3, column=1)
        menu.show_screen()

    # def read_button(message_id):
    #     read_date = read_json()
    #     for item in read_date['data']:
    #         if item['Inbox']


if __name__ == '__main__':

    def open_menu_tabs(login_menu, user):
        login_menu.withdraw()
        root = Tk()
        root.title("Welcome {}!".format(user.username))
        # root.geometry("400*300")

        tab_control = ttk.Notebook(root)

        inbox_tab = ttk.Frame(tab_control)
        draft_tab = ttk.Frame(tab_control)
        send_tab = ttk.Frame(tab_control)
        compose_tab = ttk.Frame(tab_control)
        sign_out_tab = ttk.Frame(tab_control)

        inbox_text = "No    Sender        Title        Data " + '\n'
        draft_text = "No    Receiver      Title      Data " + '\n'
        send_text = "No     Receiver       Title       Data " + '\n'
        data = read_json()
        for item in data['data']:
            if item['User'] == user.username:
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

        tab_control.add(inbox_tab, text='Inbox')
        tab_control.add(draft_tab, text='Draft')
        tab_control.add(send_tab, text='Send')
        tab_control.add(compose_tab, text='Compose')
        tab_control.add(sign_out_tab, text='Sign Out')

        tab_control.pack(expand=1, fill="both")

        ttk.Label(inbox_tab,
                  text=inbox_text).grid(column=0,
                                        row=0,
                                        padx=30,
                                        pady=30)
        ttk.Label(draft_tab,
                  text=draft_text).grid(column=0,
                                        row=0,
                                        padx=30,
                                        pady=30)
        ttk.Label(send_tab,
                  text=send_text).grid(column=0,
                                       row=0,
                                       padx=30,
                                       pady=30)

        def read(user):
            try:
                num_message = int(read_entry.get()) - 1
                message_content = user.read_message(num_message)
                if message_content == "Message not Found":
                    messagebox.showerror("Error", message_content)
                else:
                    read_window = Tk()
                    read_window.geometry("300x300+10+10")
                    read_window.title("Title: {}".format(message_content[1].title))
                    Label(read_window, text=message_content[0]).grid(row=0, column=1)
                    read_window.mainloop()
            except ValueError:
                messagebox.showerror("Error", "Please Enter a Number!")

        def update(user_update):
            try:
                num_message_update = int(update_entry.get()) - 1

                def update_button(user_update_button, num_message):
                    update_receiver = receiver_update_entry.get()
                    update_title = title_update_entry.get()
                    update_body = body_update_entry.get()
                    update_content = user_update_button.update_message(num_message,
                                                                       receiver=update_receiver,
                                                                       title=update_title,
                                                                       body=update_body
                                                                       )
                    if update_content == "Message not Found":
                        messagebox.showerror("Error", update_content)
                    elif update_content == "Successfully Update":
                        messagebox.showinfo("Info", update_content)
                        update_window.withdraw()

                update_window = Tk()
                update_window.geometry("300x300+10+10")
                update_window.title("Update")
                receiver_update_label = Label(update_window, text="Receiver")
                receiver_update_label.grid(row=1, column=1)
                receiver_update_entry = Entry(update_window)
                receiver_update_entry.grid(row=1, column=2)
                title_update_label = Label(update_window, text="Title")
                title_update_label.grid(row=2, column=1)
                title_update_entry = Entry(update_window)
                title_update_entry.grid(row=2, column=2)
                body_update_label = Label(update_window, text="Body")
                body_update_label.grid(row=3, column=1)
                body_update_entry = Entry(update_window)
                body_update_entry.grid(row=4, column=2)
                update_window_button = Button(update_window,
                                              text="Update",
                                              command=lambda: update_button(user_update, num_message_update)
                                              )
                update_window_button.grid(row=6, column=2)

            except ValueError:
                messagebox.showerror("Error", "Please Enter a Number!")

        def delete(user, box, entry_box):
            try:
                num_message = int(entry_box.get()) - 1
                delete_text = user.delete_message(num_message, box)
                if delete_text == "Successfully Deleted":
                    messagebox.showinfo("Delete", delete_text)
                else:
                    messagebox.showerror("Error", delete_text)

            except ValueError:
                messagebox.showerror("Error", "Please Enter a Number!")

        def write_message():
            receiver = receiver_entry.get()
            title = title_entry.get()
            body = body_entry.get()
            return user.write_message(receiver=receiver, title=title, body=body)

        def send_message():
            receiver = receiver_entry.get()
            written_message = write_message()
            message_status = user.send_message(receiver, written_message)
            if message_status == 'Unread':
                messagebox.showinfo("", "Message Sent")
            else:
                messagebox.showerror("Error", "Receiver not Found")

        Label(inbox_tab, text="Number: ").grid(row=1, column=0)
        read_entry = ttk.Entry(inbox_tab)
        read_entry.grid(row=1, column=1)
        ttk.Button(inbox_tab, text="Read", command=lambda: read(user)).grid(row=2, column=0)
        ttk.Button(inbox_tab, text="Delete", command=lambda: delete(user, 'Inbox', read_entry)).grid(row=2, column=1)

        Label(draft_tab, text="Number: ").grid(row=1, column=0)
        update_entry = ttk.Entry(draft_tab)
        update_entry.grid(row=1, column=1)
        ttk.Button(draft_tab, text="Update", command=lambda: update(user)).grid(row=2, column=0)
        ttk.Button(draft_tab, text="Delete", command=lambda: delete(user, 'Draft', update_entry)).grid(row=2, column=1)

        send_entry = ttk.Entry(send_tab)
        send_entry.grid(row=1, column=1)
        ttk.Button(send_tab, text="Delete", command=lambda: delete(user, 'Send', send_entry)).grid(row=2, column=1)

        Label(compose_tab, text="Receiver: ").grid(row=1, column=1)
        receiver_entry = Entry(compose_tab)
        receiver_entry.grid(row=1, column=2)
        Label(compose_tab, text="Title: ").grid(row=2, column=1)
        title_entry = Entry(compose_tab)
        title_entry.grid(row=2, column=2)
        Label(compose_tab, text="Body: ").grid(row=3, column=1)
        body_entry = Entry(compose_tab)
        body_entry.grid(row=4, column=2)
        Button(compose_tab, text='Draft', command=write_message).grid(row=6, column=0)
        Button(compose_tab, text='Send', command=send_message).grid(row=6, column=1)

        def sign_out(user):
            sign_out_text = user.sign_out()
            messagebox.showwarning("Sign out", sign_out_text)
            root.destroy()
            login_menu.deiconify()

        sign_out_button = Button(sign_out_tab, text="Sign Out", bg='pink', font="Courier 10 bold",
                                 command=lambda: sign_out(user))
        sign_out_button.grid(row=3, column=2)
        root.mainloop()


    def save_user():
        username = username_entry.get()
        password = password_entry.get()
        User.CREATE = True
        user = User(username, password)
        l = Label(text=user.text)
        l.grid(row=4, column=2)
        return user


    def login_user(menu_login):
        global login
        username = username_entry.get()
        password = password_entry.get()
        user = User(username, password)
        if not user.found:
            l1 = Label(text="Username is Wrong!")
            l1.grid(row=7, column=1)
        else:
            user.login(username, password)
            l = Label(text=user.text)
            l.grid(row=7, column=1)
        if user.login_status:
            open_menu_tabs(menu_login, user)
        login = user.login_status


    app = Panel(title='Register')
    l1 = Label(text='username')
    l1.grid(row=0)
    # username = StringVar()
    username_entry = Entry()
    username_entry.grid(row=0, column=1)
    # username = username.get()
    # print(username)
    l2 = Label(text='password')
    l2.grid(row=1)
    # password = StringVar()
    password_entry = Entry(show="*")
    password_entry.grid(row=1, column=1)
    # password = password.get()
    # print(password)
    register_button = Button(app.window, text='Register', command=save_user)
    register_button.grid(row=2, column=0)
    num_lock = 1
    login = False
    while num_lock <= 3 and not login:
        login_button = Button(app.window, text='Login', command=lambda: login_user(app))
        login_button.grid(row=2, column=1)
        if num_lock > 3:
            messagebox.showerror("Error", "Lock!")
            exit()
        if not login:
            num_lock += 1
        else:
            break
    Label(text="").grid(row=6, column=1)
    # l2 = Label(text=user.text)
    # l2.grid(row=3)
    # app = Panel(title='Login')
    # l1 = Label(text='username')
    # l1.grid(row=0)
    # e1 = Entry()
    # e1.grid(row=0, column=1)
    # l2 = Label(text='password')
    # l2.grid(row=1)
    # e2 = Entry()
    # e2.grid(row=1, column=1)
    # user1 = User(e1.get(), e2.get())

    app.show_screen()
    # print(user1.username)
