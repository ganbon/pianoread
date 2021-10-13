import cv2
import numpy as np

def lineset(m, y):
    for i in range(len(m)):
        if i == len(m):
            break
        k = m[i]
        m = list(filter(lambda x: x == k or x-k > y or x-k < 0, m))
    return m

def onpu(Image):
    img = cv2.imread(Image)
    height, width, channels = img.shape
    image_size = height*width
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img2 = cv2.blur(src=gray, ksize=(10, 10))
    retval, dst = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
    dst = cv2.bitwise_not(dst)
    retval, dst = cv2.threshold(
        dst, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cnt, hierarchy = cv2.findContours(
        dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    minsize = 40
    maxsize = 60
    j,t=0,0
    for i, count in enumerate(cnt):
        area = cv2.contourArea(count)
        if area < minsize:
            continue
        if image_size*0.5 < area:
            continue

        x, y, w, h = cv2.boundingRect(count)
        if h > 0:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
            cv2.imwrite('b.png', img)
            if h > 50:
                img3 = img[y:y+h, x-5:x+w+5]
                if w>50:
                    cv2.imwrite("../cut1-1/cut"+str(j)+".png", img3)
                    j+=1
                else:
                    cv2.imwrite("../cut1-2/cut"+str(t)+".png", img3)
                    t+=1


img2 = "result.jpg"
onpu(img2)
