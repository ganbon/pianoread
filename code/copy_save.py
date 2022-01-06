import cv2
from horizonal_line.line_data import scoreline_data

# 音階判定


def scale_disc(path, img_data):
    x, y, h, w = img_data[0]
    flg = img_data[1]
    white = [255, 255, 255]
    black = [0, 0, 0]
    scale = []
    horizonal_line = scoreline_data(path)
    img = cv2.imread(path)
    note_width = int((horizonal_line[0][0][1][0]-horizonal_line[0][0][0][0])/2)
    if flg >= 0:
        basic_line = horizonal_line[flg][0][2][0]
    else:
        basic_line = horizonal_line[abs(flg)][1][2][0]
        # 0(基準)がミ
    for i in range(-15, 15):
        _y = basic_line+note_width*i
        if _y-basic_line < y:
            continue
        if _y+basic_line > y+h:
            break
        for _x in range(int(x), int(x+w)):
            if (img[_y+basic_line-5, _x] == black).all() and (img[_y-basic_line+1, _x+5] == black).all():
                scale.append(i)
    return scale
