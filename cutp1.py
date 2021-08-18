import cv2
import numpy as np
t = []
n=[]
img = cv2.imread("sample_piano_score.jpg")
img2 = cv2.resize(img, (1240, 1754))
height = img2.shape[0]
width = img2.shape[1]
img3 = img2.copy()

# グレースケール
gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)

# 反転 ネガポジ変換
gray2 = cv2.bitwise_not(gray)
lines = cv2.HoughLinesP(gray2, rho=1, theta=np.pi/360,
                        threshold=80, minLineLength=1000, maxLineGap=5)
for line in lines:
    x1, y1, x2, y2 = line[0]
    if y1 == y2:
        # cv2.line(img3, (x1,y1), (x2,y2), (0,0,255), 1)
        t.append(y2)
t = list(set(t))
t = sorted(t)


def lineset(m, y):
    for i in range(len(m)):
        if i == len(m):
            break
        k = m[i]
        m = list(filter(lambda x: x == k or x-k > y or x-k < 0, m))
    return m


# 縦線
r = lineset(t, 25)

def cutline(lines):
    v = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x1 == x2 and 60 < y1-y2:
            v.append(x1)
    v = list(set(v))
    v = sorted(v)
    v2 = lineset(v, 100)
    return v2

for i in range(0, len(r), 2):
    v=[]
    if i == 0:
        img4 = img2[r[i]-50:r[i+1]+30, 0:int(width)]
        cv2.imwrite("pic2/test1-"+str(i)+".png",img4)
        height2 = img4.shape[0]
        width2 = img4.shape[1]
        gray = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.bitwise_not(gray)
        lines2 = cv2.HoughLinesP(
            gray2, rho=1, theta=np.pi/360, threshold=1, minLineLength=1, maxLineGap=5)
        v = cutline(lines2)
        for j in range(len(v)-1):
            img5 = img4[0:int(height2), v[j]-5:v[j+1]]
            cv2.imwrite("pic2/score"+str(i)+"-"+str(j)+".png", img5)

    elif i == len(r)-2:
        img4 = img2[r[i-1]+20:r[i+1]+70, 0:int(width)]
        cv2.imwrite("pic2/test1-"+str(i)+".png",img4)
        height2 = img4.shape[0]
        width2 = img4.shape[1]
        gray = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.bitwise_not(gray)
        lines2 = cv2.HoughLinesP(
            gray2, rho=1, theta=np.pi/360, threshold=1, minLineLength=1, maxLineGap=5)
        v = cutline(lines2)
        for j in range(len(v)-1):
            img5 = img4[0:int(height2), v[j]-5:v[j+1]]
            cv2.imwrite("pic2/score"+str(i)+"-"+str(j)+".png", img5)
    elif i % 4:
        e = int((r[i+1]+r[i+2])/2)
        img4 = img2[r[i]-50:e+20, 0:int(width)]
        cv2.imwrite("pic2/test1-"+str(i)+".png",img4)
        height2 = img4.shape[0]
        width2 = img4.shape[1]
        gray = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.bitwise_not(gray)
        lines2 = cv2.HoughLinesP(
            gray2, rho=1, theta=np.pi/360, threshold=1, minLineLength=1, maxLineGap=5)
        v = cutline(lines2)
        for j in range(len(v)-1):
            img5 = img4[0:int(height2), v[j]-5:v[j+1]]
            cv2.imwrite("pic2/score"+str(i)+"-"+str(j)+".png", img5)
    else:
        e = int((r[i]+r[i-1])/2)
        img4 = img2[e:r[i+2]-30, 0:int(width)]
        cv2.imwrite("pic2/test1-"+str(i)+".png",img4)
        height2 = img4.shape[0]
        width2 = img4.shape[1]
        gray = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.bitwise_not(gray)
        lines2 = cv2.HoughLinesP(
            gray2, rho=1, theta=np.pi/360, threshold=1, minLineLength=1, maxLineGap=5)
        v = cutline(lines2)
        for j in range(len(v)-1):
            img5 = img4[0:int(height2), v[j]-5:v[j+1]]
            cv2.imwrite("pic2/score"+str(i)+"-"+str(j)+".png", img5)

