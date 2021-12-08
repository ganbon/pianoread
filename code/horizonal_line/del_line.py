from horizonal_line.prot import Prot
from horizonal_line.mng_score import Score
from horizonal_line.line_data import scoreline_data
import cv2
#横線削除
def horizonal_del(path):
    PATH = path
    score = Score(PATH)
    lines_data, pitch = score.detect_lines()
    if pitch == 0:
        return
    score.register_stf(lines_data)
    #print(lines_data)
    lines_data=scoreline_data(path)
    imgs = score.imgs
    prot = Prot()
    prot.export_img(imgs)
    prot.paragraph(lines_data, imgs[1])
    marbles,img = score.labeling()
    prot.marbles(marbles)
    return img
