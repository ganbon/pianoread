import os
import glob
from mng_score import Score
from prot import Prot

names = glob.glob("../testdata/*")
number=0


def main(path, number):
    PATH = path
    print(path)
    score = Score(PATH)
    lines_data, pitch = score.detect_lines()
    if pitch == 0:
        return
    score.register_stf(lines_data)
    print(lines_data)
    imgs = score.imgs
    prot = Prot()
    prot.export_img(imgs)
    prot.paragraph(lines_data, imgs[1])

    marbles = score.labeling(pitch, number)
    prot.marbles(marbles)


for name in names:
    if __name__ == '__main__':
        namepath = os.path.split(name)
        number = namepath[1].replace('.png', '')
        number = int(number)
        main(name, number)
        print(number)
    number += 1
