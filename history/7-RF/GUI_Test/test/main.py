from PIL import Image
from PIL import ImageTk
import tkinter as tk
import tkinter.ttk as ttk
import threading
import datetime
import cv2
import os
import time
from parkinglot import maincontrol

def camThread():
    color = []
    cam1 = cv2.VideoCapture(1)
    cam2 = cv2.VideoCapture(0)
    panel1 = None
    panel2 = None
    
    if cam1 == None or cam2 == None :
        print("no cam")
    
    while True:
        ret,color = cam1.read()
        ret2,color2 = cam2.read()
        color = cv2.resize(color,(640,480))
        color2 = cv2.resize(color2,(640,480)) #480,360
        if (color != [] and color2!= []) :
            cv2.imshow('uvc',color)
            image = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            
            cv2.imshow('uvc',color2)
            image2 = cv2.cvtColor(color2, cv2.COLOR_BGR2RGB)
            image2 = Image.fromarray(image2)
            image2 = ImageTk.PhotoImage(image2)
            
            if panel1 is None or panel2 is None:
                panel1 = tk.Label(frame_cam,image=image)
                panel1.image = image
                panel1.pack(side="left",fill="x" , expand=True,padx = 5)
                
                panel2 = tk.Label(frame_cam,image=image2)
                panel2.image = image2
                panel2.pack(side="right",fill="x" , expand=True,padx = 5)
                
            else :
                panel1.configure(image=image)
                panel1.image = image
                panel2.configure(image=image2)
                panel2.image = image2
            
            cv2.waitKey(1)
            

if __name__  == '__main__' :
    thread_img = threading.Thread(target=camThread)
    thread_img.daemon = True
    thread_img.start()
    
    
    thread_mc = threading.Thread(target = maincontrol)
    thread_mc.start()
    
    def keyclick(e) :
        global key
        key = e.keycode
        print("key input :" , key)
        if key == 73 :
            print("in cam")
        elif key == 79 :
            print("out cam")
    
    root = tk.Tk()
    root.title("main control")
    root.geometry("1920x1080")
    root.attributes('-fullscreen',True)
    root.bind("<Key>",keyclick)
    
    frame_cam = tk.LabelFrame(root,text="cam",relief="solid", bd=1,padx=250)
    frame_cam.pack(side="top",fill="both" , expand=True,padx = 5)
    
    frame_result = tk.LabelFrame(root,text="result",relief="solid", bd=1)
    frame_result.pack(side="left",fill="both" , expand=True,padx = 5)
    
    photo3 = tk.PhotoImage(file=r"C:\Python Project\capstone\7-RF\GUI_Test\GUI_basic\src\opencv_frame_0.png")
    label3 = tk.Label(frame_result,image=photo3)
    label3.pack(side="left",fill="x" , expand=True,padx = 5)
    
    frame_info = tk.LabelFrame(root,text="info",relief="solid", bd=1)
    frame_info.pack(side="right",fill="both" , expand=True,padx = 5)
    
    treeview = ttk.Treeview(frame_info, columns=(1,2,3), height=11, show="headings")
    treeview.pack()
    
    treeview.heading(1,text="차량 번호")
    treeview.heading(2,text="입차 시간")
    treeview.heading(3,text="금액")
    
    treeview.column(1, width=200)
    treeview.column(2, width=200)
    treeview.column(3, width=200)
    
    dtime = time.strftime('%X')
    data = {
        'd' : ["123가4567",dtime,"1000원"] ,
        'b' : ["123나4567",dtime,"2000원"] ,
    }
    
    treeview.insert('', 'end', values=(data["d"]))
    treeview.insert('', 'end', values=(data["b"]))
    
    btnout = tk.Button(frame_info, text="종료", command=root.quit, width = 5 , height = 2)
    btnout.pack(pady=25)
    root.mainloop()