from tkinter import *

root = Tk()
root.title("GUI Test")
root.geometry("1920x1080")
root.resizable(False,False) # x , y 값 변경불가 (창크기)

key = 0
def keyclick(e) :
    global key
    key = e.keycode
    print("입력 코드 :" , str(key))
    
root.bind("<Key>",keyclick)    
root.mainloop()