import tkinter.messagebox as msgbox
from tkinter import *

root = Tk()
root.title("GUI Test")
root.geometry("640x480")

Label(root,text="hi").pack(side="top")
Button(root,text="order").pack(side="bottom")

frame_burger = LabelFrame(root,text="burger",relief="solid", bd=1)
frame_burger.pack(side="left",fill="both" , expand=True)

btnburger1=Button(frame_burger, text="hamburger").pack()
btnburger2=Button(frame_burger, text="cheese burger").pack()
btnburger3=Button(frame_burger, text="apple burger").pack()

frame_drink=LabelFrame(root, text="음료",bd=1)
frame_drink.pack(side="right",fill="both",expand=True)
btndrink1=Button(frame_drink, text="cola").pack()
btndrink2=Button(frame_drink, text="fanta").pack()

root.mainloop()     