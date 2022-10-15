import os
from tkinter import *
import tkinter.ttk
from PIL import ImageTk, Image


root = Tk()
def keyclick(e) :
    global key
    key = e.keycode
    print("key input :" , key)
    if key == 73 :
        print("i")
    elif key == 79 :
        print("o")


root.title("메모장")
root.geometry("1920x1080")
root.attributes('-fullscreen',True)
root.bind("<Key>",keyclick)

frame_cam = LabelFrame(root,text="cam",relief="solid", bd=1,padx=250)
frame_cam.pack(side="top",fill="x" , expand=True,padx = 5)

photo1 = PhotoImage(file=r"C:\Python Project\capstone\7-RF\GUI_Test\GUI_basic\src\img.png")
photo2 = PhotoImage(file=r"C:\Python Project\capstone\7-RF\GUI_Test\GUI_basic\src\img2.png")

label1 = Label(frame_cam,image=photo1) # ,height=250,width=250
label1.grid(row=0,column=1,padx=3)

label2 = Label(frame_cam,image=photo2)
label2.grid(row=0,column=2,padx=3)


frame_result = LabelFrame(root,text="result",relief="solid", bd=1)
frame_result.pack(side="left",fill="both" , expand=True,padx = 5)

photo3 = PhotoImage(file=r"C:\Python Project\capstone\7-RF\GUI_Test\GUI_basic\src\opencv_frame_0.png")
label3 = Label(frame_result,image=photo3)
label3.grid(row=0,column=0,padx=3,pady=3)


frame_info = LabelFrame(root,text="info",relief="solid", bd=1)
frame_info.pack(side="right",fill="both" , expand=True,padx = 5)

##
treeview=tkinter.ttk.Treeview(frame_info, columns=["one", "two","three"], displaycolumns=["one","two","three"])
treeview.pack()

# 각 컬럼 설정. 컬럼 이름, 컬럼 넓이, 정렬 등
treeview.column("#0", width=100,)
treeview.heading("#0", text="번호")

treeview.column("#1", width=100, anchor="center")
treeview.heading("one", text="입차시간", anchor="center")

treeview.column("#2", width=100, anchor="center")
treeview.heading("two", text="s", anchor="center")

treeview.column("#3", width=70, anchor="center")
treeview.heading("three", text="rank", anchor="center")

# 표에 삽입될 데이터
treelist=[("Tom", 80, 3), ("Bani", 71, 5), ("Boni", 90, 2), ("Dannel", 78, 4), ("Minho", 93, 1)]

# 표에 데이터 삽입
for i in range(len(treelist)):
    treeview.insert('', 'end', text=i, values=treelist[i], iid=str(i)+"번")


btn1 = Button(frame_info, text="종료", command=root.quit)
btn1.pack()

root.mainloop()         