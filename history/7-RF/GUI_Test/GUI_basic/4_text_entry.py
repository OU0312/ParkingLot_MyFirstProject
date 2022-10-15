from cProfile import label
from tkinter import *

root = Tk()
root.title("GUI Test")
root.geometry("640x480")

txt1 = Text(root, width=30, height=5)
txt1.pack()
txt1.insert(END, "input text")

e = Entry(root, width=30)
e.pack()
e.insert(0,"only one row")


def btncmd():
    print(txt1.get("1.0",END)) # 1 : 첫번째 라인 , 0 : 0번째 column 
    print(e.get())
    
    txt1.delete("1.0",END)
    e.delete(0, END)
    
    
btn1=Button(root,text="click me!",command=btncmd)
btn1.pack()
root.mainloop() 