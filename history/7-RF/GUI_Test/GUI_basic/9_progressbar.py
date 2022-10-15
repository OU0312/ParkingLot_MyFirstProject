from tkinter import *

root = Tk()
root.title("GUI Test")
root.geometry("640x480")

label1 = Label(root, text="choose your menu").pack()

burgerVar=IntVar()
btn_burger1=Radiobutton(root,text="Hamburger",value=1,variable=burgerVar)
btn_burger1.select()
btn_burger2=Radiobutton(root,text="Cheese burger",value=2,variable=burgerVar)
btn_burger3=Radiobutton(root,text="Apple burger",value=3,variable=burgerVar)

btn_burger1.pack()
btn_burger2.pack()
btn_burger3.pack()

drinkVar=StringVar()
btn_drink1=Radiobutton(root,text="Cola",value="Cola",variable=drinkVar)
btn_drink2=Radiobutton(root,text="eel juice",value="eel juice",variable=drinkVar)
btn_drink1.select()

btn_drink1.pack()
btn_drink2.pack()
def btncmd():
    print(burgerVar.get())
    print(drinkVar.get())
    
    
btn1=Button(root,text="click me!",command=btncmd)
btn1.pack()
root.mainloop() 