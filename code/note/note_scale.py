import cv2
from horizonal_line.line_data import scoreline_data

#音階判定
def scale_disc(path, img_data, img_kind):
    x, y, h, w = img_data[0]
    flg = img_data[1]
    white = [255, 255, 255]
    black = [0, 0, 0]
    scale = []
    horizonal_line = scoreline_data(path)
    img = cv2.imread(path)
    note_width = int((horizonal_line[0][0][1][0]-horizonal_line[0][0][0][0])/2)
    if flg >= 0:
        basic_line = int(horizonal_line[flg-1][0][2][0])
    else:
        basic_line = int(horizonal_line[abs(flg+1)][1][2][0])
        # 0(基準)がミ
    if img_kind == 2 or img_kind == 1:
        for i in range(-10, 10):
            count = 0
            _y = basic_line+note_width*i
            if _y <= y:
                continue
            if _y >= y+h:
                break
            for j in range(x, x+w):
                if (img[_y+3, j] != white).all():
                    count += 1
            if count > 20:
                scale.append(i)
    elif img_kind == 4:
        half_x = (x+x+w)//2
        for i in range(-10, 10):
            _y = basic_line+note_width*i
            if _y <= y:
                continue
            if _y >= y+h:
                break
            if (img[_y+3, half_x] != white).all() or (img[_y+3, half_x+5] != white).all():
                scale.append(i)
    elif img_kind == 8 or img_kind == 16:
        for i in range(-10, 10):
            count = 0
            _y = basic_line+note_width*i
            if _y <= y:
                continue
            if _y >= y+h:
                break
            for j in range(x, x+w):
                if (img[_y+3, j] != white).all() and (img[_y+3, x] == white).all() and (img[_y+3, x+w] == white).all():
                    count += 1
            if count > 20:
                scale.append(i)
    print(scale)
    return scale
