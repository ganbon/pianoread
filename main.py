import staff_notation as stf
import bar_line as bl
import draw
import remove_lines as rl
import cv2
import numpy as np
import math
from scipy import ndimage

# 画像の読み込み
img = cv2.imread("./data/Original_Score/0014.jpg", 0)

arg = stf.get_degree(img)
img = ndimage.rotate(img, arg, cval=255)
ret, img_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
h, w = img.shape[:2]

staff_notation_assist2, dot_list = stf.extract_lines(img_otsu)
staff_notation_opts1, line_list = stf.extract_long_lines(img_otsu)
staff_notation_opts2 = stf.data_shaping(staff_notation_opts1)
staff_notation_opts3, line_pitch = stf.grouping_staff_notation(staff_notation_opts2, h)

staff_notation_assist = stf.extract_lines_H(img_otsu)

stf.draw_staff_notation(staff_notation_opts3, img_otsu)
stf.draw_info(img, img_otsu, staff_notation_assist, staff_notation_opts1, dot_list, line_list)

staff_notation = stf.get_staff_notation(staff_notation_opts3)
print(staff_notation)

# 閾値がいくつになったか確認
# print("ret: {}\n{}×{}".format(ret, W, H))
# print("arg: {}".format(arg))

cv2.imwrite('data/dst/img_otsu.jpg', img_otsu)

bar_line_opts1, ver_dot_list = bl.extract_lines(img_otsu, staff_notation)
bl.draw_info(img_otsu, bar_line_opts1, staff_notation, ver_dot_list)

bar_line = []
for item in bar_line_opts1:
  bar_line.append(bl.data_shaping(item))

img_result = rl.extract_obj(img_otsu, staff_notation, bar_line, line_pitch)

cv2.imwrite('data/dst/result.jpg', img_result)