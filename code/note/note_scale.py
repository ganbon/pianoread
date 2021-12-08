import cv2
from horizonal_line.line_data import scoreline_data

#音階判定
def scale_disc(path, img_data):
    x, y, h, w = img_data
    white = [255, 255, 255]
    black = [0, 0, 0]
    scale = []
    horizonal_line = scoreline_data(path)
    img = cv2.imread(path)
    note_width = int((horizonal_line[0][0][0][1]-horizonal_line[0][0][0][0])/2)
    for line in horizonal_line:
        basic_line = int(line[0][0][0])
        # 0(基準)がド
        for i in range(-7, 7):
            _y = basic_line+note_width*i
            if _y < y:
                continue
            if _y > y+h:
                break
            for _x in range(int(x), int(x+w)):
                if (img[_y+basic_line-1, _x] == black).all() and (img[_y-basic_line+1, _x] == black).all():
                    scale.append(i)
    return scale
