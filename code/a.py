import cv2
from train.data_test import result_img
train_data = "../train_data/train_cnn_note.h5"
img=cv2.imread("../notedata_set/2on/10000.png")
a=result_img(img,train_data)
print(a)

