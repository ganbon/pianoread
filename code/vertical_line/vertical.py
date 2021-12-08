import cv2
from horizonal_line.line_data import scoreline_data

#縦ラインの取得と削除
def vertical_data(img,data):
    ver_data=[]
    img2=img.copy()
    white = [255, 255, 255]
    height, width = img.shape[:2]
    hlines = scoreline_data(data)
    if hlines == None:
        return
    for i, hline in enumerate(hlines):
        ver_list=[]
        scoreheight_head = hline[0][0][0]
        try:
            scoreheight_end = hline[1][4][0]
        except IndexError:
            scoreheight_end = hline[0][4][0]
        scorerange = (scoreheight_end-scoreheight_head)*0.8
        for x in range(width):
            check = 0
            for y in range(int(scoreheight_head), int(scoreheight_end)):
                if (img[y, x] == white).all():
                    continue
                else:
                    check += 1
            if check > scorerange:
                cv2.line(img2, (x, int(scoreheight_head)),
                         (x, int(scoreheight_end)), (255, 255, 255), 3)
                ver_list.append(x)
        ver_data.append(ver_list)
    return ver_data,img2