from tkinter import *
from tkinter import messagebox
from user import User
from tkinter import ttk
from PIL import ImageTk, Image


def main():
    def open_menu_tabs(login_menu, user):
        login_menu.withdraw()
        root = Tk()
        root.title("Welcome {}!".format(user.username))
        root.geometry("400x300+10+10")

        tab_control = ttk.Notebook(root)

        inbox_text, draft_text, send_text = user.get_user_info()

        inbox_tab = ttk.Frame(tab_control)
        tab_control.add(inbox_tab, text='Inbox')

        global inbox_label
        inbox_label = ttk.Label(inbox_tab, text=inbox_text)
        inbox_label.grid(column=0, row=0, padx=30, pady=30)

        draft_tab = ttk.Frame(tab_control)
        tab_control.add(draft_tab, text='Draft')

        global draft_label
        draft_label = ttk.Label(draft_tab, text=draft_text)
        draft_label.grid(column=0, row=0, padx=30, pady=30)

        send_tab = ttk.Frame(tab_control)
        tab_control.add(send_tab, text='Send')

        global send_label
        send_label = ttk.Label(send_tab, text=send_text)
        send_label.grid(column=0, row=0, padx=30, pady=30)

        compose_tab = ttk.Frame(tab_control)
        tab_control.add(compose_tab, text='Compose')

        sign_out_tab = ttk.Frame(tab_control)
        tab_control.add(sign_out_tab, text='Sign Out')

        tab_control.pack(expand=1, fill="both")

        def update_tabs(user):
            update_inbox_text, update_draft_text, update_send_text = user.get_user_info()
            inbox_label.config(text=update_inbox_text)
            draft_label.config(text=update_draft_text)
            send_label.config(text=update_send_text)

        def delete(user, box, entry_box):
            try:
                num_message = int(entry_box.get()) - 1
                delete_text = user.delete_message(num_message, box)
                if delete_text == "Successfully Deleted":
                    messagebox.showinfo("Delete", delete_text)
                    update_tabs(user)
                else:
                    messagebox.showerror("Error", delete_text)

            except ValueError:
                messagebox.showerror("Error", "Please Enter a Number!")

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

        Label(inbox_tab, text="Number: ").grid(row=1)
        read_entry = ttk.Entry(inbox_tab)
        read_entry.grid(row=1, column=1)
        ttk.Button(inbox_tab, text="Read", command=lambda: read(user)).grid(row=2, column=0)
        ttk.Button(inbox_tab, text="Delete", command=lambda: delete(user, 'Inbox', read_entry)).grid(row=2, column=1)

        def update(user_update):
            try:
                num_message_update = int(update_entry.get()) - 1
                message_find = user.find_message('Draft', num_message_update)

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
                        update_tabs(user_update_button)
                        update_window.withdraw()

                update_window = Tk()
                update_window.geometry("300x300+10+10")
                update_window.title("Update")

                receiver_update_label = Label(update_window, text="Receiver")
                receiver_update_label.grid(row=1, column=1)
                receiver_value = StringVar(update_window, value=message_find.receiver)
                receiver_update_entry = Entry(update_window, text=receiver_value)
                receiver_update_entry.grid(row=1, column=2)

                title_update_label = Label(update_window, text="Title")
                title_update_label.grid(row=2, column=1)
                title_value = StringVar(update_window, value=message_find.title)
                title_update_entry = Entry(update_window, text=title_value)
                title_update_entry.grid(row=2, column=2)

                body_update_label = Label(update_window, text="Body")
                body_update_label.grid(row=3, column=1)
                body_value = StringVar(update_window, value=message_find.body)
                body_update_entry = Entry(update_window, text=body_value)
                body_update_entry.grid(row=4, column=2)

                update_window_button = Button(update_window,
                                              text="Update",
                                              command=lambda: update_button(user_update,
                                                                            num_message_update
                                                                            )
                                              )
                update_window_button.grid(row=6, column=2)

                send_window_button = Button(update_window,
                                            text="Send",
                                            command=lambda: send_message(receiver_update_entry,
                                                                         title_update_entry,
                                                                         body_update_entry,
                                                                         num_message=num_message_update,
                                                                         window=update_window
                                                                         )
                                            )
                send_window_button.grid(row=6, column=3)


            except ValueError:
                messagebox.showerror("Error", "Please Enter a Number!")

        Label(draft_tab, text="Number: ").grid(row=1, column=0)
        update_entry = ttk.Entry(draft_tab)
        update_entry.grid(row=1, column=1)
        ttk.Button(draft_tab, text="Update", command=lambda: update(user)).grid(row=2, column=0)
        ttk.Button(draft_tab, text="Delete", command=lambda: delete(user, 'Draft', update_entry)).grid(row=2, column=1)

        send_entry = ttk.Entry(send_tab)
        send_entry.grid(row=1, column=1)
        ttk.Button(send_tab, text="Delete", command=lambda: delete(user, 'Send', send_entry)).grid(row=2, column=1)

        def write_message(receiver_entry, title_entry, body_entry):
            receiver = receiver_entry.get()
            if receiver == "":
                messagebox.showerror("Error", " Please Enter Receiver ")
            else:
                title = title_entry.get()
                body = body_entry.get()
                written_message = user.write_message(receiver=receiver, title=title, body=body)
                if written_message == "Receiver not Found":
                    messagebox.showerror("Error", "Receiver not Found")
                else:
                    update_tabs(user)
                return written_message

        def send_message(receiver_entry, title_entry, body_entry, num_message=None, window=None):
            receiver = receiver_entry.get()
            written_message = write_message(receiver_entry, title_entry, body_entry)
            message_status = user.send_message(receiver, written_message)
            if message_status == 'Unread':
                messagebox.showinfo("", "Message Sent")
                update_tabs(user)
            if num_message is not None and window is not None:
                user.delete_message(num_message, 'Draft')
                update_tabs(user)
                window.withdraw()

        Label(compose_tab, text="Receiver: ").grid(row=1, column=1)
        receiver_compose_entry = Entry(compose_tab)
        receiver_compose_entry.grid(row=1, column=2)
        Label(compose_tab, text="Title: ").grid(row=2, column=1)
        title_compose_entry = Entry(compose_tab)
        title_compose_entry.grid(row=2, column=2)
        Label(compose_tab, text="Body: ").grid(row=3, column=1)
        body_compose_entry = Entry(compose_tab)
        body_compose_entry.grid(row=4, column=2)
        Button(compose_tab, text='Draft', command=lambda: write_message(receiver_compose_entry,
                                                                        title_compose_entry,
                                                                        body_compose_entry)).grid(row=6, column=0)
        Button(compose_tab, text='Send', command=lambda: send_message(receiver_compose_entry,
                                                                      title_compose_entry,
                                                                      body_compose_entry)).grid(row=6, column=1)

        def sign_out(user):
            sign_out_text = user.sign_out()
            messagebox.showwarning("Sign out", sign_out_text)
            root.destroy()
            login_menu.deiconify()

        sign_out_button = Button(sign_out_tab, text="Sign Out", bg='pink', font="Courier 10 bold",
                                 command=lambda: sign_out(user))
        sign_out_button.grid(row=3, column=2)
        root.mainloop()

    # Define function register button
    # input : username, password from their labels
    # output: register user if user not found else show a user with the username
    def register():
        username = username_register_entry.get()
        password = password_register_entry.get()
        User.CREATE = True      # let to create user
        user = User(username, password)
        messagebox.showerror("Error", user.text)       # show there is a user with the username
        return user

    # Define function login button
    # input : messenger menu, username, password from their labels
    # output: login user if user found else show error by message box, change login status of the user
    def login_user(menu_login):
        global login
        username = username_login_entry.get()
        password = password_login_entry.get()
        user = User(username, password)     # check user existence
        if not user.found:
            messagebox.showerror("Error", "Username is Wrong!")
        else:       # if user is found
            user.login(username, password)  # try login
            if user.text == "Password is Wrong!":   # check password
                messagebox.showerror("Error", user.text)
        if user.login_status:       # check whether login is successful or not
            open_menu_tabs(menu_login, user)    # go to account of user
        login = user.login_status

    # create messenger menu and set its features
    app = Tk()
    app.title("Messenger")
    app.geometry("400x300+10+10")

    # set an icon for messenger menu
    photo = PhotoImage(file="Messenger-logo.png")
    app.iconphoto(False, photo)

    # create register and login tabs
    tab_control_login = ttk.Notebook(app)

    register_tab = ttk.Frame(tab_control_login)
    login_tab = ttk.Frame(tab_control_login)

    tab_control_login.add(register_tab, text='Register')
    tab_control_login.add(login_tab, text='Login')

    #     canvas_register = Canvas(register_tab, width=400, height=300)
    #     image_app = ImageTk.PhotoImage(Image.open("background.jpg"))
    #     canvas_register.create_image(0, 0, anchor=NW, image=image_app)
    # canvas_register.pack(expand=1, fill="both")

    #     canvas_login = Canvas(login_tab, width=400, height=300)
    #     image_app = ImageTk.PhotoImage(Image.open("background.jpg"))
    #     canvas_login.create_image(0, 0, anchor=NW, image=image_app)
    # canvas_login.pack(expand=1, fill="both")

    tab_control_login.pack(expand=1, fill="both")

    # Design register tab
    # put username label and entry
    ttk.Label(register_tab, text='username').grid(row=0)
    username_register_entry = ttk.Entry(register_tab)
    username_register_entry.grid(row=0, column=1)

    # put password label and entry
    ttk.Label(register_tab, text='password').grid(row=1)
    password_register_entry = ttk.Entry(register_tab, show="*")
    password_register_entry.grid(row=1, column=1)

    # put register button
    register_button = ttk.Button(register_tab, text='Register', command=register)
    register_button.grid(row=2, column=1)

    ttk.Label(register_tab, text="").grid(row=6, column=1)

    # Design login tab
    # put username label and entry
    ttk.Label(login_tab, text='username').grid(row=0)
    username_login_entry = ttk.Entry(login_tab)
    username_login_entry.grid(row=0, column=1)

    # put password label and entry
    ttk.Label(login_tab, text='password').grid(row=1)
    password_login_entry = ttk.Entry(login_tab, show="*")
    password_login_entry.grid(row=1, column=1)

    # put login button
    login_button = Button(login_tab, text='Login', command=lambda: login_user(app))
    login_button.grid(row=2, column=1)
    ttk.Label(login_tab, text="").grid(row=6, column=1)

    # num_lock = 1
    # login = False
    # while num_lock <= 3 and not login:
    #     login_button = Button(app, text='Login', command=lambda: login_user(app))
    #     login_button.grid(row=2, column=1)
    #     if num_lock > 3:
    #         messagebox.showerror("Error", "Lock!")
    #         exit()
    #     if not login:
    #         num_lock += 1
    #     else:
    #         break

    # show messenger menu
    app.mainloop()


if __name__ == '__main__':
    main()
