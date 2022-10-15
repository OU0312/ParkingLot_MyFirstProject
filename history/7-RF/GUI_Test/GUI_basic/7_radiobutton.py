import time
import tkinter.ttk as ttk
from tkinter import *

root = Tk()
root.title("GUI Test")
root.geometry("640x480")

# pgbar = ttk.Progressbar(root, maximum=100, mode="indeterminate")
# pgbar = ttk.Progressbar(root, maximum=100, mode="determinate")

p_var = DoubleVar()
pgbar = ttk.Progressbar(root, maximum=100, length = 150, variable = p_var, mode="determinate")
pgbar.pack()

def btncmd():
    for i in range(1,101) : # 1 ~ 100 
        time.sleep(0.01)
        p_var.set(i)
        pgbar.update()
        print(p_var.get())
        
    
    
btn1=Button(root,text="click me!",command=btncmd)
btn1.pack()
root.mainloop() 

