from PIL import Image
import cv2
import glob
import numpy as np
from sklearn import model_selection
classes = ["2on", "4on", "8on", "16on", "8kyu", "4kyu", "allon"]
num_classes = len(classes)
img_widh = 50
img_height = 100

X = []
Y = []
for index, classlabel in enumerate(classes):
    photos_dir = "../../notedata_set/" + classlabel
    files = glob.glob(photos_dir + "/*.png")
    for i, file in enumerate(files):
        if i >= 300:    
            break
        img = cv2.imread(file)
        data = cv2.resize(img,(img_widh, img_height))
        X.append(data)
        Y.append(index)
X = np.array(X)
Y = np.array(Y)
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
np.save("../../notedata_set/note.npy", xy)
