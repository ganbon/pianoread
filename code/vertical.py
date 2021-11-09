import os
import glob
import cv2
from mng_score import Score
import numpy as np
names = glob.glob("../result/lineout/*")
datas = glob.glob("../testdata/*")
black = [0, 0, 0]
white = [255, 255, 255]


def scoreline_data(path):
    PATH = path
    print(path)
    score = Score(PATH)
    lines_data, pitch = score.detect_lines()
    if pitch == 0:
        return
    score.register_stf(lines_data)
    print(lines_data)
    return lines_data


for data, name in zip(datas, names):
    img = cv2.imread(name)
    height, width = img.shape[:2]
    print(height,width)
    hlines = scoreline_data(data)
    if hlines==None:
        continue
    namepath = os.path.split(name)
    for i, hline in enumerate(hlines):
        scoreheight_head = hline[0][0][0]
        try:
            scoreheight_end = hline[1][4][0]
        except IndexError:
            scoreheight_end = hline[0][4][0]
        scorerange = (scoreheight_end-scoreheight_head)*0.8
        print(scorerange)
        for m in range(width):
            check = 0
            for j in range(int(scoreheight_head), int(scoreheight_end)):
                if (img[j, m] == white).all():
                    continue
                else:
                    check += 1
            if check > scorerange:
                cv2.line(img, (m, int(scoreheight_head)),
                         (m, int(scoreheight_end)), (255, 255, 255), 3)
    cv2.imwrite("../result/tateline/"+namepath[1], img)
