import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import glob
from sklearn import model_selection
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import keras


def one_hot(img):
    h, w, c = img.shape
    bip = []
    tresh = 128
    for i in range(h):
        e = []
        for j in range(w):
            if all(img[i][j] < 128):
                e.append(1)
            else:
                e.append(0)
        bip.append(e)
    bip = np.array(bip)
    return bip


def split(img, searchimg):
    height, width, imglist = [], [], []
    searchone_hot = one_hot(searchimg)
    sum_hot = np.sum(searchone_hot)
    img2 = cv2.resize(img, (1500, 2000))
    h, w, c = img2.shape
    for y in range(25, h-25, 1):
        for x in range(25, w-25, 1):
            img3 = img2[y:y+25, x:x+25]
            one_hot_im = one_hot(img3)
            if np.sum(one_hot_im) == 0:
                continue
            inner = searchone_hot*one_hot_im
            if 0 < sum_hot-np.sum(inner) < 25:
                cv2.line(img2, (x, y), (x+25, y+25), (0, 0, 225), 1)
                cv2.imwrite("test.png", img2)


def outputfile(img):
    files, i = split(img)
    i = 0
    for file in files:
        cv2.imwrite("../split1/split1-"+str(i)+".png", file)
        i += 1


def testdata(folder1, folder2):
    X = []
    Y = []
    classes = [folder1, folder2]
    for index, classlabel in enumerate(classes):
        files = glob.glob(classlabel+"/*.png")
        for i, file in enumerate(files):
            img = cv2.imread(file)
            data = np.asarray(img)
            X.append(data)
            Y.append(index)
    X = np.array(X)
    Y = np.array(Y)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)
    xy = (X_train, X_test, y_train, y_test)
    np.save("./dataset.npy", xy)


def model_train(X, y):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), padding='same', input_shape=X.shape[1:]))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2))
    model.add(Activation('softmax'))

    opt = keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)

    model.compile(loss='categorical_crossentropy',
                  optimizer=opt, metrics=['accuracy'])

    model.fit(X, y, batch_size=32, epochs=100)

    # モデルの保存
    model.save("./train_cnn.h5")
    return model


def model_eval(model, X, y):
    scores = model.evaluate(X, y, verbose=1)
    print('test Loss: ', scores[0])
    print('test Accuracy: ', scores[1])


def notedetection(img, pathname):
    data = []
    imglist = {}
    minsize = 40
    maxsize = 60
    #img2 = cv2.resize(img, (1500, 2000))
    height, width, channels = img.shape
    image_size = height*width
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img3 = cv2.blur(src=gray, ksize=(10, 10))
    retval, dst = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
    dst = cv2.bitwise_not(dst)
    retval, dst = cv2.threshold(
        dst, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cnt, hierarchy = cv2.findContours(
        dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i, count in enumerate(cnt):
        area = cv2.contourArea(count)
        if area < minsize:
            continue
        if image_size*0.5 < area:
            continue
        x, y, w, h = cv2.boundingRect(count)
        if h > 0:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 1)
            cv2.imwrite("../result/scoresuround/"+pathname, img)
            img2 = img[y:y+h, x-5:x+w+5]
            cod = (int(y), int(x), i)
            imglist[i] = img2
            data.append(cod)
    data.sort()
    return data, imglist


def notedetection_min(img):
    data = []
    imglist = {}
    height, width, channels = img.shape
    image_size = height*width
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = cv2.blur(src=gray, ksize=(10, 10))
    retval, dst = cv2.threshold(img2, 130, 255, cv2.THRESH_BINARY)
    dst = cv2.bitwise_not(dst)
    retval, dst = cv2.threshold(
        dst, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cnt, hierarchy = cv2.findContours(
        dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    minsize = 40
    maxsize = 60
    for i, count in enumerate(cnt):
        area = cv2.contourArea(count)
        if area < minsize:
            continue
        if image_size*0.5 < area:
            continue
        x, y, w, h = cv2.boundingRect(count)
        cv2.imwrite('c.png', img)
        if w < 50:
            cod = (int(x), int(y), i)
            img3 = img[0:height, x-5:x+w+5]
            imglist[i] = img3
            data.append(cod)
    data.sort()
    return data, imglist
