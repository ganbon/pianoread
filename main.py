from mng_score import Score
from prot import Prot


def main():
    PATH = "./data/Original_Score/0007.jpg"
    score = Score(PATH)
    lines_data, pitch = score.detect_lines()
    score.register_stf(lines_data)

    print(lines_data)
    imgs = score.imgs
    prot = Prot()
    prot.export_img(imgs)
    prot.paragraph(lines_data, imgs[1])

    marbles = score.labeling(pitch)
    prot.marbles(marbles)


if __name__ == '__main__':
    main()