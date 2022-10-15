from tkinter import *

root = Tk()
root.title("GUI Test")
root.geometry("640x480")

def new_file():
    print("new file!")
    
mainmenu = Menu(root)

# File
mainmenu_file=Menu(mainmenu,tearoff=0)
mainmenu_file.add_command(label="New File", command=new_file)
mainmenu_file.add_command(label="New Window")
mainmenu_file.add_separator()
mainmenu_file.add_command(label="Open File...")
mainmenu_file.add_separator()
mainmenu_file.add_command(label="Save All", state="disable")
mainmenu_file.add_separator()
mainmenu_file.add_command(label="Exit", command = root.quit)
mainmenu.add_cascade(label="File",menu=mainmenu_file)

# Edit(empty)
mainmenu.add_cascade(label="Edit")

# Language 
mainmenu_lang = Menu(mainmenu, tearoff = 0)
mainmenu_lang.add_radiobutton(label="Python")
mainmenu_lang.add_radiobutton(label="Java")
mainmenu_lang.add_radiobutton(label="C++")
mainmenu.add_cascade(label="Language", menu=mainmenu_lang)

# View
mainmenu_view = Menu(mainmenu, tearoff = 0)
mainmenu_view.add_checkbutton(label="Show minimap")
mainmenu.add_cascade(label="View", menu=mainmenu_view)


root.config(menu=mainmenu)
root.mainloop()     