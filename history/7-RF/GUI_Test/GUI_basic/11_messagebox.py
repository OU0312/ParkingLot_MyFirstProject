import tkinter.messagebox as msgbox
from tkinter import *

root = Tk()
root.title("GUI Test")
root.geometry("640x480")

def info():
    msgbox.showinfo("alarm","work normaly")

def warn():
    msgbox.showwarning("warning","careful")

def err():
    msgbox.showerror("error","idiot")

def okcan():
    msgbox.askokcancel("ok / cancel","are you sure?")

def retrycan():
    msgbox.askretrycancel("retry / cancel","are you idiot?")
    
def yesno():
    msgbox.askyesno("yes / no","are you idiot?")
    
def yesnocan():
    responce = msgbox.askyesnocancel("yes / no / cancel","are you idiot?")
    if responce == 1 :
        print("yes")
    elif responce == 0 :
        print("No")
    elif responce == None:
        print("cancel")



Button(root, command=info,text="alarm").pack()
Button(root, command=warn,text="warn").pack()
Button(root, command=err,text="error").pack()
Button(root, command=okcan,text="okcan").pack()
Button(root, command=retrycan,text="retrycan").pack()
Button(root, command=yesno,text="yesno").pack()
Button(root, command=yesnocan,text="yesnocan").pack()


root.mainloop()     