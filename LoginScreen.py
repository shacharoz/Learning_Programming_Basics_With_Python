import tkinter
import tkinter.font
from PIL import ImageTk, Image
import json_container
import os

class Screen(tkinter.Frame):

    def __init__(self, parent):

        self.database = json_container.JsonContainer('database2.txt')
        if os.path.isfile(self.database.container):
            self.database.load()
        else:
            self.database.save()

        print(self.database)


        """
        Redefining __init__ function, parent will be a tkinter.Tk object which will
        be the container for all the components.
        """
        tkinter.Frame.__init__(self, parent)

        self.parent = parent

       # img = ImageTk.PhotoImage(Image.open('strage_1_ok.png'))
        #panel = tkinter.Label(self.parent, image=img)

        #panel.pack(side="bottom", fill="both", expand="yes")

        #self.scale = tkinter.Scale(from_=0, to=50, orient=tkinter.HORIZONTAL, font=tkinter.font.Font(family='Calibri', size=12))
        #self.scale.pack()


    #set the title of the window
    def set_page_title(self, new_title):
        self.parent.title(new_title)

    def add_label(self, label_text):
        self.label = tkinter.Label(text=label_text,
                                   font=tkinter.font.Font(family='Calibri', size=18, weight='bold'))
        self.label.pack()

    def add_text_entry(self):
        self.entry = tkinter.Entry(font=tkinter.font.Font(family='Calibri', size=12))
        self.entry.pack()

    def add_button(self,button_text,button_command):
        self.button = tkinter.Button(text=button_text, command=button_command,
                                     font=tkinter.font.Font(family='Calibri', size=12))
        self.button.pack()

    def some_action(self):
        """
        This function will be called whenever self.button is pressed
        """
        #print(f'Entry: {self.entry.get()}; Scale: {self.scale.get()}')

    def login(self):
        username = self.entry.get()
        #search in the database
        #if no -> add username and SAVE to JSON
        #if yes-> Load last date

        self.database.data[username] = "today"
        self.database.save()
        print(self.database)

    def add_image(self, image_path):
        img = ImageTk.PhotoImage(Image.open(image_path))
        panel = tkinter.Label(parent, image=img)
        panel.pack(side="bottom", fill="both", expand="yes")


def main():

    tk = tkinter.Tk()

    page = Screen(tk)
    page.set_page_title('Login')
    page.add_label('hello')
    page.add_text_entry()
    page.add_button('Login', page.login)
    #page.add_image('../strage_1_ok.jpg')


    tk.mainloop()


if __name__ == '__main__':
    main()
