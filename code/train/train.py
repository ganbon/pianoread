from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import keras
import numpy as np

#cnnで学習
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
    model.add(Dense(7))
    model.add(Activation('softmax'))

    opt = keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)

    model.compile(loss='categorical_crossentropy',
                  optimizer=opt, metrics=['accuracy'])

    model.fit(X, y, batch_size=32, epochs=25)

    # モデルの保存
    model.save("../../train_data/train_cnn_note.h5")
    return model

def model_eval(model, X, y):
    scores = model.evaluate(X, y, verbose=1)
    print('test Loss: ', scores[0])
    print('test Accuracy: ', scores[1])
    
    
classes = ["2on", "4on", "8on", "16on", "8kyu", "4kyu", "allon"]
num_classes = len(classes)
X_train, X_test, y_train, y_test = np.load("../../notedata_set/note.npy", allow_pickle=True)
X_train = X_train.astype("float") / 256
X_test = X_test.astype("float") / 256
y_train = np_utils.to_categorical(y_train, num_classes)
y_test = np_utils.to_categorical(y_test, num_classes)
model = model_train(X_train, y_train)   
model_eval(model, X_test, y_test)