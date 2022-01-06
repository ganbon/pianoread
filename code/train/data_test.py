import tensorflow.keras
import numpy as np
from tensorflow.keras.models import load_model
import cv2
import os
import warnings
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
# 音符の判定

def result_img(img_path, train_data):
    warnings.simplefilter('ignore')
    model = load_model(train_data)
    img = cv2.imread(img_path)
    img_resize = cv2.resize(img, (50, 100))
    img2 = np.asarray(img_resize)
    img2 = img2 / 255.0
    prd = model.predict(np.array([img2]))
    #print(prd)  # 精度の表示
    prelabel = np.argmax(prd, axis=1)
    if np.max(prd) < 0.7:
        #print("none")
        return -1
    if prelabel == 0:
        #print(">>>2on")
        return 2
    elif prelabel == 1:
        #print(">>>4on")
        return 4
    elif prelabel == 2:
        #print(">>>8on")
        return 8
    elif prelabel == 3:
        #print(">>16on")
        return 16
    elif prelabel == 4:
        #print(">>8kyu")
        return -8
    elif prelabel == 5:
        #print(">4kyu")
        return -4
    elif prelabel == 6:
        #print(">>allon")
        return 1
