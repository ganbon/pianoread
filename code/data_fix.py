import re
import cv2
import numpy as np
import pandas as pd
from note.note_info import data_unpack
from horizonal_line.del_line import horizonal_del
from vertical_line.vertical import vertical_data
from note.cut_note import notedetection, note_write
from concurrent.futures import ThreadPoolExecutor
from train.data_test import result_img
import time
import shutil
start = time.time()
music_score = []
note_coor = []
func_list = []
note_info = []
train_data = "../train_data/train_cnn_note.h5"
path = input()
img = cv2.imread(path)
img2 = horizonal_del(path)
ver_datas, img3 = vertical_data(img2, path)
del img2
note_datas = notedetection(img3, path)
note_data_s = sum(note_datas, [])
note_data_s = sum(note_data_s, [])
for i, note in enumerate(note_data_s):
    note_write(note[0], i, img3)
files = ["../result/2-8-"+str(i)+".png" for i in range(len(note_data_s))]
count=[0,0,0,0,0,0,0,0]
for img in files:
    number = result_img(img, train_data)
    if number == -1:
        count[0]+=1
        shutil.move(img, "../notedata/none/")
    elif number == 2:
        count[1]+=1;
        shutil.move(img, "../notedata/2on/")
    elif number == 4:
        count[2]+=1;
        shutil.move(img, "../notedata/4on/")
    elif number == 8:
        count[3]+=1;
        shutil.move(img, "../notedata/8on/")
    elif number == 16:
        count[4]+=1;
        shutil.move(img, "../notedata/16on/")
    elif number == -8:
        count[5]+=1;
        shutil.move(img, "../notedata/8kyu/")
    elif number == -4:
        count[6]+=1;
        shutil.move(img, "../notedata/4kyu/")
    elif number == 1:
        count[7]+=1;
        shutil.move(img, "../notedata/allon/")
print(count)
