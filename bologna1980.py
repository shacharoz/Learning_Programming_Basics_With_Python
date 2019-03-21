# Removed PIL import, that was only necessary in Python 2
import tkinter
import tkinter.font
import os
import json_file
import datetime_helper


class Window(tkinter.Tk):
    """This subclass of tkinter.Tk will represent a new window which can show different pages."""

    def __init__(self, index, user_manager, title='Window', *args, **kwargs):
        """
        Initializes the class, __init__ function is used by Python as a constructor for classes.

        :param index: The start page
        :param args: Special Python arguments. All the arguments required by tkinter.Tk
        :param kwargs: Special Python arguments. All the non-positional arguments required by tkinter.Tk
        """

        # Initializing tkinter.Tk
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.wm_title(title)

        self.user_manager = user_manager

        # Initializing self._frame (named with a leading underscore because it will override tkinter.Tk.frame function)
        # and displaying the start (or index) page
        self._frame = None
        self.show_page(index(self))

    def show_page(self, page):
        """
        Destroys the current page and displays the given one.
        :param page: The page to be displayed - *NOTE: this must be an instance of tkinter.Frame
        """

        _frame = page

        # Destroying self._frame if it's defined
        if self._frame is not None:
            self._frame.destroy()

        self._frame = _frame
        self._frame.pack()  # Displaying the new frame (page)


class Login(tkinter.Frame):

    def __init__(self, parent):
        """
        Draws every component of the screen
        :param parent: The instance of tkinter.Tk this tkinter.Frame is dependant to
        :type parent: tkinter.Tk
        """

        tkinter.Frame.__init__(self, parent)

        self.parent = parent

        self.parent.wm_title('Login')

        self.canvas = tkinter.Canvas(self.parent, width=1280, height=720)  # The canvas on which the image will be drawn

        # The image MUST be in png format
        self.image = tkinter.PhotoImage(file=os.path.join('assets', 'img/background.png'))

        self.panel = tkinter.Label(self.parent, image=self.image)  # This is the label that will contain the image

        # This line is the most important one, Python's garbage collection will delete the image otherwise
        self.panel.image = self.image
        self.panel.place(x=0, y=0, relwidth=1, relheight=1)  # Places the image without padding
        self.canvas.pack()

        self.username_entry = tkinter.Entry(self.parent, font=tkinter.font.Font(family='Calibri', size=32))
        self.password_entry = tkinter.Entry(self.parent, show='\u2022',
                                            font=tkinter.font.Font(family='Calibri', size=32))

        self.username_entry.insert(0, 'Username')
        self.password_entry.insert(0, 'Password')

        self.username_entry.place(x=self.canvas.winfo_reqwidth() / 2 - self.username_entry.winfo_reqwidth() / 2, y=200)
        self.password_entry.place(x=self.canvas.winfo_reqwidth() / 2 - self.password_entry.winfo_reqwidth() / 2, y=275)

        self.login = tkinter.Button(text='Login', font=tkinter.font.Font(family='Calibri', size=24),
                                    command=self.login)
        self.login.place(x=self.canvas.winfo_reqwidth() / 2 - self.login.winfo_reqwidth() / 2, y=400)
        self.warning = tkinter.Label()

    def login(self):
        user = self.parent.user_manager.login(self.username_entry.get(), self.password_entry.get())

        if user.auth.get('success') is True:
            self.parent.show_page(Home(self.parent, user))
        else:
            self.warning.config(text='Login failed: ' + user.auth.get('cause'), fg='red',
                                font=tkinter.font.Font(family='Calibri', size=24))
            self.warning.place(x=self.canvas.winfo_reqwidth() / 2 - self.warning.winfo_reqwidth() / 2, y=345)


class Home(tkinter.Frame):

    def __init__(self, parent, user):
        tkinter.Frame.__init__(self, parent)

        self.parent = parent

        self.parent.wm_title('Home')

        self.canvas = tkinter.Canvas(self.parent, width=1280, height=720)  # The canvas on which the image will be drawn

        # The image MUST be in png format
        self.image = tkinter.PhotoImage(file=os.path.join('assets', 'img/background.png'))

        self.panel = tkinter.Label(self.parent, image=self.image)  # This is the label that will contain the image

        # This line is the most important one, Python's garbage collection will delete the image otherwise
        self.panel.image = self.image
        self.panel.place(x=0, y=0, relwidth=1, relheight=1)  # Places the image without padding
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        logins = user.data.get('logins')
        if len(logins) > 1:
            self.label = tkinter.Label(text=f"Last login: {logins[-1].get('date')}.",
                                       font=tkinter.font.Font(family='Calibri', size=64))
        else:
            self.label = tkinter.Label(text=f'You are a new user.', font=tkinter.font.Font(family='Calibri', size=64))

        self.label.place(x=self.canvas.winfo_reqwidth() / 2 - self.label.winfo_reqwidth() / 2, y=350)


class User(object):

    def __init__(self, username, password=None, data=None, auth=None):
        """
        This class represents a user.

        :param username: The name of the User.
        :type username: str

        :param password: The password of the User, optional if the data is given.
        :type password: str

        :param data: The data of the User, optional if the password is given.
        :type data: dict

        :param auth: Authentication dict. It should have this format
                     {'success': bool, 'cause': str or NoneType if successful}
        :type auth: dict
        """

        self.name = username
        self.auth = auth

        if data is not None:
            self.data = data
        elif password is not None:
            self.data = {'password': password, 'logins': []}  # Initializing the data


class UserManager:

    def __init__(self, db):

        self.db = db

        if os.path.isfile(self.db.container):
            self.db.load()
        else:
            self.db.save()

    def set(self, user):
        """
        Updates (or adds if no valid user is found) a user to the database.

        :param user: The user to update (or add) to the database.
        :type user: User
        """
        if isinstance(user, User):
            self.db.data[user.name] = user.data
            self.db.save()
        else:
            raise TypeError(f"'{user}' is not a valid User.")

    def login(self, username, password):
        """
        Loads a user from the database and authenticates him.

        :param username: The user's name
        :type username: str
        :param password: The user's password
        :type password: str
        :return: The User loaded from the database
        """

        data = self.db.data.get(username)  # Retrieving the data, if no user is found this will be set to None

        if data is not None:
            user = User(username, data=data)
            user.data.get('logins').append({'date': datetime_helper.date_now(), 'progress': 0})
            # Authenticating the user
            if user.data.get('password') == password:
                user.auth = {'success': True, 'cause': None}  # Setting the authentication to successful
            else:
                user.auth = {'success': False, 'cause': 'Wrong password!'}  # Setting the authentication to unsuccessful
            self.set(user)
            return user  # Returns the authenticated user
        else:
            self.set(User(username, password))  # Saving the new User to the database
            return self.login(username, password)  # Call to the same function for authentication

    # def login(self, username, password):
    #
    #     user = self.db.data.get(username)
    #
    #     if user is None:
    #         user = {'password': password, 'logins': [{'date': datetime_helper.date_now(), 'progress': 0}]}
    #         self.db.data[username] = user
    #         self.db.save()
    #     else:
    #         user.get('logins').append({'date': datetime_helper.date_now(), 'progress': -1})
    #         self.db.data[username] = user
    #         self.db.save()
    #     return


def main():
    db = json_file.JsonFile('bologna1980.json')

    user_manager = UserManager(db)

    # Allocating a new object that will represent the main window of the app
    window = Window(Login, user_manager, title='Good Looking window')

    window.mainloop()


# Executing if the file is ran directly
if __name__ == '__main__':
    main()
