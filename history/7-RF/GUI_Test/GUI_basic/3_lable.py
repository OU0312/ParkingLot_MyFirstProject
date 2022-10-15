from cProfile import label
from tkinter import *

root = Tk()
root.title("GUI Test")
root.geometry("1000x700")

label1 = Label(root, text="hi idiot")
label1.pack()

def change():
    label1.config(text="eat this")
    
    global photo2
    photo2 = PhotoImage(file=r"C:\Python Project\capstone\7-RF\GUI_Test\GUI_basic\src\img2.png")
    label2.config(image=photo2)
    
photo = PhotoImage(file=r"C:\Python Project\capstone\7-RF\GUI_Test\GUI_basic\src\img.png")
label2 = Label(root,image=photo)
label2.pack()

btn1=Button(root,text="click me!",command=change)
btn1.pack()
root.mainloop()