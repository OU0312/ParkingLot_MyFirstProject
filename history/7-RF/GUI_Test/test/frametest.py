import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import serial
import time
import threading

def framein(camstate,frame,img_counter,py_serial,db):
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

    #cv2.imwrite(chars + '.jpg', img_out)

    plt.figure(figsize=(12, 10))
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    #한글 리스트
    def charToArduino(db,camstate):
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
        
        if camstate == "IN" :
            if hanguel_change not in db:
                py_serial.write(hanguel_change.encode('utf-8'))
                time.sleep(0.1)
                db.append(hanguel_change)
        else :
            if hanguel_change in db:
                py_serial.write(hanguel_change.encode('utf-8'))
                time.sleep(0.1)
                db.remove(hanguel_change)
    
                    
    charThread=threading.Thread(target=charToArduino, args=(db,camstate))
    charThread.start()
    
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #cv2.imshow('img',temp_result) // 윤곽
    #cv2.imshow('img',img_out) // 결과
    cv2.waitKey(0)
    cv2.destroyAllWindows