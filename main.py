from tkinter import *
from tkinter import messagebox
from user import User
from tkinter import ttk
from PIL import ImageTk, Image


def main():
    # Define function login button
    # input: messenger menu and the user who succeed to login
    def open_menu_tabs(messenger_menu, user):
        # hide messenger menu
        messenger_menu.withdraw()

        # create welcome menu
        root = Tk()
        root.title("Welcome {}!".format(user.username))
        root.geometry("400x300+10+10")

        # create tab control for 5 tabs: inbox, draft, send, compose, sign out
        tab_control = ttk.Notebook(root)

        # get inbox, draft and send box user
        inbox_text, draft_text, send_text = user.get_user_info()

        # create inbox tab
        inbox_tab = ttk.Frame(tab_control)
        tab_control.add(inbox_tab, text='Inbox')

        # set inbox label
        global inbox_label  # define tabs label as global to access them in update tabs function
        inbox_label = ttk.Label(inbox_tab, text=inbox_text)
        inbox_label.grid(column=0, row=0)

        # create draft tab
        draft_tab = ttk.Frame(tab_control)
        tab_control.add(draft_tab, text='Draft')

        # set draft label
        global draft_label
        draft_label = ttk.Label(draft_tab, text=draft_text)
        draft_label.grid(column=0, row=0)

        # create send tab
        send_tab = ttk.Frame(tab_control)
        tab_control.add(send_tab, text='Send')

        # set send label
        global send_label
        send_label = ttk.Label(send_tab, text=send_text)
        send_label.grid(column=0, row=0)

        # create compose tab
        compose_tab = ttk.Frame(tab_control)
        tab_control.add(compose_tab, text='Compose')

        # create sign out tab
        sign_out_tab = ttk.Frame(tab_control)
        tab_control.add(sign_out_tab, text='Sign Out')

        tab_control.pack(expand=1, fill="both")

        # define update tabs function
        # update the contents of tabs after any changes
        def update_tabs():
            # get user information
            update_inbox_text, update_draft_text, update_send_text = user.get_user_info()
            # update text of tab labels by config method
            inbox_label.config(text=update_inbox_text)
            draft_label.config(text=update_draft_text)
            send_label.config(text=update_send_text)

        # define delete function
        # input : box name, the content of number entry to get number of message
        # output: delete a message from any box according to its number
        def delete(box, entry_box):
            try:
                # get number of message from the number entry of determined box
                num_message = int(entry_box.get()) - 1
                # user delete message from the determined box
                delete_text = user.delete_message(num_message, box)
                if delete_text == "Successfully Deleted":  # check whether deleting is successful or not
                    messagebox.showinfo("Delete", delete_text)  # show success
                    update_tabs()
                else:
                    messagebox.showerror("Error", delete_text)  # show error

            except ValueError:  # if message number is not entered correctly
                messagebox.showerror("Error", "Please Enter a Number!")  # ask to enter it as a number

        # define function to read inbox messages
        def read():
            try:
                # get number of message from the number entry of inbox
                num_message = int(read_entry.get()) - 1
                # user tries to read message
                message_content = user.read_message(num_message)
                if message_content == "Message not Found":  # check whether the message exists or not
                    messagebox.showerror("Error", message_content)  # show error if message not found
                else:
                    # create read window
                    read_window = Tk()
                    read_window.geometry("300x300+10+10")
                    read_window.title("Title: {}".format(message_content[1].title))
                    # show message
                    Label(read_window, text=message_content[0]).grid(row=0, column=1)
                    read_window.mainloop()
            # if message number is not entered correctly
            except ValueError:
                # show error if message not found
                messagebox.showerror("Error", "Please Enter a Number!")

        # create an entry to get the message number of inbox
        Label(inbox_tab, text="Number: ").grid(row=1)
        read_entry = ttk.Entry(inbox_tab)
        read_entry.grid(row=1, column=1)
        # create read button for inbox tab
        ttk.Button(inbox_tab, text="Read", command=read).grid(row=2, column=0)
        # create delete button for inbox tab
        ttk.Button(inbox_tab, text="Delete", command=lambda: delete('Inbox', read_entry)).grid(row=2, column=1)

        # define function to edit or send a message of draft box
        # input: get the message number from number entry of draft box
        # output: edit or send the message
        def edit():
            try:
                # get number of message from the number entry of draft
                num_message_update = int(update_entry.get()) - 1
                # user finds message from the draft box by the message number
                message_find = user.find_message('Draft', num_message_update)

                # define function for update button
                # input : message number
                # output : update message with new entries
                def update_button(num_message):
                    update_receiver = receiver_update_entry.get()       # get receiver
                    update_title = title_update_entry.get()             # get title
                    update_body = body_update_entry.get()               # get body
                    # user updates message by new entries
                    update_content = user.update_message(num_message,
                                                         receiver=update_receiver,
                                                         title=update_title,
                                                         body=update_body
                                                         )
                    if update_content == "Message not Found":       # check whether message found or not
                        messagebox.showerror("Error", update_content)       # show error if message not found
                    elif update_content == "Successfully Update":
                        messagebox.showinfo("Info", update_content)         # show successfully update
                        update_tabs()                                       # refresh tabs contents
                        update_window.withdraw()                            # hide update window

                # create update window
                update_window = Tk()
                update_window.geometry("300x300+10+10")
                update_window.title("Update")

                # create entries which are set with receiver, title and body of found message
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

                # create update button
                update_window_button = Button(update_window, text="Update",
                                              command=lambda: update_button(num_message_update)
                                              )
                update_window_button.grid(row=6, column=2)

                # create send button to send updated message if user wants
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

            # handle error if user enters wrong value for number entry
            except ValueError:
                messagebox.showerror("Error", "Please Enter a Number!")

        # create number label and entry to get message number
        Label(draft_tab, text="Number: ").grid(row=1, column=1)
        update_entry = ttk.Entry(draft_tab)
        update_entry.grid(row=1, column=2)
        # create edit button
        ttk.Button(draft_tab, text="Edit", command=edit).grid(row=2, column=2)
        # create delete button
        ttk.Button(draft_tab, text="Delete", command=lambda: delete('Draft', update_entry)).grid(row=3, column=2)

        # create number label and entry to get message number
        Label(send_tab, text="Number: ").grid(row=1, column=1)
        update_entry = ttk.Entry(draft_tab)
        send_entry = ttk.Entry(send_tab)
        send_entry.grid(row=1, column=2)
        # create delete button
        ttk.Button(send_tab, text="Delete", command=lambda: delete('Send', send_entry)).grid(row=2, column=2)

        # define function to write a new message in compose box
        # input: values of receiver, title, body entries
        # output: written message
        def write_message(receiver_entry, title_entry, body_entry):
            receiver = receiver_entry.get()     # get receiver
            if receiver == "":              # check whether receiver is empty or not
                messagebox.showerror("Error", " Please Enter Receiver ")  # show error if not
            else:
                title = title_entry.get()           # get title
                body = body_entry.get()             # get body
                # try to write a message
                written_message = user.write_message(receiver=receiver, title=title, body=body)
                if written_message == "Receiver not Found":         # check whether receiver exists or not
                    messagebox.showerror("Error", "Receiver not Found")     # show error if receiver not found
                else:                                                       # else
                    update_tabs()                                           # update tabs contents
                return written_message                                      # return written message

        def send_message(receiver_entry, title_entry, body_entry, num_message=None, window=None):
            receiver = receiver_entry.get()
            written_message = write_message(receiver_entry, title_entry, body_entry)
            message_status = user.send_message(receiver, written_message)
            if message_status == 'Unread':
                messagebox.showinfo("", "Message Sent")
                update_tabs()
                if num_message is not None and window is not None:
                    user.delete_message(num_message, 'Draft')
                    update_tabs()
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

        # define function for sign button
        def sign_out():
            sign_out_text = user.sign_out()  # sign out user
            messagebox.showwarning("Sign out", sign_out_text)  # show sign out
            root.destroy()  # destroy account menu
            messenger_menu.deiconify()  # show messenger menu

        # create sign out button
        sign_out_button = Button(sign_out_tab, text="Sign Out", bg='pink', font="Courier 10 bold",
                                 command=lambda: sign_out())
        sign_out_button.grid(row=3, column=2)
        # show account menu
        root.mainloop()

    # Define function register button
    # input : username, password from their labels
    # output: register user if user not found else show a user with the username
    def register():
        username = username_register_entry.get()
        password = password_register_entry.get()
        User.CREATE = True  # let to create user
        user = User(username, password)
        messagebox.showerror("Error", user.text)  # show there is a user with the username
        return user

    # Define function login button
    # input : messenger menu, username, password from their labels
    # output: login user if user found else show error by message box, change login status of the user
    def login_user(menu_login):
        global login
        username = username_login_entry.get()
        password = password_login_entry.get()
        user = User(username, password)  # check user existence
        if not user.found:
            messagebox.showerror("Error", "Username is Wrong!")
        else:  # if user is found
            user.login(username, password)  # try login
            if user.text == "Password is Wrong!":  # check password
                messagebox.showerror("Error", user.text)
        if user.login_status:  # check whether login is successful or not
            open_menu_tabs(menu_login, user)  # go to account of user
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
