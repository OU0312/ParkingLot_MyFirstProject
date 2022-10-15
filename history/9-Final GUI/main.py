from PIL import Image
from PIL import ImageTk
import tkinter as tk
import tkinter.ttk as ttk
import threading
import datetime
import cv2
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import serial
import time
from datetime import datetime

db = {}

py_serial = serial.Serial(
        
        # Window port
        port='COM4',
        
        # 보드 레이트 (통신 속도)
        baudrate=9600,
        
        timeout=10
)

img_counter1 = 0
img_counter2 = 0

def camThread():
    global color,color2
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
            cv2.imshow('uvc1',color)
            image = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            
            cv2.imshow('uvc2',color2)
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

def moneyupdate():
    while True :
        time.sleep(1)
        for i in db:
            past = datetime.strptime(db[i][1], "%Y-%m-%d / %H:%M:%S")
            now = datetime.now()
            diff = now - past
            if diff.seconds % 60 == 0 :
                if db[i][2] <= 8000 :
                    db[i][2] = db[i][2]+1000
                    
                elif db[i][2] >= 9000 :
                    db[i][2] = 9999

def hangeul_to_carnum(h) :
    if h == 'g' :
        carnum = "123가4567"
    elif h == 'n' :
        carnum = "261나6752"
    elif h == 'd' :
        carnum = "321다9981"
    elif h == 'r' :
        carnum = "450라2512"
    elif h == 'm' :
        carnum = "565마2547"
    elif h == 'b' :
        carnum = "951바5452"
    elif h == 's' :
        carnum = "777사7777"
    elif h == 'a' :
        carnum = "678아1229"
    elif h == 'o' :
        carnum = "570어5971"
    elif h == 'j' :
        carnum = "789자4123"
    elif h == 'h' :
        carnum = "234하5678"
    return carnum

def hangeul_to_db(hangeul) :
    carnum = hangeul_to_carnum(hangeul)
    intime = datetime.now()
    paymoney = 1000
    data = {}
    data[hangeul] = [carnum,datetime.strftime(intime, "%Y-%m-%d / %H:%M:%S"),paymoney]
    return data[hangeul]

def charToArduino(camstate,chars):
    hanguel_list_all = ["가","기","나","니","다","디","라","리","마","미","먀","므","바","비","뱌","브","사","시","샤","스","아","이","야","으","어","여","자","지","쟈","즈","하","히","햐","흐"]
    hanguel_list_ga = ["가","기","갸","그"]
    hanguel_list_na = ["나","니","냐","느"]
    hanguel_list_da = ["다","디","댜","드"]
    hanguel_list_ra = ["라","리","랴","르"]
    hanguel_list_ma = ["마","미","먀"]
    hanguel_list_ba = ["바","비","뱌","브"]
    hanguel_list_sa = ["사","시","샤","스"]
    hanguel_list_ah = ["아","이","야","으"]
    hanguel_list_ah2 = ["어","여"]
    hanguel_list_ja = ["자","지","쟈","즈"]
    hanguel_list_ha = ["하","히","햐","흐"]
    number_list = ['1','2','3','4','5','6','7','8','9','0']
    
    errorlog='e' # 에러 시리얼
    errorstate=False
    str = chars #문자열
    str_list = list(str) #한글자씩 배열
    hanguel = str_list.pop(3) #list에서 한글 빼기
    if hanguel not in hanguel_list_all :
        str_list.insert(3,hanguel)
        errorstate=True
    print(str_list)
    hanguel_change = ''
    #str_list_count = len(str_list)

    if hanguel not in hanguel_list_all: # 한글이 아닌 경우
        py_serial.write(errorlog.encode('utf-8'))
        time.sleep(0.1)
        errorstate=True

    if hanguel in hanguel_list_ga and errorstate!=True:
        hanguel_change = "g"
    
    elif hanguel in hanguel_list_na and errorstate!=True:
        hanguel_change = "n"

    elif hanguel in hanguel_list_da and errorstate!=True:
        hanguel_change = "d"
        
    elif hanguel in hanguel_list_ra and errorstate!=True:
        hanguel_change = "r"
        
    elif hanguel in hanguel_list_ma and errorstate!=True:
        hanguel_change = "m"
        
    elif hanguel in hanguel_list_ba and errorstate!=True:
        hanguel_change = "b"

    elif hanguel in hanguel_list_sa and errorstate!=True:
        hanguel_change = "s"

    elif hanguel in hanguel_list_ah and errorstate!=True:
        hanguel_change = "a"
        
    elif hanguel in hanguel_list_ah2 and errorstate!=True:
        hanguel_change = "o"

    elif hanguel in hanguel_list_ja and errorstate!=True:
        hanguel_change = "j"
        
    elif hanguel in hanguel_list_ha and errorstate!=True:
        hanguel_change = "h"
    
    if str_list[0] not in number_list and errorstate==True:
        str_list.pop(0)


    if str_list[0] == '1' and errorstate==True:
        if str_list[1] == '2' :
            if str_list[2] == '3' :
                hanguel_change = "g"
    
    elif str_list[0] == '2' and errorstate==True:
        if str_list[1] == '6' :
            if str_list[2] == '1' :
                hanguel_change = "n"
                
    elif str_list[0] == '3' and errorstate==True:
        if str_list[1] == '2' :
            if str_list[2] == '1' :
                hanguel_change = "d"
                
    elif str_list[0] == '4' and errorstate==True:
        if str_list[1] == '5' :
            if str_list[2] == '0' :
                hanguel_change = "r"
                
    elif str_list[0] == '5' and errorstate==True:
        if str_list[1] == '6' :
            if str_list[2] == '5' :
                hanguel_change = "m"
                
    elif str_list[0] == '9' and errorstate==True:
        if str_list[1] == '5' :
            if str_list[2] == '1' :
                hanguel_change = "b"
                
    elif str_list[0] == '7' and errorstate==True:
        if str_list[1] == '7' :
            if str_list[2] == '7' :
                hanguel_change = "s"
                
    elif str_list[0] == '6' and errorstate==True:
        if str_list[1] == '7' :
            if str_list[2] == '8' :
                hanguel_change = "a"
                
    if str_list[0] == '5' and errorstate==True:
        if str_list[1] == '7' :
            if str_list[2] == '0' :
                hanguel_change = "o"
    
    elif str_list[0] == '7' and errorstate==True:
        if str_list[1] == '8' :
            if str_list[2] == '9' :
                hanguel_change = "j"
                
    elif str_list[0] == '2' and errorstate==True:
        if str_list[1] == '3' :
            if str_list[2] == '4' :
                hanguel_change = "h"
    
    carnum = hangeul_to_carnum(hanguel_change)
    
    if camstate == "IN" :
        if hanguel_change not in db :
            db[hanguel_change] = hangeul_to_db(hanguel_change)
            print(carnum,"입차")
            py_serial.write(hanguel_change.encode('utf-8'))
            time.sleep(0.1)
            
    elif camstate == "OUT" :
        if hanguel_change in db :
            del(db[hanguel_change])
            print(carnum,"출차")
            py_serial.write(hanguel_change.encode('utf-8'))
            time.sleep(0.1)
    
def framein(camstate,frame,img_counter):
    print(camstate)
    img_name = "opencv_frame_{}.png".format(img_counter)
    cv2.imwrite(img_name, frame)
    print("캡처완료")
    #img_counter += 1 // 이미지 카운터
    #cam.release() 캠 멈추기임
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #img_ori = cv2.imread('C:\Python Project\opencv_frame_0.png') 사진읽기
    img_ori = cv2.imread(img_name)
    height, width, channel = img_ori.shape
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    plt.figure(figsize=(12, 10))
    plt.imshow(img_ori,cmap='gray')
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)

    img_blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=0)
    img_blur_thresh = cv2.adaptiveThreshold(
    img_blurred,
    maxValue=255.0,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY_INV,
    blockSize=19,
    C=9
    )
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    img_thresh = cv2.adaptiveThreshold(
    gray,
    maxValue=255.0,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY_INV,
    blockSize=19,
    C=9
    )
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    contours, _ = cv2.findContours(
    img_blur_thresh,
    mode=cv2.RETR_LIST,
    method=cv2.CHAIN_APPROX_SIMPLE
    )

    temp_result = np.zeros((height, width, channel), dtype=np.uint8)

    cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255,255,255))

    plt.figure(figsize=(12, 10))

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    temp_result = np.zeros((height, width, channel), dtype=np.uint8)

    contours_dict = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(temp_result, pt1=(x,y), pt2=(x+w, y+h), color=(255,255,255), thickness=2)

        contours_dict.append({
        'contour': contour,
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'cx': x + (w / 2),
        'cy': y + (h / 2)
    })

    plt.figure(figsize=(12,10))

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    MIN_AREA = 80
    MIN_WIDTH, MIN_HEIGHT=2, 8
    MIN_RATIO, MAX_RATIO = 0.25, 1.0

    possible_contours = []

    cnt = 0
    for d in contours_dict:
        area = d['w'] * d['h']
        ratio = d['w'] / d['h']
        
        if area > MIN_AREA \
        and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
        and MIN_RATIO < ratio < MAX_RATIO:
            d['idx'] = cnt
            cnt += 1
            possible_contours.append(d)

    temp_result = np.zeros((height, width, channel), dtype = np.uint8)

    for d in possible_contours:
        cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(255, 255, 255), thickness=2)
        
    plt.figure(figsize=(12, 10))

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    MAX_DIAG_MULTIPLYER = 5
    MAX_ANGLE_DIFF = 12.0
    MAX_AREA_DIFF = 0.5
    MAX_WIDTH_DIFF = 0.8
    MAX_HEIGHT_DIFF = 0.2
    MIN_N_MATCHED = 3

    def find_chars(contour_list):
        matched_result_idx = []
        
        for d1 in contour_list:
            matched_contours_idx = []
            for d2 in contour_list:
                if d1['idx'] == d2['idx']:
                    continue
                    
                dx = abs(d1['cx'] - d2['cx'])
                dy = abs(d1['cy'] - d2['cy'])
                
                diagonal_length1 = np.sqrt(d1['w'] ** 2 + d1['h'] ** 2)
                
                distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))
                if dx == 0:
                    angle_diff = 90
                else:
                    angle_diff = np.degrees(np.arctan(dy / dx))
                area_diff = abs(d1['w'] * d1['h'] - d2['w'] * d2['h']) / (d1['w'] * d1['h'])
                width_diff = abs(d1['w'] - d2['w']) / d1['w']
                height_diff = abs(d1['h'] - d2['h']) / d1['h']
                
                if distance < diagonal_length1 * MAX_DIAG_MULTIPLYER \
                and angle_diff < MAX_ANGLE_DIFF and area_diff < MAX_AREA_DIFF \
                and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                    matched_contours_idx.append(d2['idx'])
                    
            matched_contours_idx.append(d1['idx'])
            
            if len(matched_contours_idx) < MIN_N_MATCHED:
                continue
                
            matched_result_idx.append(matched_contours_idx)
            
            unmatched_contour_idx = []
            for d4 in contour_list:
                if d4['idx'] not in matched_contours_idx:
                    unmatched_contour_idx.append(d4['idx'])
            
            unmatched_contour = np.take(possible_contours, unmatched_contour_idx)
            
            recursive_contour_list = find_chars(unmatched_contour)
            
            for idx in recursive_contour_list:
                matched_result_idx.append(idx)
                
            break
            
        return matched_result_idx

    result_idx = find_chars(possible_contours)

    matched_result = []
    for idx_list in result_idx:
        matched_result.append(np.take(possible_contours, idx_list))
        
    temp_result = np.zeros((height, width, channel), dtype=np.uint8)

    for r in matched_result:
        for d in r:
            cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(255,255,255), thickness=2)

    plt.figure(figsize=(12, 10))

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    PLATE_WIDTH_PADDING = 1.3 # 1.3
    PLATE_HEIGHT_PADDING = 1.5 # 1.5
    MIN_PLATE_RATIO = 3
    MAX_PLATE_RATIO = 10

    plate_imgs = []
    plate_infos = []

    for i, matched_chars in enumerate(matched_result):
        sorted_chars = sorted(matched_chars, key=lambda x: x['cx'])

        plate_cx = (sorted_chars[0]['cx'] + sorted_chars[-1]['cx']) / 2
        plate_cy = (sorted_chars[0]['cy'] + sorted_chars[-1]['cy']) / 2
        
        plate_width = (sorted_chars[-1]['x'] + sorted_chars[-1]['w'] - sorted_chars[0]['x']) * PLATE_WIDTH_PADDING
        
        sum_height = 0
        for d in sorted_chars:
            sum_height += d['h']

        plate_height = int(sum_height / len(sorted_chars) * PLATE_HEIGHT_PADDING)
        
        triangle_height = sorted_chars[-1]['cy'] - sorted_chars[0]['cy']
        triangle_hypotenus = np.linalg.norm(
            np.array([sorted_chars[0]['cx'], sorted_chars[0]['cy']]) - 
            np.array([sorted_chars[-1]['cx'], sorted_chars[-1]['cy']])
        )
        
        angle = np.degrees(np.arcsin(triangle_height / triangle_hypotenus))
        
        rotation_matrix = cv2.getRotationMatrix2D(center=(plate_cx, plate_cy), angle=angle, scale=1.0)
        
        img_rotated = cv2.warpAffine(img_thresh, M=rotation_matrix, dsize=(width, height))
        
        img_cropped = cv2.getRectSubPix(
            img_rotated, 
            patchSize=(int(plate_width), int(plate_height)), 
            center=(int(plate_cx), int(plate_cy))
        )
        
        if img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO or img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO > MAX_PLATE_RATIO:
            continue
        
        plate_imgs.append(img_cropped)
        plate_infos.append({
            'x': int(plate_cx - plate_width / 2),
            'y': int(plate_cy - plate_height / 2),
            'w': int(plate_width),
            'h': int(plate_height)
        })
        
        plt.subplot(len(matched_result), 1, i+1)
        
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    longest_idx, longest_text = -1, 0
    plate_chars = []

    for i, plate_img in enumerate(plate_imgs):
        plate_img = cv2.resize(plate_img, dsize=(0, 0), fx=1.6, fy=1.6)
        _, plate_img = cv2.threshold(plate_img, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        # find contours again (same as above)
        contours, _ = cv2.findContours(plate_img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
        
        plate_min_x, plate_min_y = plate_img.shape[1], plate_img.shape[0]
        plate_max_x, plate_max_y = 0, 0

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            area = w * h
            ratio = w / h

            if area > MIN_AREA \
            and w > MIN_WIDTH and h > MIN_HEIGHT \
            and MIN_RATIO < ratio < MAX_RATIO:
                if x < plate_min_x:
                    plate_min_x = x
                if y < plate_min_y:
                    plate_min_y = y
                if x + w > plate_max_x:
                    plate_max_x = x + w
                if y + h > plate_max_y:
                    plate_max_y = y + h
                    
        img_result = plate_img[plate_min_y:plate_max_y, plate_min_x:plate_max_x]
        
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    longest_idx, longest_text = -1, 0
    plate_chars = []

    for i, plate_img in enumerate(plate_imgs):
        plate_img = cv2.resize(plate_img, dsize=(0, 0), fx=1.6, fy=1.6)
        _, plate_img = cv2.threshold(plate_img, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        # find contours again (same as above)
        contours, _ = cv2.findContours(plate_img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
        
        plate_min_x, plate_min_y = plate_img.shape[1], plate_img.shape[0]
        plate_max_x, plate_max_y = 0, 0

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            area = w * h
            ratio = w / h

            if area > MIN_AREA \
            and w > MIN_WIDTH and h > MIN_HEIGHT \
            and MIN_RATIO < ratio < MAX_RATIO:
                if x < plate_min_x:
                    plate_min_x = x
                if y < plate_min_y:
                    plate_min_y = y
                if x + w > plate_max_x:
                    plate_max_x = x + w
                if y + h > plate_max_y:
                    plate_max_y = y + h
                    
        img_result = plate_img[plate_min_y:plate_max_y, plate_min_x:plate_max_x]
        
        img_result = cv2.GaussianBlur(img_result, ksize=(3, 3), sigmaX=0)
        _, img_result = cv2.threshold(img_result, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img_result = cv2.copyMakeBorder(img_result, top=10, bottom=10, left=10, right=10, borderType=cv2.BORDER_CONSTANT, value=(0,0,0))
        
        try :
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
            chars = pytesseract.image_to_string(img_result, lang='kor',config='--psm 7 --oem 0' )
            #chars = pytesseract.image_to_string(img_result, lang='kor')
            result_chars = ''
            has_digit = False
            for c in chars:
                if ord('가') <= ord(c) <= ord('힣') or c.isdigit():
                    if c.isdigit():
                        has_digit = True    
                    result_chars += c
            
            print(result_chars)
            plate_chars.append(result_chars)
        except :
            print("너무 길어")

        if has_digit and len(result_chars) > longest_text:
            longest_idx = i

        plt.subplot(len(plate_imgs), 1, i+1)
        
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    info = plate_infos[longest_idx]
    chars = plate_chars[longest_idx]

    print(chars)

    img_out = img_ori.copy()

    cv2.rectangle(img_out, pt1=(info['x'], info['y']), pt2=(info['x']+info['w'], info['y']+info['h']), color=(255,0,0), thickness=2)

    cv2.imwrite('result.png', img_out)
    
    plt.figure(figsize=(12, 10))
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////                
    charThread=threading.Thread(target=charToArduino, args=(camstate,chars))
    charThread.daemon = True
    charThread.start()
    
if __name__  == '__main__' :
    
    thread_img = threading.Thread(target=camThread)
    thread_img.daemon = True
    thread_img.start()
    
    thread_moneyupdate = threading.Thread(target=moneyupdate)
    thread_moneyupdate.daemon = True
    thread_moneyupdate.start()
    
    def keyclick(e) :
        global key
        key = e.keycode
        print("key input :" , key)
        if key == 73 :
            camstate="IN"
            framein(camstate,color,img_counter1)
            redata()
        elif key == 79 :
            camstate="OUT"
            framein(camstate,color2,img_counter2)
            redata()
            
    root = tk.Tk()
    root.title("main control")
    root.geometry("1920x1080")
    root.attributes('-fullscreen',True)
    root.bind("<Key>",keyclick)
    
    frame_cam = tk.LabelFrame(root,text="cam",relief="solid", bd=1,padx=250)
    frame_cam.pack(side="top",fill="both" , expand=True,padx = 5)
    
    frame_result = tk.LabelFrame(root,text="result",relief="solid", bd=1)
    frame_result.pack(side="left",fill="both" , expand=True,padx = 5)
    
    
    
    #photo_result = tk.PhotoImage(file=r"C:\Python Project\capstone\7-RF\GUI_Test\GUI_basic\src\opencv_frame_0.png")
    photo_result = tk.PhotoImage(file=r"C:\Python Project\capstone\wait.png")
    label_result = tk.Label(frame_result,image=photo_result)
    label_result.pack(side="left",fill="x" , expand=True,padx = 5)
    
    def redata() :
        global photo_result,label_result,treeview
        photo_result = tk.PhotoImage(file=r"C:\Python Project\capstone\result.png")
        label_result.configure(image=photo_result)
        print(db)
        treeview.delete(*treeview.get_children())
        for i in db :
            treeview.insert('', 'end', values=(db[i]))
        root.update()
    
    
    
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
    
    # dtime = datetime.now()
    # data = {
    #     'g' : ["123가4567",datetime.strftime(dtime, "%Y-%m-%d / %H:%M:%S"),"1000원"] ,
    #     's' : ["777사7777",dtime,"5000원"]
    # }
    # for i in data :
    #     treeview.insert('', 'end', values=(data[i]))
    
    btnout = tk.Button(frame_info, text="종료", command=root.quit, width = 5 , height = 2)
    btnout.pack(pady=25)
    root.mainloop()