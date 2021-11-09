import os
import cv2
import glob
import numpy as np
from function import notedetection
from function import notedetection_min
n = 0
datas = []
names = glob.glob("../result/tateline/*")
for name in names:
    img = cv2.imread(name)
    print("OK")
    namepath = os.path.split(name)
    datas, imglist = notedetection(img, namepath[1])
    i = 0
    for data in datas:
        y, x, t = data
        img2 = imglist[t]
        h, w, c = img2.shape
        try:
            namepath = os.path.split(name)
            pathname = namepath[1].replace('.png', '')
            cv2.imwrite("../result/"+ pathname +"/cut"+str(i)+".png", img2)
            i += 1
        except cv2.error:
            continue
        if w > 100 and h > 40:
            datas2, imglist2 = notedetection_min(img2)
            for data2 in datas2:
                y2, x2, p = data2
                img3 = imglist2[p]
                try:
                    namepath = os.path.split(name)
                    pathname = namepath[1].replace('.png', '')
                    cv2.imwrite("../result/"+pathname + "/cut"+str(i)+".png", img3)
                except cv2.error:
                    continue
                i += 1
    n += 1
