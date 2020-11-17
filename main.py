from user import User


def main():
    # create two instance of User class
    user1 = User("roya", '123')  # create roya user
    user2 = User("reza", "789")  # create reza user
    # login user1
    user1.login("roya", "123")

    # write a message by user1
    message = user1.write_message(receiver=user2.username, title="fire", body="Hi Reza", date='2012-01-02')
    # send the message to user2 by user1
    user1.send_message(user2, message)
    # show the inbox of user2
    user2.show_inbox()
    # read the first message of inbox by user2
    user2.read_message(1)
    # show the inbox of user2
    user2.show_inbox()
    # user2 gets the fist message by its number
    message1 = user2.get_message(1)
    # update the first message of inbox by user2
    user2.update_message(message=message1, title="Hi")
    # show the inbox of user2
    user2.show_inbox()
    # delete the first message of inbox by user2
    user2.delete_message(1)
    # show the inbox of user2
    user2.show_inbox()
    # sign out user2
    user2.sign_out()


if __name__ == '__main__':
    main()  # run main function
