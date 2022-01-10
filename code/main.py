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
unpack_list = [] 
note_info = [] #音符の種類。音階のデータセット
train_data = "../train_data/train_cnn_note.h5" #訓練データ
origin_path = input() #楽譜のpath、コマンドで入力
a = time.time()
print(a-start)
origin_img = cv2.imread(origin_path) #楽譜の画像データ
horizonal_del_img = horizonal_del(origin_path) #楽譜の五線（横線）を消した画像データ
b = time.time()
print(b-a)
ver_datas, vertical_del_img = vertical_data(horizonal_del_img, origin_path) #楽譜の小節線（縦線）を消した画像データ
c = time.time()
print(c-b)
note_datas = notedetection(vertical_del_img, origin_path) #音符を切り取った座標データ
note_datas=sum(note_datas,[])
note_datas=sum(note_datas,[])
d = time.time()
print(d-c)
for i,note in enumerate(note_datas):
    note_write(note[0],i,vertical_del_img) #音符を画像ファイルとして保存(音符の種類判定用)
e = time.time()
print(e-d)
files = ["../result/"+str(i)+".png" for i in range(len(note_datas))] #ファイルの名前のリスト（順番に処理する用）
for img_data, coor in zip(files, note_datas):
    unpack_list.append([origin_path, img_data, coor])
with ThreadPoolExecutor(max_workers=50) as executor:
    notes = executor.map(data_unpack, unpack_list, timeout=None) #音符の音階、種類などを判定
for note in notes:
    note_info.append(note) 
print(time.time()-start)
df = pd.DataFrame(data=note_info, columns=['note', ',kind', 'scale']) #pandasの表形式でデータを格納
df.to_csv("test.csv") #csvファイルで保存
print(time.time()-start)
