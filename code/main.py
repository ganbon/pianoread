import cv2
import numpy as np
import pandas as pd
from note.note_info import data_unpack
from horizonal_line.del_line import horizonal_del
from vertical_line.vertical import vertical_data
from note.cut_note import notedetection,note_write
from concurrent.futures import ThreadPoolExecutor
import time
start = time.time()
func_list = []
note_info = []
train_data = "../train_data/train_cnn_note.h5"
path = input()
a = time.time()
print(a-start)
img = cv2.imread(path)
img2 = horizonal_del(path)
b = time.time()
print(b-a)
ver_datas, img3 = vertical_data(img2, path)
c = time.time()
print(c-b)
note_datas = notedetection(img3, path)
note_data_s=sum(note_datas,[])
note_data_s=sum(note_data_s,[])
d = time.time()
print(d-c)
for i,note in enumerate(note_data_s):
    note_write(note[0],i,img3)
e = time.time()
print(e-d)
files = ["../result/"+str(i)+".png" for i in range(len(note_data_s))]
for img_data, coor in zip(files, note_data_s):
    func_list.append([path, img_data, coor])
with ThreadPoolExecutor(max_workers=50) as executor:
    notes = executor.map(data_unpack, func_list, timeout=None)
for note in notes:
    note_info.append(note)
print(time.time()-start)
df = pd.DataFrame(data=note_info, columns=['note', ',kind', 'scale'])
df.to_csv("test.csv")
print(time.time()-start)
