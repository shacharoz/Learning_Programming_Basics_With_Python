import tkinter
import tkinter.font


class Page(tkinter.Frame):
    """
    This subclass of tkinter.Frame will be the start page
    of this example.
    """

    def __init__(self, parent):
        """
        Redefining __init__ function, parent will be a tkinter.Tk object which will
        be the container for all the components.
        """
        tkinter.Frame.__init__(self, parent)

        self.parent = parent

        self.parent.title('Tkinter example')
        self.label = tkinter.Label(text='Example Page', font=tkinter.font.Font(family='Calibri', size=18, weight='bold'))
        self.entry = tkinter.Entry(font=tkinter.font.Font(family='Calibri', size=12))
        self.scale = tkinter.Scale(from_=0, to=50, orient=tkinter.HORIZONTAL, font=tkinter.font.Font(family='Calibri', size=12))
        self.button = tkinter.Button(text='Do something', command=self.some_action, font=tkinter.font.Font(family='Calibri', size=12))

        self.label.pack()
        self.entry.pack()
        self.scale.pack()
        self.button.pack()

    def some_action(self):
        """
        This function will be called whenever self.button is pressed
        """
        print(f'Entry: {self.entry.get()}; Scale: {self.scale.get()}')


def main():

    tk = tkinter.Tk()

    page = Page(tk)

    tk.mainloop()


if __name__ == '__main__':
    main()
