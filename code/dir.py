import os
import glob
names = glob.glob("../result/lineout/*")
for i in range(len(names)):
    n = 0
    new_dir = "../result/test"+str(i)
    os.mkdir(new_dir)
