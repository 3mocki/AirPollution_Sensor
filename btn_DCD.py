from DCD import DCD_class
from tkinter import *
from tkinter import messagebox

def gnt_DCD():
    dcd = DCD_class()
    dcd.init()

if __name__ == '__main__':
    print("-----------Generate DCD-----------")
    root = Tk()  # Blank Window

    theLabel = Label(root, text="Make a Discoonection")
    theLabel.pack()

    btn1 = Button(root, text="Disconnection", command=gnt_DCD, bg='blue')

    btn1.pack()

    root.mainloop()
    quit()