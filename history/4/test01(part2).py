import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import serial
import time
import threading

py_serial = serial.Serial(
    
    # Window port
    port='COM9',
    
    # 보드 레이트 (통신 속도)
    baudrate=9600,
    
    timeout=10
)

plt.style.use('dark_background')

cam1 = cv2.VideoCapture(1)
cam2 = cv2.VideoCapture(0)

# cv2.namedWindow("test")

img_counter = 0
img_counter2 = 0

while True:
    isNextFrameAvail1, frame1 = cam1.read()
    isNextFrameAvail2, frame2 = cam2.read()
    if not isNextFrameAvail1 or not isNextFrameAvail2:
        break
    frame2Resized = cv2.resize(frame2,(frame1.shape[0],frame1.shape[1]))

    # ---- Option 1 ----
    #numpy_vertical = np.vstack((frame1, frame2))
    numpy_horizontal = np.hstack((frame1, frame2))

    cv2.imshow("Result", numpy_horizontal)
    
    ret, frame = cam1.read()
    ret2, frame2 = cam2.read()
    if not ret:
        print("failed to grab frame")
        break
    #cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("프로그램 종료중")
        break
    elif k%256 == ord('i'):
        # 'i' pressed
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
        def charToArduino():
            hanguel_list_all = ["가","기","나","니","다","디"] 
            hanguel_list_ga = ["가","기"]
            hanguel_list_na = ["나","니","냐","느"]
            hanguel_list_da = ["다","디"]
            number_list_all = ['1','2','3','4','5','6','7','8','9','0']

            errorlog='e' # 에러 시리얼
            errorstate=False
            str = chars #문자열
            str_list = list(str) #한글자씩 배열
            hanguel = str_list.pop(3) #list에서 한글 빼기
            print(str_list)
            str_list_count = len(str_list)

            if hanguel not in hanguel_list_all or errorstate==True: # 한글이 아닌 경우
                py_serial.write(errorlog.encode('utf-8'))
                time.sleep(0.1)
                errorstate=True

            elif hanguel in hanguel_list_ga and errorstate!=True:
                hanguel_change = "a"
                py_serial.write(hanguel_change.encode('utf-8'))
                time.sleep(0.1)

            elif hanguel in hanguel_list_na and errorstate!=True:
                hanguel_change = "n"
                py_serial.write(hanguel_change.encode('utf-8'))
                time.sleep(0.1)

            elif hanguel in hanguel_list_da and errorstate!=True:
                hanguel_change = "d"
                py_serial.write(hanguel_change.encode('utf-8'))
                time.sleep(0.1)
                
        charThread=threading.Thread(target=charToArduino)
        charThread.start()
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        #cv2.imshow('img',temp_result) // 윤곽
        #cv2.imshow('img',img_out) // 결과
        cv2.waitKey(0)
        cv2.destroyAllWindows

# 2번째 카메라 ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    elif k%256 == ord('o'):
        # 'o' pressed
        img_name2 = "opencv_frame_{}.png".format(img_counter2)
        cv2.imwrite(img_name2, frame2)
        print("캡처완료")
        #img_counter += 1 // 이미지 카운터
        #cam.release() 캠 멈추기임
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        #img_ori = cv2.imread('C:\Python Project\opencv_frame_0.png') 사진읽기
        img_ori2 = cv2.imread(img_name2)
        height, width, channel = img_ori2.shape
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        plt.figure(figsize=(12, 10))
        plt.imshow(img_ori,cmap='gray')
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        gray = cv2.cvtColor(img_ori2, cv2.COLOR_BGR2GRAY)

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

# enter here

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


        #cv2.imshow('img',temp_result) // 윤곽
        #cv2.imshow('img',img_out) // 결과
        cv2.waitKey(0)
        cv2.destroyAllWindows
