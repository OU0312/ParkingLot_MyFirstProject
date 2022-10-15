import os
from tkinter import *

root = Tk()
root.title("메모장")
root.geometry("640x480")

#menu

file_name = "mynote.txt"


def open_file() :
    if os.path.isfile(file_name):
        with open(file_name,"r",encoding="utf8") as file:
            txt1.insert(END, file.read())
    else :
        txt1.insert(END,"no file")

def save_file() :
    with open(file_name,"w",encoding="utf8") as file:
        file.write(txt1.get("1.0",END))

menu=Menu(root)

menu_file = Menu(menu,tearoff=0)
menu_file.add_command(label="열기", command=open_file)
menu_file.add_command(label="저장", command=save_file)
menu_file.add_command(label="끝내기", command = root.quit)
menu.add_cascade(label="파일",menu=menu_file)

menu_edit = Menu(menu,tearoff=0)
menu.add_cascade(label="편집",menu=menu_edit)

menu_style = Menu(menu,tearoff=0)
menu.add_cascade(label="서식",menu=menu_style)

menu_look = Menu(menu,tearoff=0)
menu.add_cascade(label="보기",menu=menu_look)

menu_help = Menu(menu,tearoff=0)
menu.add_cascade(label="도움말",menu=menu_help)

# scroll
scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")


# txt
txt1 = Text(root, width=300, height=500,yscrollcommand=scrollbar.set)
txt1.pack()



scrollbar.config(command=txt1.yview)
root.config(menu=menu)
root.mainloop()         