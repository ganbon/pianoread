import cv2
from function import notedetection
img=cv2.imread("../result/lineout/test5.png")
datas2, imglist2 = notedetection(img)
print(len(datas2))