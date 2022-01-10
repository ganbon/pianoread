import cv2
import numpy as np
from horizonal_line.line_data import scoreline_data


# 音符（連符）の分解
def notedetection_min(img, score_data):
    data = []
    x_ = 0
    x, y, h, w = score_data
    height, width = img.shape[:2]
    image_size = height*width
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = cv2.blur(src=img, ksize=(10, 10))
    retval, dst = cv2.threshold(img2, 130, 255, cv2.THRESH_BINARY)
    dst = cv2.bitwise_not(dst)
    retval, dst = cv2.threshold(
        dst, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cnt, hierarchy = cv2.findContours(
        dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i, count in enumerate(cnt):
        area = cv2.contourArea(count)
        x2, y2, w2, h2 = cv2.boundingRect(count)
        #cv2.rectangle(img, (x2, y2), (x2+w2, y2+h2), (0, 0, 255), 1)
        if 15 < w2 < 50 and 10 < h2:
            cod = (int(x+x2-20), int(y), int(height), int(w2+40))
            data.append(cod)
        data = list(set(data))
    return data


# 音符の切り取り
def notedetection(img, path):
    data = []
    #img2 = cv2.resize(img, (1500, 2000))
    height, width = img.shape[:2]
    image_size = height*width
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img3 = cv2.blur(src=gray, ksize=(10, 10))
    retval, dst = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY)
    dst = cv2.bitwise_not(dst)
    retval, dst = cv2.threshold(
        dst, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cnt, hierarchy = cv2.findContours(
        dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for number, count in enumerate(cnt):
        area = cv2.contourArea(count)
        x, y, w, h = cv2.boundingRect(count)
        if h > 20 and w > 20:
            #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 1)
            #cv2.imwrite("../test3.png", img)
            note_img = img[y:y+h, x-5:x+w+5]
            cod = (int(x), int(y), int(h), int(w))
            if w > 80 and h > 40:
                min_data = notedetection_min(note_img, cod)
                data[len(data):len(data)] = min_data
            else:
                data.append(cod)
    data = list(set(data))
    note_data = note_sort(data, path)
    return note_data

# 音符を順番通りに並べる
def note_sort(datas, path):
    horizonal_datas = scoreline_data(path)
    note_data = []
    for i, horizonal_data in enumerate(horizonal_datas):
        scoreheight_head_1 = horizonal_data[0][0][0]
        scoreheight_head_2 = horizonal_data[1][0][0]
        scoreheight_end_1 = horizonal_data[0][4][0]
        scoreheight_end_2 = horizonal_data[1][4][0]
        s_t = []
        s_c = []
        for data in datas:
            x, y, w, h = data
            if scoreheight_head_1-100 < y < scoreheight_end_1 or scoreheight_head_1 < y+h < scoreheight_end_1+100:
                s_t.append((data, i+1))
                s_t.sort()
            elif scoreheight_head_2-100 < y < scoreheight_end_2 or scoreheight_head_2 < y+h < scoreheight_end_2+100:
                s_c.append((data, -i-1))
                s_c.sort()
        note_data.append([s_t, s_c])
    return note_data

#音符データを画像ファイル化
#data_fix.pyの時はファイル名の重複を避けるためにファイル名を変えること
def note_write(data, i, img):
    x, y, h, w = data
    img2 = img[y:y+h, x:x+w]
    cv2.imwrite("../result/2-10-"+str(i)+".png", img2)
