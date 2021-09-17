import cv2
import numpy as np
from PIL import Image
img = cv2.imread("../pic18/18.jpg")
img2 = cv2.resize(img, (2500, 3400))
height = img2.shape[0]
width = img2.shape[1]
img3 = img2.copy()
t = 0
black = [0, 0, 0]
white = [255, 255, 255]


def lineset(m, y):
    for i in range(len(m)):
        if i == len(m):
            break
        k = m[i]
        m = list(filter(lambda x: x == k or x-k > y or x-k < 0, m))
    return m


def yokoline(img, x, y):
    v = []
    w = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.bitwise_not(gray)
    lines = cv2.HoughLinesP(gray2, rho=1, theta=np.pi/360,
                            threshold=100, minLineLength=x, maxLineGap=5)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if y1 == y2:
            v.append(y1)
            #cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
            #cv2.imwrite("../pic20/test2.png", img)
    v = list(set(v))
    v = sorted(v)
    v = lineset(v, y)
    #print(len(v))
    a = int(v[1]-v[0])
    b = int(v[4]-v[0])
    return a, b, v


def tateline(img,x):
    p = []
    height = img.shape[0]
    width = img.shape[1]
    a, b, v = yokoline(img, width*0.6, x)
    im = img[v[0]:v[9], 0:int(width)]
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.bitwise_not(gray)
    lines = cv2.HoughLinesP(gray2, rho=1, theta=np.pi/360,
                                threshold=1, minLineLength=1, maxLineGap=5)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x1 == x2 and y1-y2 > v[9]-v[0]-5:
            p.append(x1)
            cv2.line(img, (x1, v[4]+10),
                         (x2, v[5]-10), (255, 255, 255), 3)
            cv2.imwrite("../pic18/test.png", img)
    p = list(set(p))
    p = sorted(p)
    p = lineset(p, 100)
    return img, p


a, b, v = yokoline(img3, width*0.6, 15)
img4 = img3[v[0]-a*7:v[len(v)-1]+a*7, 0:int(width)]
a, b, v = yokoline(img4, width*0.6, 15)
height2 = img4.shape[0]
width2 = img4.shape[1]
img5 = cv2.resize(img4, (int(width2*5.0), int(height2*5.0)))

while(1):
    print('OK')
    m, n, y1, y2 = 0, 0, 0, 0
    if len(v) == 10:
        break
    height3 = img5.shape[0]
    widht3 = img5.shape[1]
    a, b, v = yokoline(img5, widht3*0.7, 50)
    print(len(v))
    retval, im2 = cv2.threshold(img5, 130, 255, cv2.THRESH_BINARY)
    if t==0 or t%2==0:
        img5, p = tateline(img5,50)
        retval, im2 = cv2.threshold(img5, 130, 255, cv2.THRESH_BINARY)
        for i in range(v[0], v[9]):
            for j in range(p[0]):
                if (im2[i, j] == black).all():
                    img5[i, j] = white
                    im2[i, j] = white
    cv2.imwrite("../pic18/test2.png", im2)



    for i in range(v[0]):
        for j in range(widht3):
            r = im2[i, j]
            if (r == white).all():
                continue
            else:
                m += 1
                break
        if m > 0:
            y1 = i
            break

    for i in range(v[4], v[5]):
        for j in range(widht3):
            r = im2[i, j]
            if (r == black).all():
                break
            if j == widht3-1:
                y2 = i
        if y2 > 0:
            break

    img6 = img5[y1:y2+50, 0:int(widht3)]
    img5 = img5[y2+50:int(height3), 0:int(widht3)]
    cv2.imwrite("../pic18/test1-"+str(t)+".png", img6)
    if len(v) == 10:
        cv2.imwrite("../pic18/test1-"+str(t+1)+".png", img5)
    t += 1

