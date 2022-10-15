from cProfile import label
from tkinter import *

root = Tk()
root.title("GUI Test")
root.geometry("640x480")

listbox = Listbox(root,selectmode="extended",height=0)
listbox.insert(0,"apple")
listbox.insert(1,"banana")
listbox.insert(2,"orange")
listbox.insert(END,"water melon")
listbox.insert(END,"mango")
listbox.pack()

def btncmd():
    #listbox.delete(0) #맨 앞을 삭제
    #listbox.delete(END) #맨 끝을 삭제
    
    #print("list size is",listbox.size()) #갯수 확인
    
    #print("1 to 3",listbox.get(0,2)) #항목 확인
    
    print("your choose is",listbox.get(listbox.curselection())) # 선택 확인
    
    
btn1=Button(root,text="click me!",command=btncmd)
btn1.pack()
root.mainloop() 