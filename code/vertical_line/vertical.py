import cv2
from horizonal_line.line_data import scoreline_data

#縦ラインの取得と削除
def vertical_data(img,data):
    img2=img.copy()
    black = [0, 0, 0]
    whilte=[255,255,255]
    height, width = img.shape[:2]
    hlines = scoreline_data(data)
    if hlines == None:
        return
    for i, hline in enumerate(hlines):
        ver_list=[]
        scoreheight_head = int(hline[0][4][0])
        try:
            scoreheight_end = int(hline[1][0][0])
        except IndexError:
            scoreheight_end = int(hline[0][4][0])
        judline=[scoreheight_head+5,int((scoreheight_end+scoreheight_head)/2),scoreheight_end-5]
        for x in range(width):
            if (img[judline[0],x] != whilte).all() and (img[judline[1],x] != whilte).all() and (img[judline[2],x] != whilte).all():
                cv2.line(img2, (x, int(hline[0][0][0])),(x, int(hline[1][4][0])), (255, 255, 255), 3)
                ver_list.append(x)
    return ver_list,img2