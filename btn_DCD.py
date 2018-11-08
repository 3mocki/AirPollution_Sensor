from DCD import DCD_class
from tkinter import *

def gnt_DCD():
    dcd = DCD_class()
    dcd.init()

def click():
    print("-----------Generate DCD-----------")
    root = Tk()  # Blank Window

    theLabel = Label(root, text="Make a Discoonection")
    theLabel.pack()

    btn1 = Button(root, text="Disconnection", command=gnt_DCD, bg='blue')

    btn1.pack()

    root.mainloop()
    quit()

if __name__ == '__main__':