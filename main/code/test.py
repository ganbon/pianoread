import cv2
import numpy as np
from function import notedetection
from function import notedetection_min
datas=[]
img=cv2.imread("result3.jpg")
datas,imglist=notedetection(img)
i=0
for data in datas:
    i+=1
    y,x,t=data
    img2=imglist[t]
    h,w,c=img2.shape
    cv2.imwrite("../cut5/cut"+str(i)+".png",img2)
    if w>100 and h>40:
        datas2,imglist2=notedetection_min(img2)
        for data2 in datas2:
            y2,x2,p=data2
            img3=imglist2[p]
            i+=1
            cv2.imwrite("../cut5/cut"+str(i)+".png",img3)


    
    

