from tkinter import *

root = Tk()

thislabel = Label(root, text = "This is an string.")
thisbutton = Button(root, text = "This is a button.")

thislabel.pack()
thisbutton.pack()

root.mainloop()