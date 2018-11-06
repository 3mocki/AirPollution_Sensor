from DCA import DCA_class
from DCD import DCD_class
from tkinter import *

def gnt_DCD():
    dca = DCA_class()
    dcd = DCD_class()
    dcd.eId = dca.cId
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