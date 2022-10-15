from tkinter import *

root = Tk()
root.title("GUI Test")
#root.geometry("1920x1080")
btn1 = Button(root, text="button1")
btn1.pack()

btn2 = Button(root, padx = 5, pady = 15, text="button2")
btn2.pack()

btn3 = Button(root, padx = 15, pady = 5,  text="button3")
btn3.pack()

btn4 = Button(root, width=10, height=3,  text="button4")
btn4.pack()

btn5 = Button(root, fg="red", bg='yellow',  text="button5")
btn5.pack()

photo = PhotoImage(file=r"C:\Python Project\capstone\7-RF\GUI_Test\GUI_basic\img.png")
btn6 = Button(root, image=photo)
btn6.pack()

def btncmd():
    print("hello idiot")

btn7 = Button(root, text="button event",command=btncmd)
btn7.pack()
root.mainloop()