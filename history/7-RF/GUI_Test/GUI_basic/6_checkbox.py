from tkinter import *

root = Tk()
root.title("GUI Test")
root.geometry("640x480")

chkvar = IntVar() # int형으로 값을 지정
chkbox = Checkbutton(root,text="don't check me",variable=chkvar)
# chkbox.select() # 자동 선택 처리
chkbox.deselect() # 선택 해제 처리
chkbox.pack()

chkvar2 = IntVar() # int형으로 값을 지정
chkbox2 = Checkbutton(root,text="go away",variable=chkvar2)
chkbox2.pack()

def btncmd():
    print(chkvar.get()) # 0 선택해제, 1 선택
    print(chkvar2.get())
    
    
btn1=Button(root,text="click me!",command=btncmd)
btn1.pack()
root.mainloop() 