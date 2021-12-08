import keras
import numpy as np
from keras.models import load_model
import cv2
# 音符の判定
def result_img(img, train_data):
    model = load_model(train_data)
    img = cv2.resize(img,(50, 100))
    img = np.asarray(img)
    img = img / 255.0
    prd = model.predict(np.array([img]))
    #print(prd)  # 精度の表示
    prelabel = np.argmax(prd, axis=1)
    if np.max(prd) < 0.8:
        #print("none")
        return -1
    elif prelabel == 0:
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
