import os
import glob
i = 0
names = glob.glob('../testdata/*')
for name in names:
    oldpath = name
    newpath = "../testdata/"+str(i)+".png"
    os.rename(oldpath, newpath)
    i += 1
