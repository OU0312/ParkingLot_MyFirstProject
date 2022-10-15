import tkinter

key = 0
def keyclick(e) :
    global key
    key = e.keycode
    print("key input :" , key)
    if key == 73 :
        print("i")
    elif key == 79 :
        print("o")

tk = tkinter.Tk()
tk.title("키 입력")
tk.bind("<Key>",keyclick)
tk.mainloop()