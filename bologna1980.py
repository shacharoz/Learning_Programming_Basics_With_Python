# Removed PIL import, that was only necessary in Python 2
import tkinter
import tkinter.font
import os
import json_file
import datetime_helper
import threading


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

        self.loginBT = tkinter.Button(text='Login', font=tkinter.font.Font(family='Calibri', size=24),
                                      command=self.login)
        self.loginBT.place(x=self.canvas.winfo_reqwidth() / 2 - self.loginBT.winfo_reqwidth() / 2, y=400)
        self.warning = tkinter.Label()

        self.bind('<Return>', self.login)
        self.focus_set()

    def login(self, event=None):
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
                                       font=tkinter.font.Font(family='Calibri', size=20))
        else:
            self.label = tkinter.Label(text=f'{user.name}, you are a new user.',
                                       font=tkinter.font.Font(family='Calibri', size=20))

        self.label.place(x=self.canvas.winfo_reqwidth() / 2 - self.label.winfo_reqwidth() / 2, y=50)

        self.startBT = tkinter.Button(text='Start', command=lambda: SlideShow(self.parent, user).restart(),
                                      font=tkinter.font.Font(family='Calibri', size=32))
        self.startBT.place(x=self.canvas.winfo_reqwidth() / 2 + self.startBT.winfo_reqwidth(), y=375)
        self.continueBT = tkinter.Button(text='Continue', command=lambda: SlideShow(self.parent, user).start(),
                                         font=tkinter.font.Font(family='Calibri', size=32))
        self.continueBT.place(x=self.canvas.winfo_reqwidth() / 2 - self.continueBT.winfo_reqwidth(), y=375)


class SlideFrame(tkinter.Frame):

    def __init__(self, parent, user, slide_show, slide):
        tkinter.Frame.__init__(self, parent)

        self.parent = parent

        self.slide_show = slide_show

        self.parent.wm_title(f'Bologna 1980 - {slide.title}')

        self.canvas = tkinter.Canvas(self.parent, width=1280, height=720)  # The canvas on which the image will be drawn

        # The image MUST be in png format
        self.image = tkinter.PhotoImage(file=os.path.join('assets', 'img', slide.image))

        self.panel = tkinter.Label(self.parent, image=self.image)  # This is the label that will contain the image

        # This line is the most important one, Python's garbage collection will delete the image otherwise
        self.panel.image = self.image
        self.panel.place(x=0, y=0, relwidth=1, relheight=1)  # Places the image without padding
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.homeBT = tkinter.Button(text='Bologna 1980',
                                     command=lambda: self.parent.show_page(Login(self.parent)),
                                     font=tkinter.font.Font(family='Calibri', size=16))

        self.homeBT.place(x=PADDING_SMALL, y=PADDING_SMALL)

        self.userBT = tkinter.Button(text=f'{user.name}',
                                     command=lambda: self.parent.show_page(Home(self.parent, user)),
                                     font=tkinter.font.Font(family='Calibri', size=16))

        self.userBT.place(x=self.canvas.winfo_reqwidth() - PADDING_SMALL - self.userBT.winfo_reqwidth(),
                          y=PADDING_SMALL)

        self.timeLB = tkinter.Label(text=slide.time,
                                    font=tkinter.font.Font(family='Calibri', size=48))
        self.timeLB.place(x=self.canvas.winfo_reqwidth() - self.timeLB.winfo_reqwidth() - PADDING,
                          y=3 * PADDING_SMALL + self.userBT.winfo_reqheight())

        self.nextBT = tkinter.Button(text="Next", command=self.slide_show.next,
                                     font=tkinter.font.Font(family='Calibri', size=32))

        self.nextBT.place(x=self.canvas.winfo_reqwidth() - self.nextBT.winfo_reqwidth() - PADDING,
                          y=self.canvas.winfo_reqheight() - PADDING - self.nextBT.winfo_reqheight())

        self.backBT = tkinter.Button(text="Back", command=self.slide_show.back,
                                     font=tkinter.font.Font(family='Calibri', size=32))

        self.backBT.place(x=PADDING, y=self.canvas.winfo_reqheight() - PADDING - self.backBT.winfo_reqheight())

        self.titleLB = tkinter.Label(text=slide.title,
                                     font=tkinter.font.Font(family='Calibri', size=64))
        self.titleLB.place(x=PADDING,
                           y=self.canvas.winfo_reqheight() - 3 * PADDING - self.titleLB.winfo_reqheight() - self.titleLB.winfo_reqheight())

        self.bind('<Right>', self.slide_show.next)
        self.bind('<Left>', self.slide_show.back)
        self.focus_set()


class Slide(object):

    def __init__(self, slide):
        """

        :param slide: The data of the Slide loaded from JSON.
        :type slide: dict
        """

        self.title = slide.get('title')
        self.time = slide.get('time')

        if slide.get('image') is None:
            self.image = 'missing.png'
        else:
            self.image = slide.get('image')


class SlideShow:

    def __init__(self, root, user):

        _slides = json_file.JsonFile(os.path.join('assets', 'dat/slides.json'))
        _slides.load()
        slides = _slides.data

        self.root = root
        self.user = user
        self.slides = slides
        self.index = 0
        self.highest = self.user.data.get('logins')[-1].get('progress')

    def restart(self):
        self.index = 0
        slide = Slide(self.slides[self.index])
        frame = SlideFrame(self.root, self.user, self, slide)
        self.root.show_page(frame)

    def start(self):
        self.index = self.user.data.get('logins')[-1].get('progress')
        slide = Slide(self.slides[self.index])
        frame = SlideFrame(self.root, self.user, self, slide)
        self.root.show_page(frame)

    def next(self, event=None):
        if self.index < len(self.slides) - 1:
            self.index += 1
            slide = Slide(self.slides[self.index])
            frame = SlideFrame(self.root, self.user, self, slide)
            self.root.show_page(frame)

            # Saving the new progress only if it's more than the last one
            if self.index > self.highest:
                self.highest = self.index
                self.user.data.get('logins')[-1] = {'date': self.user.data.get('logins')[-1].get('date'),
                                                    'progress': self.index}
                self.root.user_manager.set(self.user)

    def back(self, event=None):
        if self.index > 0:
            self.index -= 1
            slide = Slide(self.slides[self.index])
            frame = SlideFrame(self.root, self.user, self, slide)
            self.root.show_page(frame)


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


PADDING = 25
PADDING_SMALL = 10


def main():
    db = json_file.JsonFile('bologna1980.json')

    user_manager = UserManager(db)

    # cfg = config.Config('bologna1980.cfg')
    #
    # if not os.path.isfile(cfg.file):
    #     cfg.set({
    #         'Bologna1980': {
    #             'Padding': PADDING,
    #             'PaddingSmall': PADDING_SMALL
    #         }
    #     })
    #     cfg.save()
    #
    # cfg.load()
    #
    # PADDING = cfg.items().get('PaddingSmall')
    # PADDING_SMALL = cfg.items().get('Padding')

    # Allocating a new object that will represent the main window of the app
    window = Window(Login, user_manager, title='Good Looking window')

    window.mainloop()


if __name__ == '__main__':  # Executing if the file is ran directly
    main()
