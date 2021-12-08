import cv2
import os
import pandas as pd
from note.note_scale import scale_disc
from horizonal_line.del_line import horizonal_del
from vertical_line.vertical import vertical_data
from note.cut_note import notedetection, notedetection_min
from train.data_test import result_img
music_score = []
note_info = []
train_data = "../train_data/train_cnn_note.h5"
path = input()
img = cv2.imread(path)
img2 = horizonal_del(path)
ver_datas, img3 = vertical_data(img2, path)
note_datas = notedetection(img3, path)
for data in note_datas:
    x, y, h, w = data
    note_img = img[y:y+h, x-5:x+w+5]
    height, width = note_img.shape[:2]
    try:
        note_kind = result_img(note_img, train_data)
        note_scale = scale_disc(path, data)
        if note_kind != -1:
            note_info.append((data, note_kind, note_scale))
        #cv2.imwrite("../result2/"+ filename +"/cut"+str(i)+".png", node_img)
    except cv2.error:
        continue
    if width > 100 and height > 40:
        min_note_datas, min_imgs = notedetection_min(note_img)
        for min_note in min_note_datas:
            y2, x2, w, h = min_note
            min_note_img = img[0:height, x-5:x+w+5]
            try:
                note_kind = result_img(min_imgs, train_data)
                note_scale = scale_disc(path, data)
                if note_kind != -1:
                    note_info.append((min_note, note_kind, note_scale))
                #cv2.imwrite("../result2/"+filename + "/cut"+str(i)+".png", min_note_img)
            except cv2.error:
                continue
for note in note_info:
    df = pd.DataFrame([note[0], note[1], note[2]],
                      columns=['note', ',kind', 'scale'])
    df.to_csv("test.csv")
