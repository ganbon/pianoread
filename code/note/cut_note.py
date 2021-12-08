import cv2
from horizonal_line.line_data import scoreline_data

#音符の切り取り
def notedetection(img, path):
    data = []
    imglist = {}
    minsize = 40
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
        if area < minsize:
            continue
        if image_size*0.5 < area:
            continue
        x, y, w, h = cv2.boundingRect(count)
        if h > 0:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 1)
            #cv2.imwrite("../result/scoresuround/"+pathname, img)
            cod = (int(x), int(y), int(h), int(w))
            data.append(cod)
    note_data = note_sort(data, path)
    return note_data

#音符（連符）の分解
def notedetection_min(img):
    data = []
    imglist = {}
    height, width, channels = img.shape
    image_size = height*width
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = cv2.blur(src=gray, ksize=(10, 10))
    retval, dst = cv2.threshold(img2, 130, 255, cv2.THRESH_BINARY)
    dst = cv2.bitwise_not(dst)
    retval, dst = cv2.threshold(
        dst, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cnt, hierarchy = cv2.findContours(
        dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    minsize = 40
    for i, count in enumerate(cnt):
        area = cv2.contourArea(count)
        if area < minsize:
            continue
        if image_size*0.5 < area:
            continue
        x, y, w, h = cv2.boundingRect(count)
        if w < 50:
            cod = (int(x), int(y), int(w), int(h))
            data.append(cod)
    data.sort()
    return data, imglist

#音符を順番通りに並べる
def note_sort(datas, path):
    horizonal_datas = scoreline_data(path)
    note_data = []
    for i, horizonal_data in enumerate(horizonal_datas):
        scoreheight_head = horizonal_data[0][0][0]
        try:
            scoreheight_end = horizonal_data[1][4][0]
        except IndexError:
            scoreheight_end = horizonal_data[0][4][0]
        score_note = []
        for data in datas:
            x, y, w, h = data
            if scoreheight_head-100 < y < scoreheight_end or scoreheight_head-100 < y+h < scoreheight_end+100:
                score_note.append(data)
        score_note.sort()
        note_data[len(note_data):len(note_data)] = score_note
    return note_data
