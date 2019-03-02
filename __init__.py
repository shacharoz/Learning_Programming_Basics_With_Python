# Removed PIL import, that was only necessary in Python 2
import tkinter
import tkinter.font
import os


class Window(tkinter.Tk):
    """This subclass of tkinter.Tk will represent a new window which can show different pages."""

    def __init__(self, index, title='Window', *args, **kwargs):
        """
        Initializes the class, __init__ function is used by Python as a constructor for classes.

        :param index: The start page
        :param args: Special Python arguments. All the arguments required by tkinter.Tk
        :param kwargs: Special Python arguments. All the non-positional arguments required by tkinter.Tk
        """

        # Initializing tkinter.Tk
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.wm_title(title)

        # Initializing self._frame and displaying the start (or index) page
        self._frame = None
        self.show_page(index(self))

    def show_page(self, page):
        """
        Destroys the current page and displays the given one.

        :param page: The class of the page to be displayed - *NOTE: this must be a subclass of tkinter.Frame
        """

        _frame = page

        # Destroying self._frame if it's defined
        if self._frame is not None:
            self._frame.destroy()

        self._frame = _frame
        self._frame.pack()   # Displaying the new frame (page)


class Index(tkinter.Frame):

    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)

        self.parent = parent

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
                                    command=lambda: self.parent.show_page(Home(self.parent, {'username': self.username_entry.get()})))
        self.login.place(x=self.canvas.winfo_reqwidth() / 2 - self.login.winfo_reqwidth() / 2, y=350)

        # TODO: Start page buttons, labels & other components

        def update(self):
            self.canvas = tkinter.Canvas(self.parent, width=1280,
                                         height=720)  # The canvas on which the image will be drawn

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

            self.username_entry.place(x=self.canvas.winfo_reqwidth() / 2 - self.username_entry.winfo_reqwidth() / 2,
                                      y=200)
            self.password_entry.place(x=self.canvas.winfo_reqwidth() / 2 - self.password_entry.winfo_reqwidth() / 2,
                                      y=275)

            self.login = tkinter.Button(text='Login', font=tkinter.font.Font(family='Calibri', size=24),
                                        command=lambda: self.parent.show_page(
                                            Home(self.parent, {'username': self.username_entry.get()})))
            self.login.place(x=self.canvas.winfo_reqwidth() / 2 - self.login.winfo_reqwidth() / 2, y=350)


class Home(tkinter.Frame):

    def __init__(self, parent, data):

        tkinter.Frame.__init__(self, parent)

        self.parent = parent

        self.canvas = tkinter.Canvas(self.parent, width=1280, height=720)  # The canvas on which the image will be drawn

        # The image MUST be in png format
        self.image = tkinter.PhotoImage(file=os.path.join('assets', 'img/background.png'))

        self.panel = tkinter.Label(self.parent, image=self.image)  # This is the label that will contain the image

        # This line is the most important one, Python's garbage collection will delete the image otherwise
        self.panel.image = self.image
        self.panel.place(x=0, y=0, relwidth=1, relheight=1)  # Places the image without padding
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = tkinter.Label(text='Hello ' + data.get('username'), font=tkinter.font.Font(family='Calibri', size=64))

        self.label.place(x=self.canvas.winfo_reqwidth() / 2 - self.label.winfo_reqwidth() / 2, y=350)


# Allocating a new object that will represent the main window of the app
window = Window(Index, title='Good Looking window')

if __name__ == '__main__':   # Executing if this file is ran directly
    window.mainloop()
